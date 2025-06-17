from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models.user import User
from flask import current_app # Import current_app
from app.extensions import bcrypt  # 从 extensions.py 导入 bcrypt
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_password(password):
    """验证密码强度"""
    if len(password) < 6:
        return False, "密码长度至少为6位"
    if not re.search(r"[A-Z]", password):
        return False, "密码需要包含至少一个大写字母"
    if not re.search(r"[a-z]", password):
        return False, "密码需要包含至少一个小写字母"
    if not re.search(r"\d", password):
        return False, "密码需要包含至少一个数字"
    return True, "密码强度符合要求"

def validate_username(username):
    """验证用户名格式"""
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        return False, "用户名只能包含字母、数字和下划线，长度在3-20位之间"
    return True, "用户名格式正确"

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If user is already logged in, redirect based on role
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'engineer':
            return redirect(url_for('engineer.dashboard'))
        else:
            return redirect(url_for('user.my_issues'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        user_manager = current_app.user_manager
        user = user_manager.get_item_by_id(username, 'username')

        if user and bcrypt.check_password_hash(user.password_hash, password):
            if user.status == 'inactive':
                flash('您的账号已被禁用，请联系管理员。', 'danger')
                return redirect(url_for('auth.login'))
            if user.status == 'suspended':
                flash('您的账号已被暂停，请联系管理员。', 'danger')
                return redirect(url_for('auth.login'))

            login_user(user, remember=remember)
            flash('登录成功！', 'success')
            
            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'engineer':
                return redirect(url_for('engineer.dashboard'))
            else:
                return redirect(url_for('user.my_issues'))
        else:
            flash('用户名或密码错误。', 'danger')

    return render_template('auth/login.html', title='登录')

@bp.route('/register')
def register():
    """重定向到顾客注册页面"""
    return redirect(url_for('auth.register_customer'))

@bp.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'engineer':
            return redirect(url_for('engineer.dashboard'))
        else:
            return redirect(url_for('user.my_issues'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 验证用户名格式
        is_valid_username, username_msg = validate_username(username)
        if not is_valid_username:
            flash(username_msg, 'danger')
            return redirect(url_for('auth.register_customer'))

        # 验证密码强度
        is_valid_password, password_msg = validate_password(password)
        if not is_valid_password:
            flash(password_msg, 'danger')
            return redirect(url_for('auth.register_customer'))

        if password != confirm_password:
            flash('两次输入的密码不匹配。', 'danger')
            return redirect(url_for('auth.register_customer'))

        user_manager = current_app.user_manager
        existing_user = user_manager.get_item_by_id(username, 'username')
        if existing_user:
            flash('用户名已存在。', 'danger')
            return redirect(url_for('auth.register_customer'))

        new_user = User(
            username=username,
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='user',  # 顾客角色
            status='active'  # 默认状态为激活
        )
        user_manager.add_item(new_user)
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register_customer.html', title='顾客注册')

@bp.route('/register/engineer', methods=['GET', 'POST'])
def register_engineer():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'engineer':
            return redirect(url_for('engineer.dashboard'))
        else:
            return redirect(url_for('user.my_issues'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        employee_id = request.form.get('employee_id')

        # 验证用户名格式
        is_valid_username, username_msg = validate_username(username)
        if not is_valid_username:
            flash(username_msg, 'danger')
            return redirect(url_for('auth.register_engineer'))

        # 验证密码强度
        is_valid_password, password_msg = validate_password(password)
        if not is_valid_password:
            flash(password_msg, 'danger')
            return redirect(url_for('auth.register_engineer'))

        if password != confirm_password:
            flash('两次输入的密码不匹配。', 'danger')
            return redirect(url_for('auth.register_engineer'))

        # TODO: 验证工号的有效性（可以添加工号验证逻辑）
        if not employee_id:
            flash('请输入工号。', 'danger')
            return redirect(url_for('auth.register_engineer'))

        user_manager = current_app.user_manager
        existing_user = user_manager.get_item_by_id(username, 'username')
        if existing_user:
            flash('用户名已存在。', 'danger')
            return redirect(url_for('auth.register_engineer'))

        # 创建工程师账号，但状态设为待审核
        new_user = User(
            username=username,
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='engineer',  # 工程师角色
            status='pending',  # 状态为待审核
            employee_id=employee_id  # 存储工号
        )
        user_manager.add_item(new_user)
        flash('注册申请已提交，请等待管理员审核。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register_engineer.html', title='工程师注册')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出登录。', 'success')
    return redirect(url_for('auth.login')) 