#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有页面是否都已英文化
"""

import os
import re

def test_all_english():
    """测试所有页面是否都已英文化"""
    print("=" * 60)
    print("🔍 测试所有页面是否都已英文化")
    print("=" * 60)
    
    # 需要检查的模板文件
    templates_to_check = [
        'app/templates/base.html',
        'app/templates/main/index.html',
        'app/templates/auth/login.html',
        'app/templates/auth/register_engineer.html',
        'app/templates/admin/dashboard.html',
        'app/templates/engineer/dashboard.html',
        'app/templates/admin/issues.html',
        'app/templates/engineer/issues.html',
        'app/templates/admin/issue_detail.html',
        'app/templates/engineer/issue_detail.html',
        'app/templates/engineer/issue_process.html',
        'app/templates/admin/categories.html',
        'app/templates/admin/edit_category.html',
        'app/templates/admin/import_categories.html',
        'app/templates/admin/import_csv.html',
        'app/templates/admin/email_config.html'
    ]
    
    # 中文词汇模式
    chinese_patterns = [
        r'[\u4e00-\u9fff]+',  # 中文字符
        r'问题详情',
        r'处理问题',
        r'导入配置',
        r'邮箱列表',
        r'保存修改',
        r'返回列表',
        r'筛选条件',
        r'分页导航',
        r'邮件配置',
        r'管理员',
        r'工程师',
        r'登录',
        r'注册',
        r'退出',
        r'仪表盘',
        r'管理',
        r'查看',
        r'编辑',
        r'删除',
        r'添加',
        r'保存',
        r'取消',
        r'确认',
        r'提交',
        r'重置',
        r'搜索',
        r'筛选',
        r'排序',
        r'分页',
        r'上一页',
        r'下一页',
        r'首页',
        r'末页',
        r'共',
        r'页',
        r'条',
        r'个',
        r'无',
        r'暂无',
        r'没有找到',
        r'加载中',
        r'正在',
        r'请',
        r'点击',
        r'选择',
        r'输入',
        r'上传',
        r'下载',
        r'导出',
        r'导入',
        r'配置',
        r'设置',
        r'系统',
        r'用户',
        r'权限',
        r'角色',
        r'状态',
        r'类型',
        r'时间',
        r'日期',
        r'创建',
        r'更新',
        r'修改',
        r'删除',
        r'启用',
        r'禁用',
        r'开启',
        r'关闭',
        r'成功',
        r'失败',
        r'错误',
        r'警告',
        r'提示',
        r'信息',
        r'详情',
        r'列表',
        r'表格',
        r'表单',
        r'按钮',
        r'链接',
        r'标题',
        r'内容',
        r'描述',
        r'说明',
        r'帮助',
        r'支持',
        r'联系',
        r'关于',
        r'版本',
        r'更新日志',
        r'使用说明',
        r'操作指南',
        r'常见问题',
        r'技术支持',
        r'联系我们',
        r'隐私政策',
        r'服务条款',
        r'版权信息',
        r'免责声明'
    ]
    
    found_chinese = []
    
    for template_file in templates_to_check:
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否有中文内容
                chinese_found = []
                for pattern in chinese_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        chinese_found.extend(matches)
                
                if chinese_found:
                    found_chinese.append((template_file, chinese_found))
                    print(f"   ⚠️ {template_file} 发现中文内容: {chinese_found[:5]}...")
                else:
                    print(f"   ✅ {template_file} 已完全英文化")
            except Exception as e:
                print(f"   ❌ 读取 {template_file} 失败: {e}")
        else:
            print(f"   ❌ {template_file} 文件不存在")
    
    if found_chinese:
        print(f"\n⚠️ 发现 {len(found_chinese)} 个文件仍有中文内容:")
        for file_path, chinese_list in found_chinese:
            print(f"   - {file_path}: {chinese_list[:10]}")
    else:
        print("\n✅ 所有页面都已完全英文化！")
    
    print("\n" + "=" * 60)

def main():
    """主函数"""
    test_all_english()

if __name__ == "__main__":
    main() 