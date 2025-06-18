#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_windows_exe():
    """创建Windows可执行文件"""
    print("🪟 创建Windows可执行文件...")
    
    # 检查是否安装了pyinstaller
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        print("📦 安装PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 创建spec文件
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['start_windows.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('app', 'app'),
        ('config.py', '.'),
        ('run.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('CHANGELOG.md', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_login',
        'flask_bcrypt',
        'werkzeug',
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'click',
        'blinker',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AnswerCustomer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnswerCustomer',
)
'''
    
    with open('AnswerCustomer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # 运行PyInstaller
    print("🔨 正在构建可执行文件...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller", 
        "--clean", "--noconfirm", "AnswerCustomer.spec"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 可执行文件创建成功")
        
        # 检查输出目录
        dist_dir = Path("dist/AnswerCustomer")
        if dist_dir.exists():
            print(f"   位置: {dist_dir.absolute()}")
            print("   现在可以双击运行了！")
            
            # 创建桌面快捷方式
            create_shortcut(dist_dir)
            
        return True
    else:
        print(f"❌ 构建失败: {result.stderr}")
        return False

def create_shortcut(dist_dir):
    """创建桌面快捷方式"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "AnswerCustomer.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = str(dist_dir / "AnswerCustomer.exe")
        shortcut.WorkingDirectory = str(dist_dir)
        shortcut.IconLocation = str(dist_dir / "AnswerCustomer.exe")
        shortcut.save()
        
        print(f"✅ 桌面快捷方式创建成功: {shortcut_path}")
        
    except ImportError:
        print("⚠️ 无法创建桌面快捷方式，需要安装pywin32和winshell")
        print("   可以手动将dist/AnswerCustomer/AnswerCustomer.exe复制到桌面")
    except Exception as e:
        print(f"⚠️ 创建快捷方式失败: {e}")

def create_icon():
    """创建Windows图标"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("🎨 创建Windows图标...")
        
        # 创建不同尺寸的图标
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for size in sizes:
            # 创建图像
            img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制圆形背景
            margin = size // 10
            circle_bbox = [margin, margin, size - margin, size - margin]
            draw.ellipse(circle_bbox, fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=max(1, size//50))
            
            # 绘制文字
            try:
                font_size = size // 4
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
                font_size = size // 6
            
            text = "AC"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
            images.append(img)
        
        # 保存为ICO文件
        images[0].save("icon.ico", format='ICO', sizes=[(size, size) for size in sizes])
        print("✅ 图标创建成功: icon.ico")
        
    except ImportError:
        print("⚠️ 无法创建图标，需要安装Pillow")
        print("   可以手动添加icon.ico文件")
    except Exception as e:
        print(f"⚠️ 创建图标失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🪟 AnswerCustomer Windows可执行文件生成器")
    print("=" * 60)
    
    # 创建图标
    create_icon()
    
    # 创建可执行文件
    if create_windows_exe():
        print("\n🎉 Windows可执行文件创建完成！")
        print("\n📋 使用说明:")
        print("1. 双击 dist/AnswerCustomer/AnswerCustomer.exe 启动")
        print("2. 或者使用桌面快捷方式")
        print("3. 程序会自动安装依赖并启动服务")
    else:
        print("\n❌ 创建失败，请检查错误信息")

if __name__ == "__main__":
    main() 