import csv
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.issue import Issue
from app.models.category import Category
from app.utils.csv_importer import CsvImporter
from app.utils.category_importer import CategoryImporter
from app.utils.email_notifier import MockEmailNotifier
from functools import wraps
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function to check if current user is admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('您没有权限访问此页面。', 'danger')
            return redirect(url_for('main.index')) # Redirect to main page or login
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@admin_required
def dashboard():
    # Admin Dashboard
    return render_template('admin/dashboard.html', title='管理员仪表盘')

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
    
    # 数据倒序显示（按创建时间倒序）
    filtered_issues.sort(key=lambda x: x.create_time or '', reverse=True)
    
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
                         title='问题管理', 
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
        flash('问题未找到。', 'danger')
        return redirect(url_for('admin.manage_issues'))
    return render_template('admin/issue_detail.html', title='问题详情', issue=issue)

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
    
    return render_template('admin/categories.html', title='Specific Function管理', categories=categories)

@bp.route('/categories/<category_id>', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    category_manager = current_app.category_manager
    category = category_manager.get_item_by_id(category_id, 'category_id')
    
    if not category:
        flash('Specific Function未找到。', 'danger')
        return redirect(url_for('admin.manage_categories'))
    
    if request.method == 'POST':
        email_list = request.form.get('email_list', '').strip()
        
        # 解析和验证邮箱列表
        emails = CategoryImporter.parse_email_list(email_list)
        
        # 更新邮箱列表
        category.set_email_list(emails)
        category_manager.update_item(category.category_id, category, 'category_id')
        
        flash('邮箱列表已更新！', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/edit_category.html', title='编辑Specific Function', category=category)

@bp.route('/categories/import', methods=['GET', 'POST'])
@admin_required
def import_categories():
    if request.method == 'POST':
        category_manager = current_app.category_manager
        file = request.files.get('csv_file')
        if not file or file.filename == '':
            flash('请上传 category.csv 文件。', 'danger')
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
                flash('CSV文件为空或格式错误', 'danger')
                return redirect(request.url)
                
            if 'Specific Function' not in reader.fieldnames:
                flash(f'CSV文件格式错误：缺少"Specific Function"列。当前列名: {reader.fieldnames}', 'danger')
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
                    flash(f'处理第{row_num}行时出错: {str(e)}', 'warning')
                    continue
            
            flash(f'Specific Function配置导入成功！新增{imported_count}条，更新{updated_count}条。', 'success')
        except Exception as e:
            flash(f'导入category.csv时发生错误: {str(e)}', 'danger')
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")
        return redirect(url_for('admin.manage_categories'))
    return render_template('admin/import_categories.html', title='导入Specific Function配置')

@bp.route('/import_csv', methods=['GET', 'POST'])
@admin_required
def import_csv():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('没有选择文件。', 'danger')
            return redirect(request.url)
        file = request.files['csv_file']
        if file.filename == '':
            flash('没有选择文件。', 'danger')
            return redirect(request.url)
        if not file.filename.endswith('.csv'):
            flash('请上传 CSV 文件。', 'danger')
            return redirect(request.url)
        try:
            csv_content = file.read().decode('utf-8')
            validation_result = CsvImporter.validate_csv_format(csv_content)
            if not validation_result['valid']:
                flash(f'CSV 格式验证失败: {validation_result["message"]}', 'danger')
                return redirect(request.url)
            
            issue_manager = current_app.issue_manager
            category_manager = current_app.category_manager
            
            # 使用 MockEmailNotifier 进行测试（实际部署时可替换为真实的 EmailNotifier）
            email_notifier = MockEmailNotifier()
            
            import_result = CsvImporter.import_from_directvoice_format(
                csv_content, issue_manager, category_manager, email_notifier, batch_id=datetime.now().strftime('%Y%m%d_%H%M%S')
            )
            
            if import_result['imported_count'] > 0:
                flash(f'CSV 导入完成！成功导入 {import_result["imported_count"]} 条记录，跳过 {import_result["skipped_count"]} 条记录。批号: {import_result["batch_id"]}', 'success')
                
                # 显示通知结果
                if import_result.get('notification_results'):
                    notification_summary = []
                    success_count = 0
                    for result in import_result['notification_results']:
                        if result['status'] == 'success':
                            success_count += 1
                            notification_summary.append(f"{result['specific_function']}: 成功发送给 {len(result['recipients'])} 个邮箱")
                        elif result['status'] == 'skipped':
                            notification_summary.append(f"{result['specific_function']}: 跳过 ({result['reason']})")
                        else:
                            notification_summary.append(f"{result['specific_function']}: 失败 ({result['reason']})")
                    
                    if success_count > 0:
                        flash(f'邮件通知: 成功发送 {success_count} 个通知。详情: ' + '; '.join(notification_summary), 'info')
                    else:
                        flash('邮件通知: 没有发送任何通知。', 'warning')
                
                if import_result['errors']:
                    error_msg = f'导入过程中遇到 {len(import_result["errors"])} 个错误:'
                    for error in import_result['errors'][:5]:
                        error_msg += f'<br>- {error}'
                    if len(import_result['errors']) > 5:
                        error_msg += f'<br>- ... 还有 {len(import_result["errors"]) - 5} 个错误'
                    flash(error_msg, 'warning')
            else:
                flash('没有成功导入任何记录。', 'warning')
            return redirect(url_for('admin.manage_issues'))
        except Exception as e:
            flash(f'导入过程中发生错误: {str(e)}', 'danger')
            return redirect(request.url)
    return render_template('admin/import_csv.html', title='导入 CSV')

@bp.route('/config', methods=['GET', 'POST'])
@admin_required
def configure_settings():
    if request.method == 'POST':
        flash('配置已成功保存！(实际保存逻辑待实现)', 'success')
        return redirect(url_for('admin.configure_settings'))
    return render_template('admin/config.html', title='参数配置')

@bp.route('/issues/<issue_id>/notify', methods=['POST'])
@admin_required
def notify_issue(issue_id):
    """发送单个问题的通知邮件"""
    issue_manager = current_app.issue_manager
    category_manager = current_app.category_manager
    
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')
    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('admin.manage_issues'))
    
    # 查找对应的分类配置
    all_categories = category_manager.read_all()
    category = None
    for cat in all_categories:
        if cat.specific_function == issue.specific_function:
            category = cat
            break
    
    if not category or not category.email_list:
        flash(f'未找到"{issue.specific_function}"的邮箱配置。', 'warning')
        return redirect(url_for('admin.manage_issues'))
    
    # 获取邮箱列表
    emails = category.email_list.split(',') if category.email_list else []
    emails = [email.strip() for email in emails if email.strip()]
    
    if not emails:
        flash(f'"{issue.specific_function}"没有配置有效的邮箱地址。', 'warning')
        return redirect(url_for('admin.manage_issues'))
    
    # 使用 MockEmailNotifier 发送通知
    email_notifier = MockEmailNotifier()
    email_notifier.clear_sent_emails()
    
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
        
        flash(f'通知邮件已发送给 {len(emails)} 个邮箱地址。', 'success')
    else:
        flash('发送通知邮件失败。', 'danger')
    
    return redirect(url_for('admin.manage_issues')) 