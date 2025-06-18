# Windows 启动指南

## 🚀 快速启动

### 方法一：双击批处理脚本（推荐）
```
双击 start_windows.bat
```

### 方法二：图形界面启动器
```
双击 start_windows.pyw
```

### 方法三：创建可执行文件
```cmd
python create_windows_exe.py
双击 dist/AnswerCustomer/AnswerCustomer.exe
```

## 📋 系统要求

- Windows 10 或更高版本
- Python 3.7 或更高版本
- 确保Python已添加到PATH环境变量

## 🔧 自动功能

启动脚本会自动：
- ✅ 检查Python环境
- ✅ 安装项目依赖
- ✅ 创建数据目录
- ✅ 查找可用端口
- ✅ 启动服务器
- ✅ 打开浏览器

## 🌐 访问地址

启动成功后访问：`http://localhost:5000`

## 📚 详细文档

查看 [WINDOWS_SETUP.md](WINDOWS_SETUP.md) 获取完整设置指南。

## 🧪 测试功能

运行测试脚本验证环境：
```cmd
python test_windows_launch.py
```

## ❗ 常见问题

1. **Python未找到**：重新安装Python，勾选"Add Python to PATH"
2. **权限问题**：以管理员身份运行或放在用户目录
3. **端口占用**：脚本会自动查找可用端口
4. **防火墙**：允许程序访问网络

---

**享受使用 AnswerCustomer！** 🎉 