from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.user import User
from app.models.issue import Issue
from werkzeug.security import generate_password_hash # Import for password change
from app import bcrypt # Import bcrypt
from config import Config # Import Config to access MERCEDES_CARLINES

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
@login_required
def dashboard():
    return render_template('user/dashboard.html', title='用户仪表盘') # Placeholder dashboard

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_manager = current_app.user_manager
    if request.method == 'POST':
        current_user.username = request.form.get('username', current_user.username)
        current_user.email = request.form.get('email', current_user.email)
        
        # Handle password change if provided
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password:
            if new_password != confirm_password:
                flash('新密码和确认密码不匹配。', 'danger')
                return redirect(url_for('user.profile'))
            current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        
        # Placeholder for avatar upload logic
        # current_user.avatar_url = ...

        user_manager.update_item(current_user.user_id, current_user, 'user_id')
        flash('个人信息已成功更新！', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/profile.html', title='个人信息', user=current_user)

@bp.route('/submit_issue', methods=['GET', 'POST'])
@login_required
def submit_issue():
    issue_manager = current_app.issue_manager
    if request.method == 'POST':
        carline = request.form.get('carline')
        # power = request.form.get('power') # Removed
        specific_function = request.form.get('specific_function')
        # function = request.form.get('function') # Removed
        general = request.form.get('general')
        issue_type = request.form.get('issue_type')
        description = request.form.get('description')
        brief_issue = request.form.get('brief_issue')

        # Calculate global_id
        all_issues = issue_manager.read_all()
        global_id = 1
        if all_issues:
            max_global_id = 0
            for issue in all_issues:
                if issue.global_id is not None:
                    max_global_id = max(max_global_id, issue.global_id)
            global_id = max_global_id + 1

        # Calculate user_issue_id
        user_issues = [issue for issue in all_issues if issue.created_by_user_id == current_user.get_id()]
        user_issue_id = 1
        if user_issues:
            max_user_issue_id = 0
            for issue in user_issues:
                if issue.user_issue_id is not None:
                    max_user_issue_id = max(max_user_issue_id, issue.user_issue_id)
            user_issue_id = max_user_issue_id + 1

        new_issue = Issue(
            carline=carline,
            # power=power, # Removed
            specific_function=specific_function,
            # function=function, # Removed
            general=general,
            issue_type=issue_type,
            description=description,
            brief_issue=brief_issue,
            global_id=global_id,
            user_issue_id=user_issue_id,
            created_by_user_id=current_user.get_id()
        )
        issue_manager.add_item(new_issue)
        flash('问题已成功提交！', 'success')
        return redirect(url_for('user.my_issues'))

    return render_template('user/submit_issue.html', title='提交新问题', carlines=Config.MERCEDES_CARLINES)

@bp.route('/my_issues')
@login_required
def my_issues():
    issue_manager = current_app.issue_manager
    all_issues = issue_manager.read_all()
    # Filter issues by current_user.user_id
    issues = [issue for issue in all_issues if issue.created_by_user_id == current_user.get_id()]
    return render_template('user/my_issues.html', title='我的问题', issues=issues)

@bp.route('/issues/<issue_id>')
@login_required
def issue_detail(issue_id):
    issue_manager = current_app.issue_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')

    if not issue or issue.created_by_user_id != current_user.get_id():
        flash('问题未找到或您无权查看。', 'danger')
        return redirect(url_for('user.my_issues'))

    return render_template('user/issue_detail.html', title='问题详情', issue=issue)

@bp.route('/issues/<issue_id>/edit', methods=['GET', 'POST'])
@login_required
def issue_edit(issue_id):
    issue_manager = current_app.issue_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')

    if not issue or issue.created_by_user_id != current_user.get_id():
        flash('问题未找到或您无权编辑。', 'danger')
        return redirect(url_for('user.my_issues'))

    if request.method == 'POST':
        issue.carline = request.form.get('carline', issue.carline)
        # issue.power = request.form.get('power', issue.power) # Removed
        issue.specific_function = request.form.get('specific_function', issue.specific_function)
        # issue.function = request.form.get('function', issue.function) # Removed
        issue.general = request.form.get('general', issue.general)
        issue.issue_type = request.form.get('issue_type', issue.issue_type)
        issue.description = request.form.get('description', issue.description)
        issue.brief_issue = request.form.get('brief_issue', issue.brief_issue)
        
        issue_manager.update_item(issue.issue_id, issue, 'issue_id')
        flash('问题已成功更新！', 'success')
        return redirect(url_for('user.issue_detail', issue_id=issue.issue_id))

    return render_template('user/issue_edit.html', title='编辑问题', issue=issue, carlines=Config.MERCEDES_CARLINES) 