#!/usr/bin/env python3
"""
测试邮件配置
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.email_notifier import EmailNotifier
from config import Config

def test_email_config():
    """测试邮件配置是否正确"""
    
    print("=== 邮件配置测试 ===")
    print()
    
    # 检查配置
    print("当前邮件配置:")
    print(f"SMTP服务器: {Config.SMTP_SERVER}")
    print(f"SMTP端口: {Config.SMTP_PORT}")
    print(f"用户名: {Config.SMTP_USERNAME}")
    print(f"使用TLS: {Config.SMTP_USE_TLS}")
    print(f"发件人: {Config.EMAIL_FROM}")
    print()
    
    # 检查是否使用了默认配置
    if Config.SMTP_USERNAME == 'your-email@gmail.com':
        print("⚠️  警告: 仍在使用默认配置，请先配置邮件设置")
        print("请参考 EMAIL_CONFIG_GUIDE.md 进行配置")
        return False
    
    # 创建邮件通知器
    try:
        email_notifier = EmailNotifier(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            username=Config.SMTP_USERNAME,
            password=Config.SMTP_PASSWORD,
            use_tls=Config.SMTP_USE_TLS
        )
        print("✓ 邮件通知器创建成功")
    except Exception as e:
        print(f"✗ 邮件通知器创建失败: {str(e)}")
        return False
    
    # 测试邮件发送
    print()
    print("是否要发送测试邮件？(y/n): ", end="")
    choice = input().strip().lower()
    
    if choice == 'y':
        test_email = input("请输入测试邮箱地址: ").strip()
        if not test_email:
            print("未输入邮箱地址，跳过测试邮件发送")
            return True
        
        # 创建测试数据
        test_issues = [{
            'global_id': 999,
            'carline': 'Test Car',
            'function_domain': 'Test Domain',
            'issue_type': 'Test Issue',
            'brief_issue_en': 'This is a test issue',
            'create_time': datetime.now().strftime('%Y-%m-%d'),
            'status': 'New'
        }]
        
        print(f"正在发送测试邮件到 {test_email}...")
        
        try:
            success = email_notifier.send_issue_notification(
                [test_email], 
                'Test Function', 
                test_issues, 
                f"Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            if success:
                print("✓ 测试邮件发送成功！")
                print("请检查邮箱是否收到测试邮件")
            else:
                print("✗ 测试邮件发送失败")
                return False
                
        except Exception as e:
            print(f"✗ 发送测试邮件时出错: {str(e)}")
            return False
    
    print()
    print("=== 配置检查完成 ===")
    return True

def check_environment_variables():
    """检查环境变量配置"""
    
    print("=== 环境变量检查 ===")
    print()
    
    required_vars = [
        'SMTP_SERVER',
        'SMTP_PORT', 
        'SMTP_USERNAME',
        'SMTP_PASSWORD'
    ]
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            if var == 'SMTP_PASSWORD':
                print(f"{var}: {'*' * len(value)} (已设置)")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: 未设置")
    
    print()

if __name__ == "__main__":
    check_environment_variables()
    test_email_config() 