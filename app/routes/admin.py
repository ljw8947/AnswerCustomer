from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.user import User
from app.models.issue import Issue
from functools import wraps

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

@bp.route('/users')
@admin_required
def manage_users():
    user_manager = current_app.user_manager
    users = user_manager.read_all()
    
    role_filter = request.args.get('role')
    search_query = request.args.get('q')

    if role_filter and role_filter != 'all':
        users = [u for u in users if u.role == role_filter]
    if search_query:
        users = [u for u in users if search_query.lower() in u.username.lower() or search_query.lower() in u.email.lower()]

    return render_template('admin/users.html', title='用户管理', users=users, 
                           current_role_filter=role_filter, current_search_query=search_query)

@bp.route('/users/<user_id>/status', methods=['POST'])
@admin_required
def update_user_status(user_id):
    user_manager = current_app.user_manager
    user = user_manager.get_item_by_id(user_id, 'user_id')
    if not user:
        flash('用户未找到。', 'danger')
        return redirect(url_for('admin.manage_users'))

    new_status = request.form.get('status')
    if new_status in ['active', 'inactive', 'suspended']:
        user.status = new_status
        user_manager.update_item(user_id, user, 'user_id')
        flash(f'用户 {user.username} 状态已更新为 {new_status}。', 'success')
    else:
        flash('无效的用户状态。', 'danger')
    return redirect(url_for('admin.manage_users'))

@bp.route('/issues')
@admin_required
def manage_issues():
    issue_manager = current_app.issue_manager
    issues = issue_manager.read_all()

    # Placeholder for filtering and searching issues
    # No specific changes needed here as 'function' was not explicitly processed
    return render_template('admin/issues.html', title='问题管理', issues=issues)

@bp.route('/issues/<issue_id>')
@admin_required
def issue_detail(issue_id):
    issue_manager = current_app.issue_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')
    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('admin.manage_issues'))
    return render_template('admin/issue_detail.html', title='问题详情', issue=issue)

@bp.route('/config', methods=['GET', 'POST'])
@admin_required
def configure_settings():
    if request.method == 'POST':
        # Placeholder for saving configuration
        issue_types = request.form.get('issueTypes')
        max_description_length = request.form.get('maxDescriptionLength')
        max_title_length = request.form.get('maxTitleLength')
        
        # In a real application, you would save these to a config file or database
        flash('配置已成功保存！(实际保存逻辑待实现)', 'success')
        return redirect(url_for('admin.configure_settings'))

    return render_template('admin/config.html', title='参数配置') 