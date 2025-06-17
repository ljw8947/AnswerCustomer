#!/usr/bin/env python3
"""
测试邮件配置管理功能
"""

import os
import sys
import json
import tempfile
import shutil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.config_manager import ConfigManager

def test_config_manager():
    """测试配置管理器功能"""
    
    print("=== 测试邮件配置管理功能 ===")
    print()
    
    # 创建临时配置文件
    temp_dir = tempfile.mkdtemp()
    config_file = os.path.join(temp_dir, 'test_email_config.json')
    
    try:
        # 创建配置管理器
        config_manager = ConfigManager(config_file)
        
        # 测试1: 加载默认配置
        print("1. 测试加载默认配置...")
        default_config = config_manager.load_email_config()
        expected_keys = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 
                        'EMAIL_FROM', 'EMAIL_FROM_NAME', 'SMTP_USE_TLS']
        
        for key in expected_keys:
            if key in default_config:
                print(f"   ✓ {key}: {default_config[key]}")
            else:
                print(f"   ✗ 缺少 {key}")
                return False
        
        # 测试2: 保存配置
        print("\n2. 测试保存配置...")
        test_config = {
            'SMTP_SERVER': 'smtp.test.com',
            'SMTP_PORT': 587,
            'SMTP_USERNAME': 'test@example.com',
            'SMTP_PASSWORD': 'test_password',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_FROM_NAME': 'Test System',
            'SMTP_USE_TLS': True
        }
        
        if config_manager.save_email_config(test_config):
            print("   ✓ 配置保存成功")
        else:
            print("   ✗ 配置保存失败")
            return False
        
        # 测试3: 重新加载配置
        print("\n3. 测试重新加载配置...")
        loaded_config = config_manager.load_email_config()
        
        for key, expected_value in test_config.items():
            if loaded_config.get(key) == expected_value:
                print(f"   ✓ {key}: {loaded_config[key]}")
            else:
                print(f"   ✗ {key}: 期望 {expected_value}, 实际 {loaded_config.get(key)}")
                return False
        
        # 测试4: 更新配置
        print("\n4. 测试更新配置...")
        updates = {
            'SMTP_SERVER': 'smtp.updated.com',
            'SMTP_PORT': 465
        }
        
        if config_manager.update_config(updates):
            print("   ✓ 配置更新成功")
        else:
            print("   ✗ 配置更新失败")
            return False
        
        # 验证更新结果
        updated_config = config_manager.load_email_config()
        if updated_config['SMTP_SERVER'] == 'smtp.updated.com' and updated_config['SMTP_PORT'] == 465:
            print("   ✓ 更新验证成功")
        else:
            print("   ✗ 更新验证失败")
            return False
        
        # 测试5: 检查配置文件内容
        print("\n5. 检查配置文件内容...")
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                file_content = json.load(f)
                print(f"   ✓ 配置文件存在，包含 {len(file_content)} 个配置项")
                for key, value in file_content.items():
                    if key == 'SMTP_PASSWORD':
                        print(f"     {key}: {'*' * len(str(value))}")
                    else:
                        print(f"     {key}: {value}")
        else:
            print("   ✗ 配置文件不存在")
            return False
        
        print("\n=== 所有测试通过！ ===")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试过程中发生错误: {str(e)}")
        return False
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"\n清理临时文件: {temp_dir}")

def test_config_file_format():
    """测试配置文件格式"""
    
    print("\n=== 测试配置文件格式 ===")
    print()
    
    # 创建临时配置文件
    temp_dir = tempfile.mkdtemp()
    config_file = os.path.join(temp_dir, 'format_test.json')
    
    try:
        config_manager = ConfigManager(config_file)
        
        # 创建测试配置
        test_config = {
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': 587,
            'SMTP_USERNAME': 'user@gmail.com',
            'SMTP_PASSWORD': 'app_password_123',
            'EMAIL_FROM': 'user@gmail.com',
            'EMAIL_FROM_NAME': 'AnswerCustomer System',
            'SMTP_USE_TLS': True
        }
        
        # 保存配置
        config_manager.save_email_config(test_config)
        
        # 检查文件格式
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            parsed = json.loads(content)
            
            print("配置文件格式检查:")
            print(f"  - 文件大小: {len(content)} 字符")
            print(f"  - JSON格式: {'✓ 有效' if isinstance(parsed, dict) else '✗ 无效'}")
            print(f"  - 配置项数量: {len(parsed)}")
            print(f"  - 编码: UTF-8")
            
            # 检查是否包含敏感信息
            if 'app_password_123' in content:
                print("  - 安全警告: 密码以明文形式存储")
            else:
                print("  - 安全: 密码已加密或隐藏")
        
        return True
        
    except Exception as e:
        print(f"✗ 格式测试失败: {str(e)}")
        return False
        
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    success1 = test_config_manager()
    success2 = test_config_file_format()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！邮件配置管理功能正常工作。")
    else:
        print("\n❌ 部分测试失败，请检查配置管理功能。") 