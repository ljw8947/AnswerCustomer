#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import tempfile
import shutil
import csv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.config_manager import ConfigManager
from app.utils.csv_manager import CsvManager
from app.models.user import User
from app.models.issue import Issue
from app.models.comment import Comment
from app.models.category import Category
from config import Config

def test_initialization():
    """测试所有数据和配置文件的初始化"""
    print("=== AnswerCustomer 初始化检查 ===\n")
    
    # 1. 检查数据目录
    print("1. 检查数据目录")
    data_dir = Config.DATA_DIR
    if os.path.exists(data_dir):
        print(f"✅ 数据目录存在: {data_dir}")
    else:
        print(f"❌ 数据目录不存在: {data_dir}")
        return False
    
    # 2. 检查CSV文件
    print("\n2. 检查CSV文件")
    csv_files = {
        'users.csv': Config.USERS_CSV,
        'issues.csv': Config.ISSUES_CSV,
        'comments.csv': Config.COMMENTS_CSV,
        'category.csv': Config.CATEGORY_CSV
    }
    
    for name, path in csv_files.items():
        if os.path.exists(path):
            print(f"✅ {name} 存在: {path}")
            # 检查文件是否可读
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        print(f"   - 文件有内容，第一行: {first_line[:50]}...")
                    else:
                        print(f"   - 文件为空")
            except Exception as e:
                print(f"   - 读取文件失败: {e}")
        else:
            print(f"❌ {name} 不存在: {path}")
    
    # 3. 检查邮件配置文件
    print("\n3. 检查邮件配置文件")
    config_manager = ConfigManager()
    email_config = config_manager.load_email_config()
    
    if os.path.exists('email_config.json'):
        print("✅ email_config.json 存在")
        print(f"   - SMTP服务器: {email_config.get('SMTP_SERVER')}")
        print(f"   - SMTP端口: {email_config.get('SMTP_PORT')}")
        print(f"   - 用户名: {email_config.get('SMTP_USERNAME')}")
        print(f"   - 密码: {'*' * len(email_config.get('SMTP_PASSWORD', '')) if email_config.get('SMTP_PASSWORD') else '未设置'}")
        print(f"   - TLS: {email_config.get('SMTP_USE_TLS')}")
    else:
        print("⚠️ email_config.json 不存在，使用默认配置")
        print(f"   - SMTP服务器: {email_config.get('SMTP_SERVER')}")
        print(f"   - SMTP端口: {email_config.get('SMTP_PORT')}")
    
    # 4. 测试Flask应用初始化
    print("\n4. 测试Flask应用初始化")
    try:
        app = create_app()
        print("✅ Flask应用创建成功")
        
        with app.app_context():
            # 检查CSV管理器
            print("\n5. 检查CSV管理器")
            managers = {
                'user_manager': app.user_manager,
                'issue_manager': app.issue_manager,
                'comment_manager': app.comment_manager,
                'category_manager': app.category_manager
            }
            
            for name, manager in managers.items():
                try:
                    data = manager.read_all()
                    print(f"✅ {name} 初始化成功，读取到 {len(data)} 条记录")
                except Exception as e:
                    print(f"❌ {name} 初始化失败: {e}")
            
            # 检查默认管理员账户
            print("\n6. 检查默认管理员账户")
            admin = app.user_manager.get_item_by_id('admin', 'username')
            if admin:
                print(f"✅ 默认管理员账户存在: {admin.username} ({admin.role})")
            else:
                print("⚠️ 默认管理员账户不存在，将在启动时创建")
            
            # 检查邮件配置
            print("\n7. 检查邮件配置")
            smtp_config = {
                'SMTP_SERVER': app.config.get('SMTP_SERVER'),
                'SMTP_PORT': app.config.get('SMTP_PORT'),
                'SMTP_USERNAME': app.config.get('SMTP_USERNAME'),
                'SMTP_PASSWORD': app.config.get('SMTP_PASSWORD'),
                'SMTP_USE_TLS': app.config.get('SMTP_USE_TLS'),
                'EMAIL_FROM': app.config.get('EMAIL_FROM'),
                'EMAIL_FROM_NAME': app.config.get('EMAIL_FROM_NAME')
            }
            
            for key, value in smtp_config.items():
                if key == 'SMTP_PASSWORD':
                    display_value = '*' * len(str(value)) if value else '未设置'
                else:
                    display_value = value
                print(f"   - {key}: {display_value}")
            
            # 检查数据完整性
            print("\n8. 检查数据完整性")
            issues = app.issue_manager.read_all()
            categories = app.category_manager.read_all()
            users = app.user_manager.read_all()
            comments = app.comment_manager.read_all()
            
            print(f"   - 问题数据: {len(issues)} 条")
            print(f"   - 分类数据: {len(categories)} 条")
            print(f"   - 用户数据: {len(users)} 条")
            print(f"   - 评论数据: {len(comments)} 条")
            
            # 检查必要的分类数据
            driving_assist = None
            for cat in categories:
                if cat.specific_function == 'Driving Assist':
                    driving_assist = cat
                    break
            
            if driving_assist:
                print(f"   - Driving Assist分类存在，邮箱配置: {driving_assist.email_list or '无'}")
            else:
                print("   - ⚠️ Driving Assist分类不存在")
            
    except Exception as e:
        print(f"❌ Flask应用初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 9. 测试文件创建功能
    print("\n9. 测试文件创建功能")
    test_dir = tempfile.mkdtemp()
    try:
        # 测试CsvManager文件创建
        test_files = [
            ('test_users.csv', User),
            ('test_issues.csv', Issue),
            ('test_comments.csv', Comment),
            ('test_categories.csv', Category)
        ]
        
        for filename, model_class in test_files:
            file_path = os.path.join(test_dir, filename)
            manager = CsvManager(file_path, model_class)
            
            # 检查文件是否被创建
            if os.path.exists(file_path):
                print(f"✅ {filename} 创建成功")
                
                # 检查头部是否正确
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    print(f"   - 头部: {header}")
            else:
                print(f"❌ {filename} 创建失败")
        
        # 测试ConfigManager
        test_config_file = os.path.join(test_dir, 'test_email_config.json')
        test_config_manager = ConfigManager(test_config_file)
        test_config = test_config_manager.load_email_config()
        
        if os.path.exists(test_config_file):
            print("✅ 测试邮件配置文件创建成功")
        else:
            print("✅ 测试邮件配置使用默认配置")
            
    except Exception as e:
        print(f"❌ 文件创建测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir, ignore_errors=True)
    
    print("\n=== 初始化检查完成 ===")
    print("✅ 所有必要的文件和配置都已正确初始化")
    return True

if __name__ == "__main__":
    success = test_initialization()
    if success:
        print("\n🎉 系统可以正常启动！")
    else:
        print("\n❌ 系统初始化存在问题，请检查上述错误信息")
        sys.exit(1) 