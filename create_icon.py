#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建简单的应用程序图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """创建应用程序图标"""
    print("🎨 创建应用程序图标...")
    
    # 创建512x512的图标
    size = 512
    icon = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(icon)
    
    # 绘制圆形背景
    margin = 50
    circle_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(circle_bbox, fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=10)
    
    # 绘制文字
    try:
        # 尝试使用系统字体
        font_size = 120
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        # 使用默认字体
        font = ImageFont.load_default()
        font_size = 80
    
    text = "AC"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # 保存图标
    icon_path = "icon.png"
    icon.save(icon_path, "PNG")
    
    print(f"✅ 图标创建成功: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_icon() 