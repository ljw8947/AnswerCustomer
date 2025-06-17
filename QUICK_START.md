# AnswerCustomer 快速启动指南

## 🚀 一键启动

AnswerCustomer 提供了跨平台的启动脚本，支持自动安装依赖并启动服务。

### Windows 用户

1. **双击运行** `start.bat` 文件
2. 或者在命令提示符中运行：
   ```cmd
   start.bat
   ```

### macOS/Linux 用户

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

在终端中按 `Ctrl+C` 停止服务器。

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
chmod +x init_and_run.py
```

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本是否符合要求
2. 网络连接是否正常
3. 端口是否被其他程序占用
4. 系统权限是否足够

---

**享受使用 AnswerCustomer！** 🎉 