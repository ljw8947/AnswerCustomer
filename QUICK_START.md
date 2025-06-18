# AnswerCustomer 快速启动指南

## 🚀 一键启动

AnswerCustomer 提供了跨平台的启动脚本，支持自动安装依赖并启动服务。

### Windows 用户

#### 方法一：双击批处理脚本（推荐）
1. **双击运行** `start_windows.bat` 文件
2. 脚本会自动处理所有依赖并启动服务

#### 方法二：图形界面启动器
1. **双击运行** `start_windows.pyw` 文件
2. 在图形界面中点击"启动服务"
3. 等待启动完成，程序会自动打开浏览器

#### 方法三：创建可执行文件
1. 运行可执行文件生成器：
   ```cmd
   python create_windows_exe.py
   ```
2. 双击生成的 `dist/AnswerCustomer/AnswerCustomer.exe` 启动

#### 方法四：命令行启动
1. 在命令提示符中运行：
   ```cmd
   start_windows.bat
   ```
2. 或者直接运行Python脚本：
   ```cmd
   python init_and_run.py
   ```

### macOS 用户

#### 方法一：双击应用程序（推荐）
1. **双击运行** `AnswerCustomer.app` 应用程序包
2. 这是最简单的方式，会自动处理所有依赖

#### 方法二：使用.command文件
1. **双击运行** `start_mac.command` 文件
2. 或者在终端中运行：
   ```bash
   ./start_mac.command
   ```

#### 方法三：使用shell脚本
1. 在终端中运行：
   ```bash
   ./start.sh
   ```

### Linux 用户

1. **双击运行** `start.sh` 文件（如果支持）
2. 或者在终端中运行：
   ```bash
   ./start.sh
   ```

### 直接使用Python脚本

如果上述方法不可用，可以直接运行Python脚本：

```bash
python init_and_run.py
```

## 📋 系统要求

- **Python**: 3.7 或更高版本
- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **网络**: 需要网络连接来下载依赖包

## 🔧 自动完成的操作

启动脚本会自动执行以下操作：

1. ✅ **检查Python版本** - 确保版本兼容
2. ✅ **检查pip** - 确保包管理器可用
3. ✅ **升级pip** - 获取最新版本
4. ✅ **安装依赖** - 从requirements.txt安装所有包
5. ✅ **创建数据目录** - 创建必要的文件夹结构
6. ✅ **检查端口** - 自动查找可用端口
7. ✅ **启动服务器** - 启动Flask应用

## 🌐 访问应用

启动成功后，在浏览器中访问：

```
http://localhost:5000
```

如果5000端口被占用，脚本会自动选择其他端口（如5001、5002等）。

## 🛑 停止服务

- **Windows**: 在命令提示符中按 `Ctrl+C`，或关闭启动器窗口
- **macOS/Linux**: 在终端中按 `Ctrl+C`

## 🪟 Windows 特殊说明

### 权限问题
如果遇到权限问题，请：
1. 以管理员身份运行命令提示符
2. 或者将项目放在用户目录下

### Python环境
确保Python已正确安装并添加到PATH：
1. 重新安装Python，勾选"Add Python to PATH"
2. 或在系统环境变量中手动添加Python路径

### 防火墙设置
首次运行时，Windows防火墙可能会询问是否允许程序访问网络，请选择"允许"。

### 创建可执行文件
如果需要创建独立的可执行文件：
```cmd
python create_windows_exe.py
```

## 🍎 macOS 特殊说明

### 创建应用程序包
如果你想重新创建macOS应用程序包，可以运行：
```bash
python create_mac_app.py
```

### 权限问题
如果遇到权限问题，请确保脚本有执行权限：
```bash
chmod +x start.sh
chmod +x start_mac.command
chmod +x init_and_run.py
```

### 安全设置
首次运行时，macOS可能会阻止运行。解决方法：
1. 打开"系统偏好设置" > "安全性与隐私"
2. 点击"仍要打开"或"允许"

## ❗ 常见问题

### Python未安装
- **Windows**: 从 [python.org](https://www.python.org/downloads/) 下载安装
- **macOS**: 使用 `brew install python3`
- **Ubuntu**: 使用 `sudo apt-get install python3 python3-pip`

### 端口被占用
脚本会自动查找可用端口，无需手动处理。

### 依赖安装失败
- 检查网络连接
- 尝试使用国内镜像源：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```

### 权限问题（Linux/macOS）
确保脚本有执行权限：
```bash
chmod +x start.sh
chmod +x start_mac.command
chmod +x init_and_run.py
```

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本是否符合要求
2. 网络连接是否正常
3. 端口是否被其他程序占用
4. 系统权限是否足够

## 📚 详细文档

- **Windows用户**: 查看 [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **macOS用户**: 查看 [MACOS_SETUP.md](MACOS_SETUP.md)

---

**享受使用 AnswerCustomer！** 🎉 