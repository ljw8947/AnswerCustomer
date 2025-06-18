# AnswerCustomer

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 项目目的

AnswerCustomer 是一个专为汽车行业设计的用户问题管理系统，旨在提高客户问题响应效率和服务质量。系统通过自动化的邮件通知机制，将用户提交的问题及时分配给相应的技术工程师，实现问题的快速处理和跟踪。

### 🎯 核心目标

- **提高响应速度**：通过自动分发机制，确保问题在最短时间内到达相关工程师
- **提升服务质量**：标准化的问题处理流程，确保每个问题都得到妥善处理
- **增强透明度**：实时的问题状态更新，让用户了解问题处理进度
- **优化资源配置**：根据问题类型和工程师专长进行智能分配

## 🛠️ 技术栈

### 后端技术
- **Python 3.7+** - 主要编程语言
- **Flask 2.0+** - Web框架
- **Flask-Login** - 用户认证管理
- **Flask-Bcrypt** - 密码加密
- **Jinja2** - 模板引擎

### 数据存储
- **CSV文件** - 轻量级数据存储
- **JSON配置** - 系统配置管理

### 前端技术
- **HTML5/CSS3** - 页面结构和样式
- **JavaScript** - 交互功能
- **Bootstrap** - 响应式UI框架

### 邮件服务
- **SMTP** - 邮件发送协议
- **支持多种邮件服务商**（163、QQ、Gmail等）

### 开发工具
- **Git** - 版本控制
- **PyInstaller** - 可执行文件生成（Windows）
- **Tkinter** - GUI界面（Windows启动器）

## 🏗️ 功能模块

### 👨‍💼 管理员模块 (`/admin`)
- **仪表盘** - 系统概览和统计信息
- **问题管理** - 查看、筛选、分页显示所有问题
- **Specific Function管理** - 管理功能分类和邮件列表
- **邮件配置** - 配置SMTP服务器和邮件发送参数
- **CSV导入** - 批量导入问题和分类数据
- **通知功能** - 手动发送邮件通知给相关人员

### 🔧 工程师模块 (`/engineer`)
- **仪表盘** - 个人工作概览
- **问题列表** - 查看分配给自己的问题
- **问题处理** - 更新问题状态和处理进度
- **问题详情** - 查看问题详细信息和历史记录
- **评论功能** - 添加处理备注和状态变更记录

### 🔐 认证模块 (`/auth`)
- **登录功能** - 支持管理员和工程师登录
- **注册功能** - 工程师账号注册
- **密码管理** - 安全的密码存储和验证

### 📊 数据管理
- **CSV数据存储** - 使用CSV文件存储问题、用户、分类等数据
- **自动备份** - 数据文件的自动备份机制
- **数据导入导出** - 支持批量数据操作

## 📚 详细文档

- **[文档索引](DOCS.md)** - 所有文档的快速导航和索引
- **[系统架构](ARCHITECTURE.md)** - 详细的技术架构说明
- **[快速启动指南](QUICK_START.md)** - 跨平台快速启动说明
- **[Windows设置指南](WINDOWS_SETUP.md)** - Windows系统详细配置
- **[macOS设置指南](MACOS_SETUP.md)** - macOS系统详细配置
- **[邮件配置指南](EMAIL_CONFIG_GUIDE.md)** - 邮件服务配置说明
- **[CSV导入指南](CSV_IMPORT_GUIDE.md)** - 数据导入格式说明
- **[更新日志](CHANGELOG.md)** - 版本更新记录

## 🔧 开发指南

### 项目结构
```
AnswerCustomer/
├── app/                    # 应用核心
│   ├── __init__.py        # 应用初始化
│   ├── models/            # 数据模型
│   ├── routes/            # 路由处理
│   ├── templates/         # HTML模板
│   ├── static/           # 静态文件
│   └── utils/            # 工具函数
├── data/                 # 数据文件
├── tests/               # 测试文件
├── config.py            # 配置文件
├── run.py              # 启动脚本
├── requirements.txt    # 依赖管理
└── 各种启动脚本        # 跨平台启动支持
```

### 开发环境设置
```bash
# 克隆项目
git clone <repository-url>
cd AnswerCustomer

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python run.py
```

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情



---

如果这个项目对你有帮助，欢迎给一个 ⭐️ 