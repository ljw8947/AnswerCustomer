# AnswerCustomer Changelog

## 2024-06-17

### Added
- 新增batch字段到Issue模型，用于记录导入批次信息
- 创建tests目录，统一管理所有测试文件
- 添加Markup导入到app/__init__.py以支持HTML标签渲染

### Changed
- 修改CSV导入逻辑：删除extra_info自动赋值，改为赋值batch字段
- 更新nl2br过滤器：使用Markup确保HTML标签正确渲染，解决评论中换行显示问题
- 重新组织项目结构：将所有测试文件移动到tests目录

### Fixed
- 修复评论中<br>标记显示为文本而非HTML标签的问题
- 修复导入时extra_info字段被错误赋值的问题

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