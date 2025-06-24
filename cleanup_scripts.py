#!/usr/bin/env python3
"""
视频处理脚本清理工具
保留核心功能脚本，删除重复或过时的脚本
"""

import os
import shutil
from pathlib import Path

class ScriptCleanup:
    def __init__(self):
        self.keep_scripts = [
            # 核心自动化脚本
            "complete_video_automation.py",
            "create_simple_bilingual_video.py",
            "optimized_youtube_downloader.py",
            
            # 保留的工具脚本
            "bilingual_subtitle_processor.py",
            "manual_translation_workflow.py",
            "verify_quality_parameters.py",
            
            # 配置和指南
            "requirements.txt",
            "setup.sh",
            "COMPLETE_TRANSLATION_GUIDE.md",
            "AUTO_PROCESSOR_GUIDE.md",
            "project_summary.md",
            "README.md",
            
            # 清理工具本身
            "cleanup_scripts.py"
        ]
        
        self.remove_scripts = [
            # 重复的下载器
            "video_processor.py",
            "improved_video_processor.py", 
            "auto_video_processor.py",
            "download_video_segment.py",
            "simple_segment_downloader.py",
            "direct_segment_download.py",
            
            # 重复的翻译工具
            "sider_workflow.py",
            "auto_sider_workflow.py",
            "real_sider_workflow.py",
            "sider_video_processor.py",
            "automated_sider_translation.py",
            "fully_automated_sider_translator.py",
            "sider_ai_translation_helper.py",
            "sider_translation_helper.py",
            "sider_trump_translation.py",
            
            # 过时的MCP自动化
            "browser_mcp_translator.py",
            "browser_mcp_automation_executor.py",
            "complete_browser_mcp_automation.py", 
            "real_browser_mcp_automation.py",
            "real_browser_mcp_translator.py",
            "precise_sider_automation.py",
            
            # 重复的视频生成
            "create_bilingual_video.py",
            "create_chinese_subtitle_video.py",
            "create_final_video.py",
            "create_ffmpeg_video.py",
            "create_test_video.py",
            
            # 专门的项目脚本（不通用）
            "create_trump_jan6_final_video.py",
            "trump_jan6_special_danmaku.py",
            "create_bilibili_version.py",
            "create_bilibili_hd_version.py",
            "create_tiktok_version.py",
            "improved_bilibili_generator.py",
            
            # 演示和测试脚本
            "demo.py",
            "demo_sider_integration.py",
            "demo_improved_workflow.py",
            "high_quality_demo.py",
            "ultra_high_quality_demo.py",
            "quick_test.py",
            "check_status.py",
            
            # 单功能工具（已整合）
            "extract_english_subtitles.py",
            "convert_srt_to_ass.py",
            "create_dual_subtitles.py",
            "fix_subtitle_layers.py",
            "subtitle_embed_demo.py",
            
            # 弹幕相关（非核心功能）
            "create_jianying_danmaku.py",
            "advanced_jianying_danmaku.py",
            "create_video_with_danmaku.py",
            "danmaku_coordinates_demo.py",
            "preview_danmaku_effects.py",
            "auto_jianying_project.py",
            
            # 缩略图工具（非核心）
            "create_thumbnail.py",
            "create_clean_thumbnail.py",
            "create_custom_frame_thumbnail.py",
            "create_tiktok_thumbnail.py",
            "create_video_frame_thumbnail.py",
            
            # 文件上传和保存
            "sider_file_upload_automation.py",
            "save_sider_translation.py",
            "save_translation_result.py",
            "generate_sider_video.py",
            
            # 其他实验性脚本
            "complete_automation.py",
            "advanced_translation_demo.py",
            "download_and_process_serious_video.py"
        ]
    
    def analyze_scripts(self):
        """分析当前脚本情况"""
        print("📊 分析当前脚本情况...")
        print("="*50)
        
        all_python_files = [f for f in os.listdir('.') if f.endswith('.py')]
        
        print(f"📁 总计Python文件: {len(all_python_files)}")
        print(f"✅ 保留脚本: {len(self.keep_scripts)}")
        print(f"🗑️  待删除脚本: {len(self.remove_scripts)}")
        
        # 检查意外的脚本
        unexpected = set(all_python_files) - set(self.keep_scripts) - set(self.remove_scripts)
        if unexpected:
            print(f"⚠️  未分类脚本: {len(unexpected)}")
            for script in sorted(unexpected):
                print(f"   • {script}")
        
        return all_python_files
    
    def backup_scripts(self):
        """备份要删除的脚本"""
        backup_dir = "backup_deleted_scripts"
        
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        os.makedirs(backup_dir)
        
        print(f"\n💾 备份删除的脚本到: {backup_dir}")
        
        backed_up = 0
        for script in self.remove_scripts:
            if os.path.exists(script):
                shutil.copy2(script, backup_dir)
                backed_up += 1
                print(f"   ✅ {script}")
        
        print(f"📊 备份完成，共 {backed_up} 个文件")
        return backup_dir
    
    def remove_scripts(self):
        """删除指定的脚本"""
        print(f"\n🗑️  开始删除脚本...")
        
        removed_count = 0
        for script in self.remove_scripts:
            if os.path.exists(script):
                os.remove(script)
                removed_count += 1
                print(f"   🗑️  删除: {script}")
        
        print(f"✅ 删除完成，共删除 {removed_count} 个文件")
        return removed_count
    
    def show_final_structure(self):
        """显示清理后的结构"""
        print(f"\n📁 清理后的脚本结构:")
        print("="*50)
        
        # 按功能分类显示保留的脚本
        categories = {
            "🎯 核心自动化": [
                "complete_video_automation.py",
                "create_simple_bilingual_video.py"
            ],
            "📥 下载工具": [
                "optimized_youtube_downloader.py"
            ],
            "🔧 处理工具": [
                "bilingual_subtitle_processor.py",
                "manual_translation_workflow.py",
                "verify_quality_parameters.py"
            ],
            "📚 文档指南": [
                "COMPLETE_TRANSLATION_GUIDE.md",
                "AUTO_PROCESSOR_GUIDE.md",
                "project_summary.md",
                "README.md"
            ],
            "⚙️ 配置": [
                "requirements.txt",
                "setup.sh",
                "cleanup_scripts.py"
            ]
        }
        
        for category, scripts in categories.items():
            print(f"\n{category}:")
            for script in scripts:
                if os.path.exists(script):
                    print(f"   ✅ {script}")
                else:
                    print(f"   ❌ {script} (未找到)")
    
    def create_usage_guide(self):
        """创建使用指南"""
        guide_content = """# 视频处理系统使用指南

## 🚀 快速开始

### 1. 完整自动化处理
```bash
python complete_video_automation.py
```
- 输入YouTube URL，自动创建项目目录
- 选择是否切片
- 等待提取字幕
- 完成翻译后运行 `python complete_video_automation.py --finalize`

### 项目管理
```bash
python complete_video_automation.py --list      # 列出所有项目
python complete_video_automation.py --continue <项目目录>  # 继续指定项目
```

### 2. 手动翻译流程
```bash
python manual_translation_workflow.py
```
- 适合需要精细控制翻译质量的场景

### 3. 单独生成双语视频
```bash
python create_simple_bilingual_video.py
```
- 使用现有的中英文字幕文件

## 📁 核心文件说明

- `complete_video_automation.py` - 主要自动化脚本
- `COMPLETE_TRANSLATION_GUIDE.md` - 完整翻译指南
- `optimized_youtube_downloader.py` - 高质量下载器
- `requirements.txt` - 依赖包列表

## 🎯 推荐工作流程

1. 使用 `complete_video_automation.py` 开始
2. 参考 `COMPLETE_TRANSLATION_GUIDE.md` 进行翻译
3. 运行 `--finalize` 完成处理
4. 使用生成的B站元数据上传

## 🔧 故障排除

- 检查依赖: `pip install -r requirements.txt`
- 验证FFmpeg: `ffmpeg -version`
- 检查Whisper: `python -c "import whisper; print('OK')"`
"""
        
        with open("USAGE_GUIDE.md", 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"\n📖 使用指南已创建: USAGE_GUIDE.md")
    
    def run_cleanup(self, confirm=True):
        """运行完整的清理流程"""
        print("🧹 视频处理脚本清理工具")
        print("="*50)
        
        # 分析当前情况
        all_files = self.analyze_scripts()
        
        if confirm:
            print(f"\n⚠️  将删除 {len([s for s in self.remove_scripts if os.path.exists(s)])} 个脚本")
            print("这些脚本的功能已被整合到核心脚本中")
            
            choice = input("\n是否继续? (y/N): ").strip().lower()
            if choice != 'y':
                print("❌ 取消清理")
                return False
        
        # 备份
        backup_dir = self.backup_scripts()
        
        # 删除
        removed_count = self.remove_scripts()
        
        # 显示结果
        self.show_final_structure()
        
        # 创建使用指南
        self.create_usage_guide()
        
        print(f"\n🎉 清理完成!")
        print(f"📊 删除了 {removed_count} 个重复/过时脚本")
        print(f"💾 备份保存在: {backup_dir}")
        print(f"📖 查看使用指南: USAGE_GUIDE.md")
        
        return True

def main():
    cleanup = ScriptCleanup()
    cleanup.run_cleanup()

if __name__ == "__main__":
    main() 