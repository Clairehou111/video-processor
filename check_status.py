#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目状态检查脚本
"""

import sys
import os
import subprocess

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本需要3.8+")
        return False

def check_dependencies():
    """检查依赖库"""
    dependencies = [
        ('yt_dlp', 'YouTube下载'),
        ('whisper', 'Whisper语音识别'),
        ('moviepy', 'MoviePy视频处理'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow图像处理'),
        ('numpy', 'NumPy数值计算'),
        ('requests', 'HTTP请求')
    ]
    
    print("\n检查依赖库:")
    all_ok = True
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {description} ({module})")
        except ImportError:
            print(f"❌ {description} ({module}) - 未安装")
            all_ok = False
    
    return all_ok

def check_directories():
    """检查目录结构"""
    print("\n检查目录结构:")
    
    required_files = [
        'video_processor.py',
        'demo.py',
        'quick_test.py',
        'setup.sh',
        'README.md'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 文件缺失")
            all_ok = False
    
    # 检查输出目录
    if os.path.exists('output'):
        print("✅ output目录")
    else:
        print("⚠️ output目录 - 将在首次运行时创建")
    
    return all_ok

def check_virtual_env():
    """检查虚拟环境"""
    print("\n检查虚拟环境:")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 当前在虚拟环境中")
        return True
    else:
        print("⚠️ 当前不在虚拟环境中")
        print("建议激活虚拟环境: source venv/bin/activate")
        return False

def main():
    """主函数"""
    print("=== YouTube视频处理工具 - 状态检查 ===\n")
    
    checks = [
        ("Python版本", check_python_version),
        ("虚拟环境", check_virtual_env),
        ("项目文件", check_directories),
        ("依赖库", check_dependencies)
    ]
    
    results = []
    for name, check_func in checks:
        results.append((name, check_func()))
    
    print("\n" + "="*50)
    print("检查总结:")
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有检查通过！项目已准备就绪")
        print("\n推荐使用方法:")
        print("1. python demo.py - 运行演示")
        print("2. python video_processor.py - 完整功能")
    else:
        print("⚠️ 有些检查未通过，请解决问题后重试")
        print("\n解决方法:")
        print("1. 确保在虚拟环境中: source venv/bin/activate")
        print("2. 安装依赖: ./setup.sh 或手动安装")
        print("3. 检查Python版本是否为3.8+")

if __name__ == "__main__":
    main() 