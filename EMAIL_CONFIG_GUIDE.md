# 邮件配置指南

本文档说明如何配置AnswerCustomer系统的邮件发送功能。

## 配置方法

### 方法1：Web界面配置（推荐）

1. 登录管理员账户
2. 进入"邮件配置管理"页面
3. 填写SMTP服务器配置信息
4. 点击"保存配置"按钮
5. 点击"测试配置"按钮验证配置是否正确

### 方法2：环境变量配置

在系统环境变量中设置以下参数：

```bash
# SMTP服务器配置
export SMTP_SERVER=smtp.163.com
export SMTP_PORT=25
export SMTP_USERNAME=your-email@163.com
export SMTP_PASSWORD=your-authorization-code
export SMTP_USE_TLS=false

# 发件人信息
export EMAIL_FROM=your-email@163.com
export EMAIL_FROM_NAME=AnswerCustomer System
```

### 方法3：直接修改config.py

在`config.py`文件中直接修改以下配置：

```python
# Email Configuration
SMTP_SERVER = 'smtp.163.com'  # 邮件服务器地址
SMTP_PORT = 25                # 端口号
SMTP_USERNAME = 'your-email@163.com'  # 邮箱用户名
SMTP_PASSWORD = 'your-authorization-code'     # 邮箱密码
SMTP_USE_TLS = False             # 是否使用TLS加密
EMAIL_FROM = 'your-email@163.com'     # 发件人邮箱
EMAIL_FROM_NAME = 'AnswerCustomer System'  # 发件人名称
```

## 配置参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| SMTP_SERVER | SMTP服务器地址 | smtp.163.com |
| SMTP_PORT | SMTP端口号 | 25, 587, 465 |
| SMTP_USERNAME | 邮箱用户名 | your-email@163.com |
| SMTP_PASSWORD | 邮箱密码/授权码 | 应用专用密码或授权码 |
| SMTP_USE_TLS | 是否使用TLS加密 | true/false |
| EMAIL_FROM | 发件人邮箱 | your-email@163.com |
| EMAIL_FROM_NAME | 发件人名称 | AnswerCustomer System |

## 常用邮件服务商配置

### 163邮箱 (推荐)

**配置参数：**
- 服务器：smtp.163.com
- 端口：25
- TLS：关闭
- 密码：授权码

**获取授权码步骤：**
1. 登录163邮箱
2. 进入"设置" -> "POP3/SMTP/IMAP"
3. 开启"SMTP服务"
4. 获取授权码作为SMTP_PASSWORD

### Gmail

**配置参数：**
- 服务器：smtp.gmail.com
- 端口：587
- TLS：开启
- 密码：应用专用密码

**获取应用专用密码步骤：**
1. 登录Google账户
2. 进入"安全性"设置
3. 开启"两步验证"
4. 生成"应用专用密码"
5. 使用生成的16位密码作为SMTP_PASSWORD

### QQ邮箱

**配置参数：**
- 服务器：smtp.qq.com
- 端口：587
- TLS：开启
- 密码：授权码

**获取授权码步骤：**
1. 登录QQ邮箱
2. 进入"设置" -> "账户"
3. 开启"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 获取授权码作为SMTP_PASSWORD

### 企业邮箱

根据企业邮箱服务商的具体要求配置，通常需要联系IT部门获取SMTP设置。

## 端口和加密说明

| 端口 | 加密方式 | 说明 |
|------|----------|------|
| 25 | 无加密 | 传统SMTP端口，部分网络可能被拦截 |
| 587 | TLS | 推荐端口，支持STARTTLS加密 |
| 465 | SSL | 直接SSL连接，需要特殊处理 |

**建议配置：**
- 163邮箱：端口25 + TLS关闭，或端口587 + TLS开启
- Gmail：端口587 + TLS开启
- QQ邮箱：端口587 + TLS开启

## 测试邮件发送

### 方法1：Web界面测试

1. 在"邮件配置管理"页面填写配置
2. 点击"测试配置"按钮
3. 系统会发送测试邮件到配置的邮箱
4. 查看测试结果

### 方法2：功能测试

1. 在管理员界面导入CSV文件
2. 确保Specific Function配置了邮箱地址
3. 系统会自动发送通知邮件
4. 或使用单个问题的"发送通知"按钮

## 故障排除

### 常见错误

1. **认证失败 (535 Error)**
   - 检查用户名和密码是否正确
   - 确认是否使用了授权码而不是登录密码
   - 检查端口和TLS设置是否匹配

2. **连接超时**
   - 检查SMTP服务器地址和端口
   - 确认网络连接正常
   - 检查防火墙设置

3. **TLS错误**
   - 尝试设置SMTP_USE_TLS=false
   - 或使用SSL端口（如465）
   - 检查端口和加密方式的匹配

4. **端口被占用**
   - 检查是否有其他应用占用SMTP端口
   - 尝试使用不同的端口

### 调试步骤

1. **检查配置**
   - 确认所有必填字段都已填写
   - 验证邮箱地址格式正确
   - 检查端口号是否为数字

2. **测试连接**
   - 使用telnet测试SMTP连接
   - 检查网络连接是否正常

3. **查看日志**
   - 检查应用日志中的错误信息
   - 查看邮件发送的详细错误

## 安全建议

1. **密码安全**
   - 不要在代码中硬编码密码
   - 使用环境变量或配置文件存储敏感信息
   - 定期更换授权码

2. **邮件安全**
   - 限制邮件发送频率，避免被标记为垃圾邮件
   - 使用TLS加密提高传输安全性
   - 定期检查邮件发送日志

3. **访问控制**
   - 限制邮件配置页面的访问权限
   - 定期审查邮件发送记录

## 邮件模板

系统发送的邮件包含以下信息：
- Specific Function名称
- 批次ID
- 问题数量和详情
- 每个问题的关键信息（车型、功能域、问题类型等）

### 邮件内容示例

```
新问题通知

Specific Function: Driving Assist
批次ID: Debug_1
问题数量: 1

问题详情:

1. 问题 #1
    - 车型: 177
    - 功能域: ADAS
    - 问题类型: User Experience Issue
    - 简要描述: Optimized rear camera design
    - 创建时间: 2024-09-22
    - 状态: New

请及时处理这些问题。

此邮件由系统自动发送，请勿回复。
```

邮件内容可以通过修改`app/utils/email_notifier.py`中的`_create_email_body`方法来自定义。

## 配置优先级

系统按以下优先级加载邮件配置：

1. Web界面保存的配置（email_config.json）
2. 环境变量配置
3. config.py中的默认配置

**注意：** Web界面配置会覆盖其他配置方式，建议使用Web界面进行配置管理。 