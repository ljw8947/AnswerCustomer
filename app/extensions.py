from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录。'
login_manager.login_message_category = 'info'

# 初始化 Flask-Bcrypt
bcrypt = Bcrypt() 