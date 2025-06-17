import os
from flask import Flask, current_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from markupsafe import Markup
from app.utils.csv_manager import CsvManager
from app.models.user import User
from app.models.issue import Issue
from app.models.comment import Comment
from app.models.category import Category
from config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    """Flask-Login 需要的方法，根据用户名加载用户"""
    if not current_app:
        return None
    user_manager = current_app.user_manager
    return user_manager.get_item_by_id(username, 'username')

def nl2br(value):
    """将换行符转换为HTML的<br>标签"""
    if value:
        # 使用Markup确保HTML标签被正确渲染
        return Markup(value.replace('\n', '<br>'))
    return value

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 注册自定义过滤器
    app.jinja_env.filters['nl2br'] = nl2br

    bcrypt.init_app(app)
    login_manager.init_app(app)

    # CSV managers
    app.user_manager = CsvManager(Config.USERS_CSV, User)
    app.issue_manager = CsvManager(Config.ISSUES_CSV, Issue)
    app.comment_manager = CsvManager(Config.COMMENTS_CSV, Comment)
    app.category_manager = CsvManager(Config.CATEGORY_CSV, Category)

    # 确保默认管理员账户存在
    with app.app_context():
        user_manager = app.user_manager
        admin = user_manager.get_item_by_id('admin', 'username')
        if not admin:
            # 创建默认管理员账户
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=bcrypt.generate_password_hash('admin_password').decode('utf-8'),
                role='admin',
                status='active'
            )
            user_manager.add_item(admin)
            print("Default admin account created.")

    # 注册蓝图
    from app.routes.admin import bp as admin_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.engineer import bp as engineer_bp
    from app.routes.main import bp as main_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(engineer_bp)
    app.register_blueprint(main_bp)

    return app 