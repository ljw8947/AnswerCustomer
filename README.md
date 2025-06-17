# AnswerCustomer

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📝 项目简介

AnswerCustomer 是一个基于 Flask 框架开发的汽车用户问题管理系统。该系统旨在提高用户问题响应速度，通过自动分发机制将用户提交的问题及时分配给相关部门处理。

### ✨ 主要特性

- 用户问题提交与管理
- 工程师问题处理与追踪
- 邮件通知系统
- 问题状态实时更新
- 多角色权限管理
- CSV数据存储

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Flask 2.0+
- Git

### 安装步骤

1. 克隆项目
```bash
git clone git@github.com:ljw8947/AnswerCustomer.git
cd AnswerCustomer
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

5. 运行应用
```bash
flask run
```

访问 http://localhost:5000 即可使用系统。

## 🏗️ 系统架构

### 目录结构
```
AnswerCustomer/
├── app/
│   ├── __init__.py
│   ├── models/          # 数据模型
│   ├── routes/          # 路由处理
│   ├── templates/       # HTML模板
│   ├── static/         # 静态文件
│   └── utils/          # 工具函数
├── data/               # CSV数据文件
├── tests/             # 测试文件
├── config.py          # 配置文件
├── requirements.txt   # 依赖管理
└── README.md         # 项目文档
```

### 功能模块

#### 1. 管理员模块
- 用户管理：查看、过滤、搜索用户信息
- 问题管理：查看、过滤、搜索问题列表
- 系统配置：设置问题类型、输入限制等

#### 2. 用户模块
- 用户注册与登录
- 个人信息管理
- 问题提交与管理
- 问题状态追踪

#### 3. 工程师模块
- 用户注册与登录
- 个人信息管理
- 问题处理与更新
- 问题关注与追踪

## 🔧 开发指南

### 代码规范

- 使用 Black 进行代码格式化
- 遵循 PEP 8 规范
- 使用 Pylint 进行代码检查
- 使用 Flake8 进行代码风格检查
- 使用 MyPy 进行类型检查

### 开发工具

- **代码质量工具**
  - Black: 代码格式化
  - Pylint: 代码检查
  - Flake8: 代码风格检查
  - MyPy: 类型检查
  - Coverage: 测试覆盖率

- **开发环境**
  - Python 3.8+
  - Flask 2.0+
  - Virtual Environment
  - Git 版本控制

### 测试

运行测试：
```bash
pytest
```

查看测试覆盖率：
```bash
pytest --cov=app tests/
```

## 🔒 安全规范

- 所有用户输入必须进行验证和转义
- 使用 Flask-WTF 进行表单验证
- 实现 CSRF 保护
- 密码加密存储
- 会话管理
- 请求频率限制

## 📚 文档

- [API文档](docs/api.md)
- [部署指南](docs/deployment.md)
- [开发指南](docs/development.md)
- [用户手册](docs/user-manual.md)

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- ljw8947 - 初始工作 - [GitHub](https://github.com/ljw8947)

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- 其他使用的开源项目

## 📞 联系方式

- 项目链接：[https://github.com/ljw8947/AnswerCustomer](https://github.com/ljw8947/AnswerCustomer)
- 邮箱：ljw8947@gmail.com

---

如果这个项目对你有帮助，欢迎给一个 ⭐️ 