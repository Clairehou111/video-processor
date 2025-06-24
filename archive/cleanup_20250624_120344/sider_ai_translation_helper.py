#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sider.AI翻译助手
帮助用户使用Sider.AI进行字幕翻译
"""

import os
import webbrowser
import pyperclip
from pathlib import Path

class SiderAITranslationHelper:
    """Sider.AI翻译助手"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        
    def prepare_translation_prompt(self, english_segments):
        """准备翻译提示词"""
        prompt = """请将以下英文字幕翻译为中文，要求：
1. 保持原有的编号格式
2. 翻译要自然流畅，符合中文表达习惯
3. 保持政治脱口秀的幽默感和讽刺语调
4. 专有名词（人名、地名）保持英文或使用通用中文译名
5. 每行翻译后请换行

英文字幕内容：

"""
        
        for i, segment in enumerate(english_segments, 1):
            prompt += f"{i}. {segment['text']}\n"
        
        return prompt
    
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        try:
            pyperclip.copy(text)
            return True
        except:
            return False
    
    def open_sider_ai(self):
        """打开Sider.AI网站"""
        try:
            webbrowser.open("https://sider.ai")
            return True
        except:
            return False
    
    def show_instructions(self, prompt_text):
        """显示使用说明"""
        print("🤖 Sider.AI 翻译指南")
        print("="*60)
        print()
        
        # 尝试复制到剪贴板
        clipboard_success = self.copy_to_clipboard(prompt_text)
        
        if clipboard_success:
            print("✅ 翻译提示词已复制到剪贴板！")
        else:
            print("⚠️ 无法自动复制，请手动复制以下内容：")
        
        print()
        print("🔧 使用步骤:")
        print("1. 打开 https://sider.ai")
        print("2. 选择 ChatGPT 或 Claude 模型")
        print("3. 粘贴翻译提示词 (已复制到剪贴板)" if clipboard_success else "3. 复制下方的翻译提示词")
        print("4. 等待翻译完成")
        print("5. 复制翻译结果")
        print(f"6. 保存到文件: {os.path.join(self.output_dir, 'chinese_translation.txt')}")
        print()
        
        # 尝试自动打开网站
        if self.open_sider_ai():
            print("🌐 已自动打开Sider.AI网站")
        else:
            print("🌐 请手动打开: https://sider.ai")
        
        print()
        if not clipboard_success:
            print("📝 翻译提示词:")
            print("─" * 60)
            print(prompt_text)
            print("─" * 60)
        
        print()
        print("⏳ 完成翻译后，将结果保存到文件，然后运行:")
        print("   python create_bilingual_video.py")
        print()
        
        input("按回车键继续...")
    
    def validate_translation_file(self, translation_file):
        """验证翻译文件"""
        if not os.path.exists(translation_file):
            print(f"❌ 翻译文件不存在: {translation_file}")
            return False
        
        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                print(f"❌ 翻译文件为空: {translation_file}")
                return False
            
            # 检查是否包含编号格式
            lines = content.split('\n')
            numbered_lines = [line for line in lines if line.strip() and line.strip().startswith(('1.', '2.', '3.'))]
            
            if len(numbered_lines) < 3:
                print(f"⚠️ 翻译文件格式可能不正确，请检查是否保持了编号格式")
                return False
            
            print(f"✅ 翻译文件验证通过: {len(numbered_lines)} 条翻译")
            return True
            
        except Exception as e:
            print(f"❌ 读取翻译文件失败: {e}")
            return False

def main():
    """主函数"""
    print("🤖 Sider.AI 翻译助手")
    print("="*50)
    
    helper = SiderAITranslationHelper()
    
    # 检查英文字幕文件
    english_srt_files = []
    output_dir = "output"
    
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.endswith('_english.srt'):
                english_srt_files.append(os.path.join(output_dir, file))
    
    if not english_srt_files:
        print("❌ 未找到英文字幕文件")
        print("请先运行 bilingual_subtitle_processor.py 提取英文字幕")
        return
    
    print("📝 可用的英文字幕文件:")
    for i, srt_file in enumerate(english_srt_files, 1):
        print(f"   {i}. {os.path.basename(srt_file)}")
    
    # 选择字幕文件
    try:
        if len(english_srt_files) == 1:
            choice = 0
            print(f"\n自动选择: {os.path.basename(english_srt_files[0])}")
        else:
            choice = int(input(f"\n请选择字幕文件 (1-{len(english_srt_files)}): ")) - 1
            
        if 0 <= choice < len(english_srt_files):
            selected_srt = english_srt_files[choice]
        else:
            print("❌ 无效选择")
            return
    except ValueError:
        print("❌ 无效输入")
        return
    
    # 解析英文字幕
    print(f"\n📖 解析英文字幕: {os.path.basename(selected_srt)}")
    
    try:
        with open(selected_srt, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单解析SRT格式
        segments = []
        blocks = content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                text = ' '.join(lines[2:])
                segments.append({'text': text})
        
        print(f"✅ 解析完成，共 {len(segments)} 个片段")
        
    except Exception as e:
        print(f"❌ 解析字幕文件失败: {e}")
        return
    
    # 准备翻译提示词
    prompt_text = helper.prepare_translation_prompt(segments)
    
    # 保存提示词到文件
    prompt_file = os.path.join(output_dir, "sider_translation_prompt.txt")
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_text)
    print(f"📝 翻译提示词已保存: {prompt_file}")
    
    # 显示使用说明
    helper.show_instructions(prompt_text)
    
    # 检查翻译结果
    translation_file = os.path.join(output_dir, "chinese_translation.txt")
    print(f"\n🔍 检查翻译文件: {translation_file}")
    
    if helper.validate_translation_file(translation_file):
        print("\n🎉 翻译文件准备就绪！")
        print("现在可以运行: python create_bilingual_video.py")
    else:
        print("\n⏳ 请完成Sider.AI翻译后重新运行此脚本")

if __name__ == "__main__":
    main() 