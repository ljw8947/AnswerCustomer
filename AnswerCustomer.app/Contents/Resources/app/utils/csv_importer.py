import csv
import io
from datetime import datetime
from typing import Dict, List
from app.models.issue import Issue
from app.utils.email_notifier import EmailNotifier

class CsvImporter:
    """CSV 导入工具，专门处理 directvoice.csv 格式的数据"""
    
    @staticmethod
    def import_from_directvoice_format(csv_content, issue_manager, category_manager=None, 
                                      email_notifier=None, batch_id=None):
        """
        从 directvoice.csv 格式导入数据，并发送邮件通知
        
        Args:
            csv_content: CSV 文件内容（字符串）
            issue_manager: 问题管理器实例
            category_manager: 分类管理器实例（用于获取邮箱配置）
            email_notifier: 邮件通知器实例
            batch_id: 批号标识，如果为 None 则自动生成
            
        Returns:
            dict: 包含导入结果的字典
        """
        if batch_id is None:
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 读取现有问题以获取最大 issue_id（纯数字）
        existing_issues = issue_manager.read_all()
        max_issue_id = 0  # 从0开始，如果没有现有数据则从1开始
        for issue in existing_issues:
            try:
                iid = int(issue.issue_id)
                if iid > max_issue_id:
                    max_issue_id = iid
            except Exception:
                continue
        
        # 递增 global_id 逻辑保留（兼容性）
        max_global_id = 0
        if existing_issues:
            for issue in existing_issues:
                if issue.global_id is not None:
                    max_global_id = max(max_global_id, issue.global_id)
        
        # 解析 CSV 内容
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        imported_count = 0
        skipped_count = 0
        errors = []
        notification_results = []
        
        # 用于按 specific_function 分组的问题
        issues_by_function: Dict[str, List[Issue]] = {}
        
        for row_num, row in enumerate(csv_reader, start=2):  # 从第2行开始（跳过标题行）
            try:
                # 映射 directvoice.csv 的列名到 Issue 模型字段
                # 处理可能的 BOM 字符
                create_time = row.get('create_time') or row.get('\ufeffcreate_time', datetime.now().strftime("%Y-%m-%d"))
                carline = row.get('Carline', '')
                power = row.get('Power', '')
                specific_function = row.get('Specific Function', '')
                function_domain = row.get('Function Domain', '')
                general_domain = row.get('General Domain', '')
                issue_type = row.get('Issue Type', '')
                description = row.get('Description', '')
                description_en = row.get('Description En', '')
                brief_issue = row.get('Brief_Issue', '')
                brief_issue_en = row.get('Brief_Issue_En', '')
                
                # 跳过空行
                if not brief_issue and not description:
                    skipped_count += 1
                    continue
                
                # 验证必要字段
                if not carline and not specific_function:
                    errors.append(f"第 {row_num} 行: 缺少必要字段 (车型或具体功能)")
                    skipped_count += 1
                    continue
                
                # 递增 global_id
                max_global_id += 1
                # 递增 issue_id（纯数字字符串）
                max_issue_id += 1
                
                # 创建新的 Issue 实例
                new_issue = Issue(
                    issue_id=str(max_issue_id),
                    create_time=create_time,
                    carline=carline,
                    power=power,
                    specific_function=specific_function,
                    function_domain=function_domain,
                    general_domain=general_domain,
                    issue_type=issue_type,
                    description=description,
                    description_en=description_en,
                    brief_issue=brief_issue,
                    brief_issue_en=brief_issue_en,
                    global_id=max_global_id,
                    user_issue_id=1,
                    created_by_user_id='admin_import',
                    status='New',
                    notified=0,
                    batch=batch_id
                )
                
                # 添加到问题管理器
                issue_manager.add_item(new_issue)
                imported_count += 1
                
                # 按 specific_function 分组
                if specific_function:
                    if specific_function not in issues_by_function:
                        issues_by_function[specific_function] = []
                    issues_by_function[specific_function].append(new_issue)
                
            except Exception as e:
                errors.append(f"第 {row_num} 行: {str(e)}")
                skipped_count += 1
                continue
        
        # 发送邮件通知
        if category_manager and email_notifier and issues_by_function:
            notification_results = CsvImporter._send_notifications(
                issues_by_function, category_manager, email_notifier, batch_id, issue_manager
            )
        
        return {
            'imported_count': imported_count,
            'skipped_count': skipped_count,
            'errors': errors,
            'batch_id': batch_id,
            'notification_results': notification_results
        }
    
    @staticmethod
    def _send_notifications(issues_by_function: Dict[str, List[Issue]], 
                           category_manager, email_notifier: EmailNotifier, 
                           batch_id: str, issue_manager):
        """
        为每个 specific_function 发送邮件通知
        
        Args:
            issues_by_function: 按 specific_function 分组的问题
            category_manager: 分类管理器
            email_notifier: 邮件通知器
            batch_id: 批号
            issue_manager: 问题管理器（用于更新通知状态）
            
        Returns:
            list: 通知结果列表
        """
        notification_results = []
        
        # 获取所有分类配置
        all_categories = category_manager.read_all()
        category_map = {cat.specific_function: cat for cat in all_categories}
        
        for specific_function, issues in issues_by_function.items():
            try:
                # 查找对应的分类配置
                category = category_map.get(specific_function)
                if not category or not category.email_list:
                    notification_results.append({
                        'specific_function': specific_function,
                        'status': 'skipped',
                        'reason': 'No email configuration found'
                    })
                    continue
                
                # 获取邮箱列表
                emails = category.email_list.split(',') if category.email_list else []
                emails = [email.strip() for email in emails if email.strip()]
                
                if not emails:
                    notification_results.append({
                        'specific_function': specific_function,
                        'status': 'skipped',
                        'reason': 'No valid email addresses'
                    })
                    continue
                
                # 转换问题为字典格式
                issues_dict = [issue.to_dict() for issue in issues]
                
                # 发送邮件通知
                success = email_notifier.send_issue_notification(
                    emails, specific_function, issues_dict, batch_id
                )
                
                if success:
                    # 更新所有问题的通知状态
                    for issue in issues:
                        issue.notified = 1
                        issue_manager.update_item(issue.issue_id, issue, 'issue_id')
                    
                    notification_results.append({
                        'specific_function': specific_function,
                        'status': 'success',
                        'recipients': emails,
                        'issue_count': len(issues)
                    })
                else:
                    notification_results.append({
                        'specific_function': specific_function,
                        'status': 'failed',
                        'reason': 'Email sending failed'
                    })
                    
            except Exception as e:
                notification_results.append({
                    'specific_function': specific_function,
                    'status': 'error',
                    'reason': str(e)
                })
        
        return notification_results
    
    @staticmethod
    def _clean_column_name(column_name):
        """
        清理列名，移除 BOM 字符和多余的空格
        
        Args:
            column_name: 原始列名
            
        Returns:
            str: 清理后的列名
        """
        if column_name is None:
            return None
        # 移除 BOM 字符和多余的空格
        return column_name.replace('\ufeff', '').strip()
    
    @staticmethod
    def validate_csv_format(csv_content):
        """
        验证 CSV 文件格式是否符合 directvoice.csv 的要求
        
        Args:
            csv_content: CSV 文件内容（字符串）
            
        Returns:
            dict: 包含验证结果的字典
        """
        try:
            # 创建两个独立的 CSV 读取器，一个用于验证列名，一个用于计算行数
            csv_reader_columns = csv.DictReader(io.StringIO(csv_content))
            csv_reader_rows = csv.DictReader(io.StringIO(csv_content))
            
            required_columns = [
                'create_time', 'Carline', 'Power', 'Specific Function',
                'Function Domain', 'General Domain', 'Issue Type',
                'Description', 'Description En', 'Brief_Issue', 'Brief_Issue_En'
            ]
            
            # 检查列名
            actual_columns = csv_reader_columns.fieldnames
            if actual_columns is None:
                return {
                    'valid': False,
                    'message': '无法读取 CSV 列名，请检查文件格式'
                }
            
            # 清理列名（移除 BOM 字符）
            cleaned_actual_columns = [CsvImporter._clean_column_name(col) for col in actual_columns]
            
            missing_columns = [col for col in required_columns if col not in cleaned_actual_columns]
            
            if missing_columns:
                return {
                    'valid': False,
                    'message': f'缺少必要的列: {", ".join(missing_columns)}',
                    'actual_columns': actual_columns,
                    'cleaned_columns': cleaned_actual_columns
                }
            
            # 检查是否有数据行
            rows = list(csv_reader_rows)
            if not rows:
                return {
                    'valid': False,
                    'message': 'CSV 文件没有数据行'
                }
            
            return {
                'valid': True,
                'message': f'CSV 格式验证通过，包含 {len(rows)} 行数据',
                'row_count': len(rows)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'CSV 格式验证失败: {str(e)}'
            } 