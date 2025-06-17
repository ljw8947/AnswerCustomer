# AnswerCustomer Changelog

## 2024-06-17

### Added
- 新增邮件配置管理功能
  - 添加邮件配置管理页面 (`/admin/email_config`)
  - 实现邮件配置的保存和加载功能
  - 添加邮件配置测试功能
  - 创建ConfigManager工具类管理邮件配置
  - 创建EmailNotifier工具类处理邮件发送
- 新增邮件通知功能
  - 在问题导入时自动发送邮件通知
  - 在问题列表页面添加单个问题通知功能
  - 支持按Specific Function分组发送通知
  - 添加通知状态跟踪（notified字段）
- 新增问题列表排序功能
  - 按issue_id降序排列，最新问题显示在前面
  - 支持分页显示（每页20条记录）
- 新增问题列表筛选功能
  - 支持按状态、车型、功能域、具体功能筛选
  - 动态下拉列表从category.csv数据生成
- 新增问题列表列名统一
  - 将"Global ID"列名改为"ID"
  - 统一显示issue_id字段
- 新增Specific Function管理功能
  - 添加category.csv导入功能
  - 支持编辑每个Specific Function的邮箱列表
  - 支持BOM字符处理
- 新增评论功能
  - 工程师可以在问题详情页面添加评论
  - 支持换行符显示（nl2br过滤器）
  - 状态变更自动记录为评论
- 新增batch字段到Issue模型，用于记录导入批次信息
- 创建tests目录，统一管理所有测试文件
- 添加Markup导入到app/__init__.py以支持HTML标签渲染

### Changed
- 修改CSV导入逻辑：删除extra_info自动赋值，改为赋值batch字段
- 更新nl2br过滤器：使用Markup确保HTML标签正确渲染，解决评论中换行显示问题
- 重新组织项目结构：将所有测试文件移动到tests目录
- 更新邮件配置指南文档
  - 添加Web界面配置方法说明
  - 完善常用邮件服务商配置
  - 添加端口和加密说明
  - 增强故障排除和调试步骤
  - 添加邮件内容示例
- 优化问题列表页面
  - 统一admin和engineer页面的列名和显示
  - 改进分页控件显示
  - 优化筛选表单布局
- 改进邮件发送逻辑
  - 支持163邮箱端口25+TLS关闭配置
  - 优化邮件内容格式
  - 添加错误处理和日志记录

### Fixed
- 修复评论中<br>标记显示为文本而非HTML标签的问题
- 修复导入时extra_info字段被错误赋值的问题
- 修复邮件配置页面测试功能
  - 解决邮件发送失败的错误处理
  - 修复163邮箱认证问题
- 修复问题列表页面通知功能
  - 解决邮件配置检查失败问题
  - 修复通知按钮状态管理
- 修复分页控件显示问题
  - 解决Jinja2模板中max/min函数未定义错误
- 修复路由引用错误
  - 统一engineer.issues路由引用
- 修复邮件配置优先级问题
  - Web界面配置正确覆盖默认配置

### Removed
- 移除用户相关功能
  - 删除用户注册和登录功能
  - 删除用户问题提交功能
  - 删除用户仪表盘和问题管理页面
  - 简化用户模型，仅保留认证功能
- 移除管理员参数配置页面
  - 删除config.html模板
  - 删除configure_settings路由
- 移除工程师问题处理按钮
  - 从问题列表页面移除"Process Issue"按钮
- 清理测试文件
  - 删除临时测试脚本
  - 整理tests目录结构

## 2023-10-27

### Added
- Created `.cursorrules.md` for project-specific configurations.
- Designed `Issue` data structure in `app/models/issue.py` based on provided Excel sheet.
- Generated initial `README.md` with project overview, setup, architecture, and development guidelines.

### Updated
- Refined `.cursorrules.md` content and hierarchy for better readability and organization.
- Updated GitHub repository link, author info, and contact email in `README.md`.

### Fixed
- Corrected JSON formatting issues in `.cursorrules` (before converting to `.cursorrules.md`). 