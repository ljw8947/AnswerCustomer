# macOS 启动设置指南

## 🍎 macOS 用户专用指南

### 方法一：双击应用程序包（最简单）

1. **直接双击** `AnswerCustomer.app` 文件
2. 系统会自动打开终端并启动服务
3. 在浏览器中访问 `http://localhost:5000`

### 方法二：使用.command文件

1. **双击** `start_mac.command` 文件
2. 系统会打开终端并运行启动脚本
3. 自动安装依赖并启动服务

### 方法三：使用终端

1. 打开终端应用
2. 导航到项目目录：
   ```bash
   cd /path/to/AnswerCustomer
   ```
3. 运行启动脚本：
   ```bash
   ./start_mac.command
   ```

## 🔧 创建自定义应用程序包

如果你想重新创建应用程序包，可以运行：

```bash
python create_mac_app.py
```

这会创建一个新的 `AnswerCustomer.app` 文件。

## 🎨 创建应用程序图标

要创建自定义图标，需要先安装Pillow：

```bash
pip install Pillow
python create_icon.py
```

## ⚠️ 常见问题解决

### 1. 安全设置阻止运行

首次运行时，macOS可能会显示安全警告：

**解决方法：**
1. 打开"系统偏好设置" > "安全性与隐私"
2. 在"通用"标签页中，点击"仍要打开"
3. 或者右键点击文件 > "打开" > "打开"

### 2. 权限不足

如果遇到权限问题：

```bash
chmod +x start_mac.command
chmod +x start.sh
chmod +x init_and_run.py
```

### 3. Python未安装

**使用Homebrew安装（推荐）：**
```bash
# 安装Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Python3
brew install python3
```

**从官网下载：**
访问 [python.org](https://www.python.org/downloads/macos/) 下载安装包

### 4. 端口被占用

脚本会自动查找可用端口，无需手动处理。

### 5. 依赖安装失败

**使用国内镜像：**
```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 📱 使用技巧

### 添加到Dock
1. 将 `AnswerCustomer.app` 拖拽到Dock
2. 以后可以直接从Dock启动

### 创建别名
1. 右键点击 `AnswerCustomer.app`
2. 选择"制作替身"
3. 将替身放在桌面或其他位置

### 设置开机启动
1. 打开"系统偏好设置" > "用户与群组"
2. 选择你的用户账户
3. 点击"登录项"
4. 点击"+"号，添加 `AnswerCustomer.app`

## 🎯 推荐使用方式

**对于普通用户：**
- 直接双击 `AnswerCustomer.app`

**对于开发者：**
- 使用终端运行 `./start_mac.command`

**对于高级用户：**
- 使用 `python init_and_run.py` 获得更多控制

---

**享受在macOS上使用AnswerCustomer！** 🚀 