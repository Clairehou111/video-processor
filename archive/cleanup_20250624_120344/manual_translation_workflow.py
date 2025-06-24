#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动翻译工作流程
1. 提取英文字幕
2. 用户手动提供中文翻译
3. 生成双语视频
"""

import os
import re
import subprocess
from pathlib import Path

class ManualTranslationWorkflow:
    """手动翻译工作流程处理器"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        
    def extract_english_subtitles(self, srt_file):
        """提取英文字幕内容"""
        print("📖 提取英文字幕...")
        
        try:
            with open(srt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 分割字幕块
            blocks = content.strip().split('\n\n')
            english_lines = []
            
            for i, block in enumerate(blocks, 1):
                lines = block.strip().split('\n')
                if len(lines) >= 3:
                    # 提取文本内容
                    text = ' '.join(lines[2:])
                    english_lines.append(f"{i}. {text}")
            
            # 保存英文字幕列表
            english_file = os.path.join(self.output_dir, "english_subtitles_for_translation.txt")
            with open(english_file, 'w', encoding='utf-8') as f:
                f.write("英文字幕内容 (请在下方提供对应的中文翻译):\n")
                f.write("="*50 + "\n\n")
                for line in english_lines:
                    f.write(line + "\n")
                
                f.write("\n" + "="*50 + "\n")
                f.write("请在此处提供中文翻译 (保持相同的编号格式):\n")
                f.write("="*50 + "\n\n")
                f.write("示例格式:\n")
                f.write("1. 中文翻译内容\n")
                f.write("2. 中文翻译内容\n")
                f.write("...\n\n")
            
            print(f"✅ 英文字幕已提取: {english_file}")
            print(f"📊 共 {len(english_lines)} 条字幕")
            
            # 显示前5条预览
            print("\n📄 英文字幕预览 (前5条):")
            for i, line in enumerate(english_lines[:5]):
                print(f"   {line}")
            if len(english_lines) > 5:
                print(f"   ... 还有 {len(english_lines) - 5} 条")
            
            return english_file, english_lines
            
        except Exception as e:
            print(f"❌ 提取英文字幕失败: {e}")
            return None, None
    
    def wait_for_chinese_translation(self, english_file):
        """等待用户提供中文翻译"""
        print(f"\n📝 请编辑文件并添加中文翻译:")
        print(f"   文件位置: {english_file}")
        print(f"   📂 在文件管理器中打开: {os.path.abspath(english_file)}")
        
        # 自动打开文件
        try:
            import subprocess
            import platform
            
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", english_file])
            elif platform.system() == "Windows":
                subprocess.run(["notepad", english_file])
            else:  # Linux
                subprocess.run(["xdg-open", english_file])
            
            print("✅ 文件已自动打开")
        except:
            print("⚠️ 请手动打开文件进行编辑")
        
        print("\n💡 翻译要求:")
        print("   1. 保持编号格式 (1. 2. 3. ...)")
        print("   2. 每行一条翻译")
        print("   3. 保持政治脱口秀的幽默感")
        print("   4. 专有名词可保持英文")
        
        input("\n⏳ 翻译完成后，请按回车键继续...")
        
        return self.extract_chinese_translation(english_file)
    
    def extract_chinese_translation(self, translation_file):
        """从编辑后的文件中提取中文翻译"""
        print("📖 提取中文翻译...")
        
        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找中文翻译部分
            lines = content.split('\n')
            chinese_lines = []
            start_extracting = False
            
            for line in lines:
                line = line.strip()
                
                # 跳过示例和说明
                if "示例格式" in line or "中文翻译内容" in line:
                    continue
                
                # 开始提取中文翻译
                if re.match(r'^\d+\.', line) and not line.endswith('gross.') and not line.endswith('getting.'):
                    # 检查是否包含中文字符
                    if any('\u4e00' <= char <= '\u9fff' for char in line):
                        chinese_lines.append(line)
                        start_extracting = True
                    elif start_extracting:
                        # 如果已经开始提取但这行没有中文，可能是英文原文，跳过
                        continue
            
            if not chinese_lines:
                print("❌ 未找到中文翻译，请检查文件格式")
                print("💡 确保中文翻译使用格式: 1. 中文内容")
                return None
            
            # 保存中文翻译
            chinese_file = os.path.join(self.output_dir, "chinese_translation.txt")
            with open(chinese_file, 'w', encoding='utf-8') as f:
                for line in chinese_lines:
                    f.write(line + "\n")
            
            print(f"✅ 中文翻译已提取: {chinese_file}")
            print(f"📊 共 {len(chinese_lines)} 条翻译")
            
            # 显示前5条预览
            print("\n📄 中文翻译预览 (前5条):")
            for i, line in enumerate(chinese_lines[:5]):
                print(f"   {line}")
            if len(chinese_lines) > 5:
                print(f"   ... 还有 {len(chinese_lines) - 5} 条")
            
            return chinese_file
            
        except Exception as e:
            print(f"❌ 提取中文翻译失败: {e}")
            return None
    
    def create_bilingual_video(self, video_file, english_srt_file, chinese_file):
        """创建双语视频"""
        print("🎬 开始创建双语视频...")
        
        try:
            # 调用现有的双语视频创建脚本
            result = subprocess.run(
                ["python3", "create_bilingual_video.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                print("✅ 双语视频创建成功!")
                print(result.stdout)
                return True
            else:
                print(f"❌ 双语视频创建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 创建双语视频时出错: {e}")
            return False
    
    def run_workflow(self, video_file=None, english_srt_file=None):
        """运行完整的手动翻译工作流程"""
        print("🎯 手动翻译工作流程")
        print("="*50)
        
        # 自动检测文件
        if not video_file:
            video_file = "output/VP9_segment_2m36s-5m59s.mp4"
        if not english_srt_file:
            english_srt_file = "output/VP9_segment_2m36s-5m59s_english.srt"
        
        # 检查文件是否存在
        if not os.path.exists(video_file):
            print(f"❌ 视频文件不存在: {video_file}")
            return False
        
        if not os.path.exists(english_srt_file):
            print(f"❌ 英文字幕文件不存在: {english_srt_file}")
            return False
        
        print(f"📁 输入文件:")
        print(f"   🎬 视频: {video_file}")
        print(f"   📝 英文字幕: {english_srt_file}")
        
        # 步骤1: 提取英文字幕
        print(f"\n📖 步骤1: 提取英文字幕")
        english_file, english_lines = self.extract_english_subtitles(english_srt_file)
        if not english_file:
            return False
        
        # 步骤2: 等待用户提供中文翻译
        print(f"\n📝 步骤2: 等待中文翻译")
        chinese_file = self.wait_for_chinese_translation(english_file)
        if not chinese_file:
            return False
        
        # 步骤3: 创建双语视频
        print(f"\n🎬 步骤3: 创建双语视频")
        success = self.create_bilingual_video(video_file, english_srt_file, chinese_file)
        
        if success:
            print(f"\n🎉 手动翻译工作流程完成!")
            print(f"📁 输出文件:")
            
            # 列出生成的文件
            bilingual_video = video_file.replace('.mp4', '_bilingual.mp4')
            bilingual_srt = english_srt_file.replace('_english.srt', '_bilingual.srt')
            
            if os.path.exists(bilingual_video):
                size_mb = os.path.getsize(bilingual_video) / (1024*1024)
                print(f"   🎬 双语视频: {bilingual_video} ({size_mb:.1f}MB)")
            
            if os.path.exists(bilingual_srt):
                print(f"   📝 双语字幕: {bilingual_srt}")
            
            print(f"   📖 中文翻译: {chinese_file}")
            
        return success

def main():
    """主函数"""
    workflow = ManualTranslationWorkflow()
    
    # 运行工作流程
    try:
        success = workflow.run_workflow()
        if success:
            print("\n✅ 所有任务完成!")
        else:
            print("\n❌ 工作流程失败")
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\n❌ 工作流程出错: {e}")

if __name__ == "__main__":
    main() 