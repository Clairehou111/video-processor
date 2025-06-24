#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保存Sider.AI翻译结果的脚本
用于处理从Browser MCP获取的翻译数据
"""

import os
import re
from datetime import datetime

def save_translation_result(translation_text, output_file="output/sider_chinese_translation.txt"):
    """
    保存翻译结果到文件
    
    Args:
        translation_text (str): 翻译文本
        output_file (str): 输出文件路径
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 清理和格式化翻译文本
        cleaned_text = clean_translation_text(translation_text)
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        print(f"✅ 翻译结果已保存到: {output_file}")
        print(f"📊 翻译内容长度: {len(cleaned_text)} 字符")
        
        # 显示预览
        lines = cleaned_text.split('\n')[:10]
        print(f"📄 翻译预览 (前10行):")
        for line in lines:
            if line.strip():
                print(f"   {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ 保存翻译结果失败: {e}")
        return False

def clean_translation_text(text):
    """
    清理和格式化翻译文本
    
    Args:
        text (str): 原始翻译文本
        
    Returns:
        str: 清理后的文本
    """
    # 移除多余的空行
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            # 确保编号格式正确
            if re.match(r'^\d+\.', line):
                cleaned_lines.append(line)
            elif line and not line.startswith('请') and not line.startswith('以下'):
                # 可能是翻译内容但没有编号，尝试添加编号
                if cleaned_lines:
                    last_num = len(cleaned_lines)
                    cleaned_lines.append(f"{last_num + 1}. {line}")
                else:
                    cleaned_lines.append(f"1. {line}")
    
    return '\n'.join(cleaned_lines)

def create_bilingual_subtitles():
    """
    使用新的翻译结果创建双语字幕
    """
    try:
        import subprocess
        print("🎬 开始创建双语字幕和视频...")
        
        result = subprocess.run(
            ["python3", "create_bilingual_video.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✅ 双语视频创建成功!")
            print(result.stdout)
        else:
            print(f"❌ 双语视频创建失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 创建双语视频时出错: {e}")

def main():
    """
    主函数 - 处理用户输入的翻译结果
    """
    print("🎯 Sider.AI翻译结果保存工具")
    print("="*50)
    
    # 检查是否有现有的翻译文件
    existing_file = "output/chinese_translation.txt"
    if os.path.exists(existing_file):
        print(f"📁 发现现有翻译文件: {existing_file}")
        choice = input("是否要替换现有翻译? (y/n): ").lower().strip()
        if choice != 'y':
            print("操作已取消")
            return
    
    print("\n📝 请粘贴从Sider.AI获取的翻译结果:")
    print("(输入完成后按Ctrl+D或输入'END'结束)")
    print("-" * 50)
    
    translation_lines = []
    try:
        while True:
            line = input()
            if line.strip() == 'END':
                break
            translation_lines.append(line)
    except EOFError:
        pass
    
    if not translation_lines:
        print("❌ 未输入任何翻译内容")
        return
    
    translation_text = '\n'.join(translation_lines)
    
    # 保存翻译结果
    if save_translation_result(translation_text):
        # 询问是否创建双语视频
        choice = input("\n🎬 是否立即创建双语视频? (y/n): ").lower().strip()
        if choice == 'y':
            create_bilingual_subtitles()
    
    print("\n🎉 处理完成!")

if __name__ == "__main__":
    main() 