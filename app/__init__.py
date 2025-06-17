from flask import Flask, current_app
from app.extensions import login_manager, bcrypt
from app.utils.csv_manager import CsvManager
from app.models.user import User
from app.models.issue import Issue
from config import Config

@login_manager.user_loader
def load_user(username):
    """Flask-Login 需要的方法，根据用户名加载用户"""
    if not current_app:
        return None
    user_manager = current_app.user_manager
    return user_manager.get_item_by_id(username, 'username')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化 Flask-Login
    login_manager.init_app(app)
    
    # 初始化 Flask-Bcrypt
    bcrypt.init_app(app)

    # 初始化 CSV 管理器
    app.user_manager = CsvManager(Config.USERS_CSV, User)
    app.issue_manager = CsvManager(Config.ISSUES_CSV, Issue)

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
    from app.routes.auth import bp as auth_bp
    from app.routes.admin import bp as admin_bp
    from app.routes.user import bp as user_bp
    from app.routes.engineer import bp as engineer_bp
    from app.routes.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(engineer_bp)
    app.register_blueprint(main_bp)

    return app 