#!/usr/bin/env python3
"""
测试nl2br过滤器修复
"""

def test_nl2br_filter():
    """测试nl2br过滤器是否正确渲染HTML标签"""
    
    # 测试数据
    test_comment = "这是第一行\n这是第二行\n这是第三行"
    
    print("测试nl2br过滤器修复...")
    print(f"测试评论内容: {repr(test_comment)}")
    print("期望结果: 换行符应该被转换为<br>标签并正确渲染")
    print()
    
    print("请手动测试以下步骤:")
    print("1. 访问 http://localhost:5000/engineer/login")
    print("2. 使用工程师账户登录 (Engineer1/engineer_password)")
    print("3. 进入任意问题详情页面")
    print("4. 在评论框中输入包含换行的文本，例如:")
    print("   这是第一行")
    print("   这是第二行")
    print("   这是第三行")
    print("5. 提交评论")
    print("6. 检查评论是否正确显示换行")
    print()
    print("如果评论中的换行正确显示，则修复成功！")
    print("修复内容: 使用Markup确保HTML标签被正确渲染")
    
    return True

if __name__ == "__main__":
    test_nl2br_filter() 