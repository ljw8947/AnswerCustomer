# CSV 导入功能使用指南

## 功能概述

管理员可以通过 Web 界面批量导入 CSV 文件中的问题数据。该功能专门设计用于处理 `directvoice.csv` 格式的数据，并自动添加到现有记录后面。

## 主要特性

- ✅ 支持 `directvoice.csv` 格式的 CSV 文件导入
- ✅ 自动生成批号（使用时间戳）
- ✅ 自动分配全局 ID
- ✅ 数据验证和错误处理
- ✅ 导入结果统计和反馈
- ✅ 支持中英文双语数据

## 使用方法

### 1. 访问导入页面

1. 登录管理员账户
2. 在管理员仪表盘中点击"导入 CSV"按钮
3. 或者直接访问 `/admin/import_csv` 页面

### 2. 准备 CSV 文件

CSV 文件应包含以下列（列名必须完全匹配）：

| 列名 | 说明 | 示例 |
|------|------|------|
| `create_time` | 创建时间 | 2024-09-22 |
| `Carline` | 车型 | 177, 118, 213 |
| `Power` | 动力类型 | ICE, BEV, PHEV |
| `Specific Function` | 具体功能 | Driving Assist, Remote Control |
| `Function Domain` | 功能域 | ADAS, Mme APP, Smart Cabin |
| `General Domain` | 通用域 | Software, Hardware |
| `Issue Type` | 问题类型 | User Experience Issue, New Requirement |
| `Description` | 详细描述（中文） | 360摄像头不灵敏... |
| `Description En` | 详细描述（英文） | The 360-degree camera... |
| `Brief_Issue` | 简要问题（中文） | 改进后摄像头设计 |
| `Brief_Issue_En` | 简要问题（英文） | Optimized rear camera design |

### 3. 上传并导入

1. 点击"选择文件"按钮
2. 选择符合格式要求的 CSV 文件
3. 点击"开始导入"按钮
4. 等待导入完成并查看结果

## CSV 文件格式示例

```csv
create_time,Carline,Power,Specific Function,Function Domain,General Domain,Issue Type,Description,Description En,Brief_Issue,Brief_Issue_En
2024-09-22,177,ICE,Driving Assist,ADAS,Software,User Experience Issue,360摄像头不灵敏，快要撞到了都不出来，而且打转向灯也不出来,"The 360-degree camera is not sensitive, it doesn't even respond when I'm about to collide, and it also fails to display the turn signal.",改进后摄像头设计,Optimized rear camera design
2024-09-22,118,ICE,Remote Control,Mme APP,Software,New Requirement,APP远程控制给CLA200加上远程启动和开空调功能,The APP remote control adds remote start and air conditioning turn-on functions to my CLA200.,改进空调控制功能,Enhance air conditioning control function
```

## 导入规则

### 数据验证
- 文件必须是 CSV 格式
- 必须包含所有必需的列
- 至少包含一行数据

### 数据处理
- 空行会被自动跳过
- 缺少必要字段的行会被跳过并记录错误
- 系统会自动分配新的全局 ID
- 导入的记录标记为 `admin_import`

### 批号系统
- 每次导入使用当前时间戳作为批号
- 格式：`YYYYMMDD_HHMMSS`
- 批号记录在 `extra_info` 字段中

## 导入结果

导入完成后会显示：
- ✅ 成功导入的记录数量
- ⚠️ 跳过的记录数量
- 📋 批号信息
- ❌ 错误详情（如果有）

## 错误处理

### 常见错误及解决方案

1. **文件格式错误**
   - 确保文件是 CSV 格式
   - 检查文件编码是否为 UTF-8

2. **列名不匹配**
   - 确保列名完全匹配要求
   - 注意大小写和空格

3. **数据格式错误**
   - 检查日期格式是否为 YYYY-MM-DD
   - 确保必填字段不为空

4. **编码问题**
   - 确保 CSV 文件使用 UTF-8 编码
   - 避免使用特殊字符

## 技术实现

### 核心组件
- `CsvImporter` 类：处理 CSV 导入逻辑
- `CsvManager` 类：管理 CSV 文件操作
- `Issue` 模型：数据模型定义

### 导入流程
1. 文件上传和格式验证
2. CSV 内容解析
3. 数据映射和转换
4. 批量保存到数据库
5. 结果统计和反馈

### 安全特性
- 文件类型验证
- 数据格式验证
- 错误处理和日志记录
- 事务性导入（避免部分导入）

## 注意事项

1. **数据备份**：导入前建议备份现有数据
2. **文件大小**：建议单次导入不超过 1000 条记录
3. **网络稳定**：确保上传过程中网络稳定
4. **权限检查**：只有管理员可以执行导入操作

## 故障排除

如果遇到导入问题：

1. 检查 CSV 文件格式是否正确
2. 查看浏览器控制台的错误信息
3. 检查服务器日志
4. 尝试使用较小的测试文件

## 联系支持

如果遇到技术问题，请联系系统管理员或查看系统日志获取详细信息。 