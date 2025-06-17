import csv
import os
from app.models.category import Category

class CategoryImporter:
    @staticmethod
    def import_from_original_csv(original_csv_path, category_manager):
        """从原始category.csv导入数据到新的Category格式"""
        if not os.path.exists(original_csv_path):
            print(f"原始category.csv文件不存在: {original_csv_path}")
            return False
        
        try:
            with open(original_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                imported_count = 0
                
                for row in reader:
                    # 检查是否已存在相同的specific_function
                    existing_categories = category_manager.read_all()
                    existing = None
                    for cat in existing_categories:
                        if cat.specific_function == row['Specific Function']:
                            existing = cat
                            break
                    
                    if existing:
                        # 更新现有记录
                        existing.function_domain = row['Function Domain']
                        existing.general_domain = row['General Domain']
                        category_manager.update_item(existing.category_id, existing, 'category_id')
                    else:
                        # 创建新记录
                        new_category = Category(
                            specific_function=row['Specific Function'],
                            function_domain=row['Function Domain'],
                            general_domain=row['General Domain']
                        )
                        category_manager.add_item(new_category)
                        imported_count += 1
                
                print(f"成功导入 {imported_count} 个新的Specific Function配置")
                return True
                
        except Exception as e:
            print(f"导入category.csv时发生错误: {str(e)}")
            return False
    
    @staticmethod
    def validate_email(email):
        """简单的邮箱验证"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def parse_email_list(email_string):
        """解析邮箱字符串为列表"""
        if not email_string:
            return []
        
        emails = [email.strip() for email in email_string.split(',') if email.strip()]
        valid_emails = []
        invalid_emails = []
        
        for email in emails:
            if CategoryImporter.validate_email(email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)
        
        if invalid_emails:
            print(f"发现无效邮箱: {invalid_emails}")
        
        return valid_emails 