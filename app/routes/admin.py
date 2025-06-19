import csv
import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.models.issue import Issue
from app.models.category import Category
from app.utils.csv_importer import CsvImporter
from app.utils.category_importer import CategoryImporter
from app.utils.email_notifier import EmailNotifier
from app.utils.config_manager import ConfigManager
from functools import wraps
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function to check if current user is admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index')) # Redirect to main page or login
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@admin_required
def dashboard():
    # Admin Dashboard
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@bp.route('/issues')
@admin_required
def manage_issues():
    issue_manager = current_app.issue_manager
    category_manager = current_app.category_manager
    all_issues = issue_manager.read_all()
    
    # 获取所有Category数据用于下拉列表
    all_categories = category_manager.read_all()
    
    # 获取唯一的Function Domain和Specific Function选项
    function_domains = sorted(list(set([cat.function_domain for cat in all_categories if cat.function_domain])))
    specific_functions = sorted(list(set([cat.specific_function for cat in all_categories if cat.specific_function])))
    
    # 应用筛选条件
    filtered_issues = all_issues
    
    # 状态筛选
    status_filter = request.args.get('status')
    if status_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.status == status_filter]
    
    # 车型筛选
    carline_filter = request.args.get('carline')
    if carline_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.carline == carline_filter]
    
    # 功能域筛选
    function_domain_filter = request.args.get('function_domain')
    if function_domain_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.function_domain == function_domain_filter]
    
    # 具体功能筛选
    specific_function_filter = request.args.get('specific_function')
    if specific_function_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.specific_function == specific_function_filter]
    
    # 数据倒序显示（按issue_id降序）
    filtered_issues.sort(key=lambda x: int(x.issue_id) if x.issue_id and x.issue_id.isdigit() else 0, reverse=True)
    
    # 分页处理 - 固定每页20条记录
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 固定每页显示20条记录
    
    total_issues = len(filtered_issues)
    total_pages = (total_issues + per_page - 1) // per_page
    
    # 确保page在有效范围内
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # 计算分页切片
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_issues = filtered_issues[start_idx:end_idx]

    return render_template('admin/issues.html', 
                         title='Issue Management', 
                         issues=paginated_issues,
                         function_domains=function_domains,
                         specific_functions=specific_functions,
                         page=page,
                         per_page=per_page,
                         total_pages=total_pages,
                         total_issues=total_issues)

@bp.route('/issues/<issue_id>')
@admin_required
def issue_detail(issue_id):
    issue_manager = current_app.issue_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')
    if not issue:
        flash('Issue not found.', 'danger')
        return redirect(url_for('admin.manage_issues'))
    return render_template('admin/issue_detail.html', title='Issue Detail', issue=issue)

@bp.route('/categories')
@admin_required
def manage_categories():
    category_manager = current_app.category_manager
    categories = category_manager.read_all()
    
    # 按General Domain、Function Domain、Specific Function降序排列
    categories.sort(key=lambda x: (
        x.general_domain or '', 
        x.function_domain or '', 
        x.specific_function or ''
    ), reverse=False)
    
    return render_template('admin/categories.html', title='Specific Function Management', categories=categories)

@bp.route('/categories/<category_id>', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    category_manager = current_app.category_manager
    category = category_manager.get_item_by_id(category_id, 'category_id')
    
    if not category:
        flash('Specific Function not found.', 'danger')
        return redirect(url_for('admin.manage_categories'))
    
    if request.method == 'POST':
        email_list = request.form.get('email_list', '').strip()
        
        # 解析和验证邮箱列表
        emails = CategoryImporter.parse_email_list(email_list)
        
        # 更新邮箱列表
        category.set_email_list(emails)
        category_manager.update_item(category.category_id, category, 'category_id')
        
        flash('Email list updated!', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/edit_category.html', title='Edit Specific Function', category=category)

@bp.route('/categories/import', methods=['GET', 'POST'])
@admin_required
def import_categories():
    if request.method == 'POST':
        category_manager = current_app.category_manager
        file = request.files.get('csv_file')
        if not file or file.filename == '':
            flash('Please upload category.csv file.', 'danger')
            return redirect(request.url)
        try:
            # 读取上传的CSV内容，处理BOM字符
            csv_content = file.read()
            if csv_content.startswith(b'\xef\xbb\xbf'):
                csv_content = csv_content[3:]  # 移除BOM
            csv_content = csv_content.decode('utf-8')
            
            import io
            reader = csv.DictReader(io.StringIO(csv_content))
            
            # 检查列名是否存在
            if not reader.fieldnames:
                flash('CSV file is empty or format error', 'danger')
                return redirect(request.url)
                
            if 'Specific Function' not in reader.fieldnames:
                flash(f'CSV file format error: Missing "Specific Function" column. Current column names: {reader.fieldnames}', 'danger')
                return redirect(request.url)
            
            imported_count = 0
            updated_count = 0
            
            for row_num, row in enumerate(reader, start=2):  # 从第2行开始计数
                try:
                    specific_function = row['Specific Function'].strip()
                    function_domain = row['Function Domain'].strip()
                    general_domain = row['General Domain'].strip()
                    
                    if not specific_function:
                        continue
                    
                    existing_categories = category_manager.read_all()
                    existing = None
                    for cat in existing_categories:
                        if cat.specific_function == specific_function:
                            existing = cat
                            break
                    
                    if existing:
                        existing.function_domain = function_domain
                        existing.general_domain = general_domain
                        category_manager.update_item(existing.category_id, existing, 'category_id')
                        updated_count += 1
                    else:
                        new_category = Category(
                            specific_function=specific_function,
                            function_domain=function_domain,
                            general_domain=general_domain
                        )
                        category_manager.add_item(new_category)
                        imported_count += 1
                except Exception as e:
                    flash(f'Error occurred processing row {row_num}: {str(e)}', 'warning')
                    continue
            
            flash(f'Specific Function configuration imported successfully! Added {imported_count} new, updated {updated_count} existing.', 'success')
        except Exception as e:
            flash(f'Error occurred during import: {str(e)}', 'danger')
            import traceback
            print(f"Detailed error information: {traceback.format_exc()}")
        return redirect(url_for('admin.manage_categories'))
    return render_template('admin/import_categories.html', title='Import Specific Function Configuration')

@bp.route('/import_csv', methods=['GET', 'POST'])
@admin_required
def import_csv():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)
        file = request.files['csv_file']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)
        if not file.filename.endswith('.csv'):
            flash('Please upload CSV file.', 'danger')
            return redirect(request.url)
        try:
            csv_content = file.read().decode('utf-8')
            validation_result = CsvImporter.validate_csv_format(csv_content)
            if not validation_result['valid']:
                flash(f'CSV format validation failed: {validation_result["message"]}', 'danger')
                return redirect(request.url)
            
            issue_manager = current_app.issue_manager
            category_manager = current_app.category_manager
            
            # 使用真实的 EmailNotifier
            email_notifier = EmailNotifier(server_url=request.host_url.rstrip('/'))
            
            import_result = CsvImporter.import_from_directvoice_format(
                csv_content, issue_manager, category_manager, email_notifier, batch_id=datetime.now().strftime('%Y%m%d_%H%M%S')
            )
            
            if import_result['imported_count'] > 0:
                flash(f'CSV import completed! Successfully imported {import_result["imported_count"]} records, skipped {import_result["skipped_count"]} records. Batch: {import_result["batch_id"]}', 'success')
                
                # Show notification result
                if import_result.get('notification_results'):
                    notification_summary = []
                    success_count = 0
                    for result in import_result['notification_results']:
                        if result['status'] == 'success':
                            success_count += 1
                            notification_summary.append(f"{result['specific_function']}: Successfully sent to {len(result['recipients'])} email(s)")
                        elif result['status'] == 'skipped':
                            notification_summary.append(f"{result['specific_function']}: Skipped ({result['reason']})")
                        else:
                            notification_summary.append(f"{result['specific_function']}: Failed ({result['reason']})")
                    
                    if success_count > 0:
                        flash(f'Email notification: Successfully sent {success_count} notification(s). Details: ' + '; '.join(notification_summary), 'info')
                    else:
                        flash('Email notification: No notifications sent.', 'warning')
                
                if import_result['errors']:
                    error_msg = f'Encountered {len(import_result["errors"])} errors during import:'
                    for error in import_result['errors'][:5]:
                        error_msg += f'<br>- {error}'
                    if len(import_result['errors']) > 5:
                        error_msg += f'<br>- ... {len(import_result["errors"]) - 5} more errors'
                    flash(error_msg, 'warning')
            else:
                flash('No records were successfully imported.', 'warning')
            return redirect(url_for('admin.manage_issues'))
        except Exception as e:
            flash(f'Error occurred during import: {str(e)}', 'danger')
            return redirect(request.url)
    return render_template('admin/import_csv.html', title='Import CSV')

@bp.route('/issues/<issue_id>/notify', methods=['POST'])
@admin_required
def notify_issue(issue_id):
    """Send notification email for a single issue"""
    issue_manager = current_app.issue_manager
    category_manager = current_app.category_manager
    
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')
    if not issue:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': 'Issue not found'}), 404
        flash('Issue not found.', 'danger')
        return redirect(url_for('admin.manage_issues'))
    
    # 查找对应的分类配置
    all_categories = category_manager.read_all()
    category = None
    for cat in all_categories:
        if cat.specific_function == issue.specific_function:
            category = cat
            break
    
    if not category or not category.email_list:
        error_msg = f'No email configuration found for "{issue.specific_function}".'
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': error_msg}), 400
        flash(error_msg, 'warning')
        return redirect(url_for('admin.manage_issues'))
    
    # 获取邮箱列表
    emails = category.email_list.split(',') if category.email_list else []
    emails = [email.strip() for email in emails if email.strip()]
    
    if not emails:
        error_msg = f'No valid email addresses configured for "{issue.specific_function}".'
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': error_msg}), 400
        flash(error_msg, 'warning')
        return redirect(url_for('admin.manage_issues'))
    
    # 使用真实的 EmailNotifier
    email_notifier = EmailNotifier(server_url=request.host_url.rstrip('/'))
    
    # 转换问题为字典格式
    issue_dict = issue.to_dict()
    
    # 发送邮件通知
    success = email_notifier.send_issue_notification(
        emails, issue.specific_function, [issue_dict], f"Manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    
    if success:
        # 更新问题的通知状态
        issue.notified = 1
        issue_manager.update_item(issue.issue_id, issue, 'issue_id')
        
        success_msg = f'Notification email sent to {len(emails)} email address(es).'
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': True, 'message': success_msg})
        flash(success_msg, 'success')
    else:
        error_msg = 'Failed to send notification email.'
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': error_msg}), 500
        flash(error_msg, 'danger')
    
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'success': True, 'redirect': url_for('admin.manage_issues')})
    return redirect(url_for('admin.manage_issues'))

@bp.route('/email_config', methods=['GET', 'POST'])
@admin_required
def email_config():
    """Email configuration management page"""
    config_manager = ConfigManager()
    
    if request.method == 'POST':
        try:
            # 获取表单数据
            smtp_server = request.form.get('smtp_server')
            smtp_port = int(request.form.get('smtp_port'))
            smtp_username = request.form.get('smtp_username')
            smtp_password = request.form.get('smtp_password')
            email_from = request.form.get('email_from')
            email_from_name = request.form.get('email_from_name')
            smtp_use_tls = 'smtp_use_tls' in request.form
            
            # 验证必填字段
            if not all([smtp_server, smtp_port, smtp_username, smtp_password, email_from, email_from_name]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(request.url)
            
            # 保存配置
            config_data = {
                'SMTP_SERVER': smtp_server,
                'SMTP_PORT': smtp_port,
                'SMTP_USERNAME': smtp_username,
                'SMTP_PASSWORD': smtp_password,
                'EMAIL_FROM': email_from,
                'EMAIL_FROM_NAME': email_from_name,
                'SMTP_USE_TLS': smtp_use_tls
            }
            
            if config_manager.save_email_config(config_data):
                flash('Email configuration saved!', 'success')
            else:
                flash('Failed to save configuration. Please check file permissions.', 'danger')
            
            return redirect(url_for('admin.email_config'))
            
        except Exception as e:
            flash(f'Error occurred during save: {str(e)}', 'danger')
            return redirect(request.url)
    
    # GET请求：显示当前配置
    config = config_manager.load_email_config()
    
    return render_template('admin/email_config.html', title='Email Configuration Management', config=config)

@bp.route('/test_email_config', methods=['POST'])
@admin_required
def test_email_config():
    """Test email configuration"""
    import tempfile, os, json
    try:
        # 获取表单数据
        smtp_server = request.form.get('smtp_server')
        smtp_port = int(request.form.get('smtp_port'))
        smtp_username = request.form.get('smtp_username')
        smtp_password = request.form.get('smtp_password')
        email_from = request.form.get('email_from')
        email_from_name = request.form.get('email_from_name')
        smtp_use_tls = 'smtp_use_tls' in request.form
        # 验证必填字段
        if not all([smtp_server, smtp_port, smtp_username, smtp_password, email_from]):
            return jsonify({'success': False, 'error': 'Please fill in all required fields.'})
        # 写入临时配置文件
        config_data = {
            'SMTP_SERVER': smtp_server,
            'SMTP_PORT': smtp_port,
            'SMTP_USERNAME': smtp_username,
            'SMTP_PASSWORD': smtp_password,
            'EMAIL_FROM': email_from,
            'EMAIL_FROM_NAME': email_from_name,
            'SMTP_USE_TLS': smtp_use_tls
        }
        with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.json') as tmpf:
            json.dump(config_data, tmpf, ensure_ascii=False)
            tmpf.flush()
            tmp_config_file = tmpf.name
        # 创建邮件通知器，传入临时配置文件
        email_notifier = EmailNotifier(server_url=request.host_url.rstrip('/'), config_file=tmp_config_file)
        # 创建测试邮件数据
        test_issues = [{
            'global_id': 999,
            'carline': 'Test Car',
            'function_domain': 'Test Domain',
            'issue_type': 'Test Issue',
            'brief_issue_en': 'This is a test email from AnswerCustomer system',
            'create_time': datetime.now().strftime('%Y-%m-%d'),
            'status': 'New'
        }]
        # 发送测试邮件
        success = email_notifier.send_issue_notification(
            [smtp_username],  # Send to configured email
            'Test Function',
            test_issues,
            f"Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        # 删除临时配置文件
        os.unlink(tmp_config_file)
        if success:
            return jsonify({
                'success': True,
                'test_email': smtp_username,
                'message': 'Test email sent successfully.'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send test email. Please check your configuration.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error occurred during test: {str(e)}'
        })

@bp.route('/issues/<issue_id>/check_email_config', methods=['GET'])
@admin_required
def check_issue_email_config(issue_id):
    """Check email configuration for an issue"""
    issue_manager = current_app.issue_manager
    category_manager = current_app.category_manager
    
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')
    if not issue:
        return jsonify({'success': False, 'error': 'Issue not found'})
    
    # 查找对应的分类配置
    all_categories = category_manager.read_all()
    category = None
    for cat in all_categories:
        if cat.specific_function == issue.specific_function:
            category = cat
            break
    
    if not category:
        return jsonify({
            'success': False, 
            'error': f'No email configuration found for "{issue.specific_function}"',
            'has_config': False
        })
    
    if not category.email_list:
        return jsonify({
            'success': False, 
            'error': f'No email addresses configured for "{issue.specific_function}"',
            'has_config': False
        })
    
    # 获取邮箱列表
    emails = category.email_list.split(',') if category.email_list else []
    emails = [email.strip() for email in emails if email.strip()]
    
    if not emails:
        return jsonify({
            'success': False, 
            'error': f'No valid email addresses configured for "{issue.specific_function}"',
            'has_config': False
        })
    
    return jsonify({
        'success': True,
        'has_config': True,
        'emails': emails,
        'specific_function': issue.specific_function,
        'message': f'Found {len(emails)} email address(es)'
    }) 