#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试DirectVoice名称和英文界面修改
"""

import os
import sys
import subprocess
import time
import requests
from bs4 import BeautifulSoup

def test_directvoice_changes():
    """测试DirectVoice名称和英文界面修改"""
    print("=" * 60)
    print("🔍 测试DirectVoice名称和英文界面修改")
    print("=" * 60)
    
    # 测试配置文件修改
    print("\n📋 测试配置文件修改...")
    test_config_changes()
    
    # 测试模板文件修改
    print("\n📄 测试模板文件修改...")
    test_template_changes()
    
    # 测试网站运行
    print("\n🌐 测试网站运行...")
    test_website_running()
    
    print("\n✅ 所有测试完成！")

def test_config_changes():
    """测试配置文件修改"""
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'DirectVoice System' in content:
            print("   ✅ config.py中的EMAIL_FROM_NAME已更新为DirectVoice System")
        else:
            print("   ❌ config.py中的EMAIL_FROM_NAME未更新")
            
    except Exception as e:
        print(f"   ❌ 读取config.py失败: {e}")

def test_template_changes():
    """测试模板文件修改"""
    templates_to_check = [
        ('app/templates/base.html', ['DirectVoice', 'Login', 'Logout', 'Admin', 'Engineer']),
        ('app/templates/main/index.html', ['Welcome to DirectVoice', 'Automotive Issue Management System']),
        ('app/templates/auth/login.html', ['User Login', 'Username', 'Password', 'Remember me']),
        ('app/templates/auth/register_engineer.html', ['Engineer Registration', 'Employee ID']),
        ('app/templates/admin/dashboard.html', ['Welcome, Administrator!', 'Manage Issues', 'Import CSV']),
        ('app/templates/engineer/dashboard.html', ['Welcome, Engineer!', 'View Issue List']),
        ('app/templates/admin/issues.html', ['Issue Management', 'Filter Conditions', 'Status', 'Carline']),
        ('app/templates/engineer/issues.html', ['Engineer Issue List', 'Filter Conditions', 'Status', 'Carline']),
        ('app/templates/admin/email_config.html', ['Email Configuration Management', 'SMTP Server Configuration'])
    ]
    
    for template_file, expected_terms in templates_to_check:
        try:
            if os.path.exists(template_file):
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                missing_terms = []
                for term in expected_terms:
                    if term not in content:
                        missing_terms.append(term)
                
                if not missing_terms:
                    print(f"   ✅ {template_file} 已正确更新")
                else:
                    print(f"   ⚠️ {template_file} 缺少以下英文术语: {missing_terms}")
            else:
                print(f"   ❌ {template_file} 文件不存在")
                
        except Exception as e:
            print(f"   ❌ 读取 {template_file} 失败: {e}")

def test_website_running():
    """测试网站运行"""
    try:
        # 启动服务器
        print("   🚀 启动测试服务器...")
        process = subprocess.Popen([sys.executable, 'run.py', '--port', '5002'], 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(5)
        
        # 测试主页
        print("   🌐 测试主页...")
        response = requests.get('http://localhost:5002', timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查页面标题
            title = soup.find('title')
            if title and 'DirectVoice' in title.text:
                print("   ✅ 页面标题包含DirectVoice")
            else:
                print("   ❌ 页面标题未包含DirectVoice")
            
            # 检查导航栏品牌名称
            navbar_brand = soup.find('a', class_='navbar-brand')
            if navbar_brand and 'DirectVoice' in navbar_brand.text:
                print("   ✅ 导航栏品牌名称为DirectVoice")
            else:
                print("   ❌ 导航栏品牌名称不是DirectVoice")
            
            # 检查页面语言
            html_tag = soup.find('html')
            if html_tag and html_tag.get('lang') == 'en':
                print("   ✅ 页面语言设置为英文")
            else:
                print("   ❌ 页面语言未设置为英文")
            
            # 检查英文内容
            page_text = soup.get_text()
            english_terms = ['Welcome to DirectVoice', 'Login', 'Engineer Registration', 'Issue Management']
            missing_terms = []
            
            for term in english_terms:
                if term not in page_text:
                    missing_terms.append(term)
            
            if not missing_terms:
                print("   ✅ 页面包含所有预期的英文内容")
            else:
                print(f"   ⚠️ 页面缺少以下英文内容: {missing_terms}")
                
        else:
            print(f"   ❌ 主页请求失败，状态码: {response.status_code}")
        
        # 停止服务器
        process.terminate()
        process.wait()
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 网络请求失败: {e}")
    except Exception as e:
        print(f"   ❌ 测试网站运行失败: {e}")
        if 'process' in locals():
            process.terminate()

def main():
    """主函数"""
    test_directvoice_changes()

if __name__ == "__main__":
    main() 