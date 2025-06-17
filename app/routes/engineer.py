from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.models.issue import Issue

bp = Blueprint('engineer', __name__, url_prefix='/engineer')

# Helper function to check if current user is an engineer or admin
def engineer_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (current_user.role != 'engineer' and current_user.role != 'admin'):
            flash('您没有权限访问此页面。', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@engineer_required
def dashboard():
    return render_template('engineer/dashboard.html', title='工程师仪表盘')

@bp.route('/issues')
@engineer_required
def issues_list():
    issue_manager = current_app.issue_manager
    all_issues = issue_manager.read_all()
    
    # For now, display all issues for engineers. Later, add filtering for assigned/followed issues.
    issues = all_issues # Placeholder

    return render_template('engineer/issues.html', title='工程师问题列表', issues=issues)

@bp.route('/issues/<issue_id>')
@engineer_required
def issue_detail_engineer(issue_id):
    issue_manager = current_app.issue_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')

    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('engineer.issues_list'))

    return render_template('engineer/issue_detail.html', title='问题详情', issue=issue)

@bp.route('/issues/<issue_id>/process', methods=['GET', 'POST'])
@engineer_required
def process_issue(issue_id):
    issue_manager = current_app.issue_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')

    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('engineer.issues_list'))

    if request.method == 'POST':
        new_status = request.form.get('status')
        extra_info = request.form.get('extra_info')
        assign_to_me = request.form.get('assign_to_me')

        if new_status:
            issue.status = new_status
        if extra_info:
            issue.extra_info = extra_info # Overwrite for simplicity, or append in real app
        if assign_to_me == 'on':
            issue.assigned_to_user_id = current_user.get_id()
            issue.status = 'Assigned' # Automatically set to Assigned if assigned

        issue_manager.update_item(issue.issue_id, issue, 'issue_id')
        flash('问题处理信息已更新！', 'success')
        return redirect(url_for('engineer.issue_detail_engineer', issue_id=issue.issue_id))

    return render_template('engineer/issue_process.html', title='处理问题', issue=issue) 