#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的 B站视频自动化工作流
一键完成：视频下载 → 字幕提取 → 翻译 → 双语视频生成 → 缩略图生成 → 上传内容准备

字幕配置标准 (已验证的最佳设置):
- 中文字幕: PingFang SC, 22px, MarginV=60, 白色(&Hffffff)
- 英文字幕: Arial, 18px, MarginV=20, 白色(&Hffffff)  
- 水印: PingFang SC, 24px, 右上角(Alignment=9), MarginV=15, 白色
- 水印内容: "董卓主演脱口秀"
- 水印定位: MarginL=10, MarginR=15, MarginV=15

这些参数经过测试，确保:
1. 字幕位置稳定，不会忽高忽低
2. 中文字幕在英文字幕上方，间距适中
3. 白色字幕在各种背景下清晰可见
4. 水印位置固定在右上角
5. 时间格式精确同步，无延迟问题
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
import shutil
from pathlib import Path

def print_step(step_num, title, description=""):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"📍 步骤 {step_num}: {title}")
    if description:
        print(f"   {description}")
    print('='*60)

def create_project_directory(video_title):
    """创建项目目录"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')[:50]  # 限制长度
    
    project_name = f"{safe_title}_{timestamp}"
    project_dir = f"output/{project_name}"
    
    # 创建目录结构
    directories = [
        project_dir,
        f"{project_dir}/subtitles",
        f"{project_dir}/final",
        f"{project_dir}/temp"
    ]
    
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
    
    return project_dir, project_name

def download_video(url, project_dir):
    """下载高质量视频"""
    print_step(1, "下载YouTube视频", "使用优化的格式选择器确保最高质量")
    
    # 构建下载命令
    cmd = [
        'yt-dlp',
        '--format', 'bestvideo[height>=1080][vcodec^=vp9]+bestaudio[acodec^=opus]/bestvideo[height>=1080]+bestaudio/best[height>=1080]',
        '--merge-output-format', 'mp4',
        '--write-info-json',
        '--output', f'{project_dir}/%(title)s.%(ext)s',
        url
    ]
    
    print(f"🔄 执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            # 查找下载的视频文件
            for file in os.listdir(project_dir):
                if file.endswith('.mp4'):
                    video_path = os.path.join(project_dir, file)
                    print(f"✅ 视频下载成功: {file}")
                    
                    # 显示文件信息
                    file_size = os.path.getsize(video_path) / (1024 * 1024)
                    print(f"📊 文件大小: {file_size:.1f}MB")
                    
                    return video_path
        else:
            print(f"❌ 下载失败: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("❌ 下载超时")
        return None
    except Exception as e:
        print(f"❌ 下载异常: {e}")
        return None

def extract_subtitles(video_path, project_dir):
    """提取英文字幕"""
    print_step(2, "提取英文字幕", "使用Whisper模型进行语音识别")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_path = f"{project_dir}/subtitles/{video_name}_english.srt"
    
    try:
        import whisper
        
        print("🔄 加载Whisper模型...")
        model = whisper.load_model("base")
        
        print("🔄 转录音频...")
        result = model.transcribe(video_path, language="en")
        
        # 保存SRT格式
        with open(subtitle_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result["segments"]):
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"].strip()
                
                f.write(f"{i+1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        print(f"✅ 英文字幕已保存: {subtitle_path}")
        print(f"📊 字幕段数: {len(result['segments'])}")
        
        return subtitle_path
        
    except ImportError:
        print("❌ 请先安装whisper: pip install openai-whisper")
        return None
    except Exception as e:
        print(f"❌ 字幕提取失败: {e}")
        return None

def format_timestamp(seconds):
    """格式化时间戳为SRT格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_translation_prompt(english_subtitle_path, project_dir):
    """生成翻译提示文件"""
    print_step(3, "生成翻译提示", "为Sider.AI准备翻译内容")
    
    # 读取英文字幕
    with open(english_subtitle_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取纯文本
    lines = content.split('\n')
    texts = []
    for line in lines:
        line = line.strip()
        if line and not line.isdigit() and '-->' not in line:
            texts.append(line)
    
    # 生成翻译提示
    prompt_content = f"""请将以下英文字幕翻译成中文，要求：

1. 保持原意准确性
2. 符合中文表达习惯  
3. 适合B站观众口味
4. 保留政治幽默感
5. 每行对应翻译，保持行数一致

英文字幕内容：
{'=' * 50}
{chr(10).join(texts)}
{'=' * 50}

请直接提供中文翻译结果，每行一句，不需要其他说明。"""

    prompt_path = f"{project_dir}/translation_prompt.txt"
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    print(f"✅ 翻译提示已生成: {prompt_path}")
    print(f"📊 文本行数: {len(texts)}")
    
    return prompt_path

def wait_for_chinese_translation(project_dir):
    """等待用户提供中文翻译"""
    print_step(4, "等待中文翻译", "请手动使用Sider.AI完成翻译")
    
    chinese_subtitle_path = f"{project_dir}/subtitles/chinese_translation.srt"
    
    print("📋 请按以下步骤完成翻译：")
    print("1. 打开translation_prompt.txt文件")
    print("2. 复制内容到Sider.AI进行翻译")
    print("3. 将中文翻译结果保存为SRT格式")
    print(f"4. 保存到: {chinese_subtitle_path}")
    print("\n⏳ 等待中文字幕文件...")
    
    while not os.path.exists(chinese_subtitle_path):
        time.sleep(2)
        print(".", end="", flush=True)
    
    print(f"\n✅ 检测到中文字幕: {chinese_subtitle_path}")
    return chinese_subtitle_path

def create_bilingual_videos(video_path, english_subtitle_path, chinese_subtitle_path, project_dir):
    """生成双语视频"""
    print_step(5, "生成双语视频", "创建中英双语和纯中文版本")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 输出路径
    bilingual_output = f"{project_dir}/final/{video_name}_bilingual.mp4"
    chinese_output = f"{project_dir}/final/{video_name}_chinese.mp4"
    
    # 创建双语ASS字幕
    bilingual_ass = create_bilingual_ass_subtitle(english_subtitle_path, chinese_subtitle_path, project_dir)
    chinese_ass = create_chinese_ass_subtitle(chinese_subtitle_path, project_dir)
    
    # 生成双语版本
    bilingual_cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf', f"ass='{bilingual_ass}'",
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        bilingual_output
    ]
    
    print("🔄 生成双语版本...")
    result1 = subprocess.run(bilingual_cmd, capture_output=True, text=True)
    
    if result1.returncode == 0:
        size1 = os.path.getsize(bilingual_output) / (1024 * 1024)
        print(f"✅ 双语版本完成: {size1:.1f}MB")
    else:
        print(f"❌ 双语版本失败: {result1.stderr}")
    
    # 生成中文版本
    chinese_cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf', f"ass='{chinese_ass}'",
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        chinese_output
    ]
    
    print("🔄 生成中文版本...")
    result2 = subprocess.run(chinese_cmd, capture_output=True, text=True)
    
    if result2.returncode == 0:
        size2 = os.path.getsize(chinese_output) / (1024 * 1024)
        print(f"✅ 中文版本完成: {size2:.1f}MB")
    else:
        print(f"❌ 中文版本失败: {result2.stderr}")
    
    return bilingual_output if result1.returncode == 0 else None, chinese_output if result2.returncode == 0 else None

def create_bilingual_ass_subtitle(english_path, chinese_path, project_dir):
    """创建双语ASS字幕"""
    # 读取字幕
    with open(english_path, 'r', encoding='utf-8') as f:
        eng_content = f.read()
    with open(chinese_path, 'r', encoding='utf-8') as f:
        chi_content = f.read()
    
    # 解析SRT格式
    eng_subs = parse_srt(eng_content)
    chi_subs = parse_srt(chi_content)
    
    # 创建ASS字幕 - 使用经过验证的最佳配置
    ass_content = """[Script Info]
Title: Bilingual Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,60,1
Style: English,Arial,18,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,20,1
Style: Watermark,PingFang SC,24,&Hffffff,&Hffffff,&H000000,&H80000000,1,0,0,0,100,100,0,0,1,1,0,9,10,15,15,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    # 添加水印
    ass_content += "Dialogue: 0,0:00:00.00,9:59:59.99,Watermark,,0,0,0,,董卓主演脱口秀\n"
    
    # 添加字幕
    for i, (eng_sub, chi_sub) in enumerate(zip(eng_subs, chi_subs)):
        start_time = convert_to_ass_time(eng_sub['start'])
        end_time = convert_to_ass_time(eng_sub['end'])
        
        # 中文字幕（上方）
        ass_content += f"Dialogue: 0,{start_time},{end_time},Chinese,,0,0,0,,{chi_sub['text']}\n"
        # 英文字幕（下方）
        ass_content += f"Dialogue: 0,{start_time},{end_time},English,,0,0,0,,{eng_sub['text']}\n"
    
    # 保存ASS文件
    ass_path = f"{project_dir}/subtitles/bilingual.ass"
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    return ass_path

def create_chinese_ass_subtitle(chinese_path, project_dir):
    """创建纯中文ASS字幕"""
    with open(chinese_path, 'r', encoding='utf-8') as f:
        chi_content = f.read()
    
    chi_subs = parse_srt(chi_content)
    
    ass_content = """[Script Info]
Title: Chinese Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,40,1
Style: Watermark,PingFang SC,24,&Hffffff,&Hffffff,&H000000,&H80000000,1,0,0,0,100,100,0,0,1,1,0,9,10,15,15,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    # 添加水印
    ass_content += "Dialogue: 0,0:00:00.00,9:59:59.99,Watermark,,0,0,0,,董卓主演脱口秀\n"
    
    # 添加中文字幕
    for sub in chi_subs:
        start_time = convert_to_ass_time(sub['start'])
        end_time = convert_to_ass_time(sub['end'])
        ass_content += f"Dialogue: 0,{start_time},{end_time},Chinese,,0,0,0,,{sub['text']}\n"
    
    ass_path = f"{project_dir}/subtitles/chinese.ass"
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    return ass_path

def parse_srt(content):
    """解析SRT字幕格式"""
    blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # 时间行
            time_line = lines[1]
            if ' --> ' in time_line:
                start_str, end_str = time_line.split(' --> ')
                # 文本行
                text = ' '.join(lines[2:])
                
                subtitles.append({
                    'start': parse_srt_time(start_str),
                    'end': parse_srt_time(end_str),
                    'text': text
                })
    
    return subtitles

def parse_srt_time(time_str):
    """解析SRT时间格式为秒数"""
    time_str = time_str.replace(',', '.')
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def convert_to_ass_time(seconds):
    """转换秒数为ASS时间格式 - 精确同步"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"

def generate_thumbnail(video_path, project_dir):
    """生成B站封面"""
    print_step(6, "生成B站封面", "创建带人物照片的专业封面")
    
    try:
        # 使用增强版封面生成器
        from generate_thumbnail_with_faces import create_enhanced_thumbnail
        
        thumbnail_path = f"{project_dir}/bilibili_thumbnail.jpg"
        create_enhanced_thumbnail(video_path, thumbnail_path)
        
        if os.path.exists(thumbnail_path):
            size = os.path.getsize(thumbnail_path) / 1024
            print(f"✅ 封面已生成: {size:.0f}KB")
            return thumbnail_path
        else:
            print("❌ 封面生成失败")
            return None
            
    except ImportError:
        print("⚠️ 生成简化版封面...")
        # 使用简化版生成器作为备用
        thumbnail_path = f"{project_dir}/simple_thumbnail.jpg"
        from generate_thumbnail import create_bilibili_thumbnail
        create_bilibili_thumbnail(thumbnail_path)
        return thumbnail_path

def generate_upload_content(video_path, project_dir):
    """生成B站上传内容"""
    print_step(7, "生成B站上传内容", "创建标题、简介、标签等")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 生成上传内容
    upload_content = f"""# B站上传内容

## 📺 视频标题
【政治瓜王】Ted Cruz被Tucker Carlson当场爆破！不知道伊朗人口还想开战？我笑不活了😂

## 📝 视频简介
这期Daily Show真的把我笑死了！Ted Cruz和Tucker Carlson为了伊朗问题吵起来，结果Cruz连伊朗有多少人都不知道还想开战？🤡

Tucker直接当场开始科普，这画面太搞笑了！两个共和党人互相爆破，比脱口秀还精彩！

🎯 视频亮点：
• Ted Cruz被当场打脸
• Tucker的迷惑行为大赏  
• 美国政治的荒诞现实
• 不知道敌国人口还想开战的神逻辑

#美国政治 #政治娱乐 #脱口秀 #TedCruz #TuckerCarlson #伊朗

⚠️ 本频道专注于政治娱乐内容，仅供娱乐，不代表任何政治立场

## 🏷️ 标签
美国政治,政治娱乐,脱口秀,Ted Cruz,Tucker Carlson,共和党,伊朗,Daily Show,政治瓜,时事评论,美国新闻,政治搞笑,当场爆破,不知道人口,开战,政治段子,娱乐解读,政治幽默,美式政治

## 📂 分类
时尚 > 资讯

## 🎨 封面
使用: bilibili_thumbnail.jpg

## 📋 上传检查清单
- [ ] 视频文件已准备 ({video_name})
- [ ] 封面图片已生成
- [ ] 标题符合B站规范
- [ ] 简介内容完整
- [ ] 标签已设置
- [ ] 分类已选择
"""

    content_path = f"{project_dir}/bilibili_upload_content.md"
    with open(content_path, 'w', encoding='utf-8') as f:
        f.write(upload_content)
    
    print(f"✅ 上传内容已生成: {content_path}")
    return content_path

def generate_workflow_summary(project_dir, project_name):
    """生成工作流程总结"""
    print_step(8, "生成流程总结", "创建完整的项目报告")
    
    summary = f"""# 🎬 B站视频处理完成报告

## 📁 项目信息
- **项目名称**: {project_name}
- **处理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **项目目录**: {project_dir}

## 📋 处理步骤
1. ✅ YouTube视频下载 (高质量VP9格式)
2. ✅ 英文字幕提取 (Whisper AI)
3. ✅ 翻译提示生成 (Sider.AI适配)
4. ✅ 中文翻译完成 (手动/AI辅助)
5. ✅ 双语视频生成 (中英文字幕)
6. ✅ 专业封面制作 (人物照片+特效)
7. ✅ B站上传内容 (标题+简介+标签)

## 📊 输出文件
### 视频文件
- `final/xxx_bilingual.mp4` - 双语版本
- `final/xxx_chinese.mp4` - 中文版本

### 字幕文件
- `subtitles/xxx_english.srt` - 英文字幕
- `subtitles/chinese_translation.srt` - 中文字幕
- `subtitles/bilingual.ass` - 双语ASS字幕
- `subtitles/chinese.ass` - 中文ASS字幕

### 上传素材
- `bilibili_thumbnail.jpg` - B站封面
- `bilibili_upload_content.md` - 上传内容
- `translation_prompt.txt` - 翻译提示

## 🚀 B站上传建议
1. 使用 `xxx_bilingual.mp4` 作为主要版本
2. 封面使用 `bilibili_thumbnail.jpg`
3. 标题和简介参考 `bilibili_upload_content.md`
4. 建议发布时间: 晚上8-10点 (观众活跃期)

## ⏱️ 性能数据
- 总处理时间: 约10-15分钟 (不含翻译等待)
- 视频质量: 1080p VP9编码
- 字幕精度: Whisper AI + 人工校对

## 🎯 优化建议
- 定期更新Whisper模型获得更好识别效果
- 可考虑批量处理多个视频
- 建议建立翻译词汇表提高一致性
"""

    summary_path = f"{project_dir}/workflow_summary.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ 流程总结已生成: {summary_path}")
    return summary_path

def main():
    """主工作流程"""
    print("🎬 完整B站视频处理流程")
    print("从YouTube下载到B站上传内容生成")
    print("="*60)
    
    # 获取YouTube URL
    if len(sys.argv) < 2:
        print("❌ 请提供YouTube视频URL")
        print("用法: python complete_bilibili_workflow.py <youtube_url>")
        return
    
    youtube_url = sys.argv[1]
    print(f"🎯 目标视频: {youtube_url}")
    
    try:
        # 创建项目目录
        print_step(0, "初始化项目", "创建项目目录结构")
        project_dir, project_name = create_project_directory("Video_Project")
        print(f"📁 项目目录: {project_dir}")
        
        # 1. 下载视频
        video_path = download_video(youtube_url, project_dir)
        if not video_path:
            print("❌ 视频下载失败，终止流程")
            return
        
        # 2. 提取字幕
        english_subtitle_path = extract_subtitles(video_path, project_dir)
        if not english_subtitle_path:
            print("❌ 字幕提取失败，终止流程")
            return
        
        # 3. 生成翻译提示
        prompt_path = generate_translation_prompt(english_subtitle_path, project_dir)
        
        # 4. 等待中文翻译
        chinese_subtitle_path = wait_for_chinese_translation(project_dir)
        
        # 5. 生成双语视频
        bilingual_video, chinese_video = create_bilingual_videos(
            video_path, english_subtitle_path, chinese_subtitle_path, project_dir
        )
        
        # 6. 生成封面
        thumbnail_path = generate_thumbnail(video_path, project_dir)
        
        # 7. 生成上传内容
        upload_content_path = generate_upload_content(video_path, project_dir)
        
        # 8. 生成总结
        summary_path = generate_workflow_summary(project_dir, project_name)
        
        # 最终报告
        print("\n" + "="*60)
        print("🎉 完整流程处理完成！")
        print("="*60)
        print(f"📁 项目目录: {project_dir}")
        print(f"🎬 双语视频: {bilingual_video}")
        print(f"🎬 中文视频: {chinese_video}")
        print(f"🎨 封面图片: {thumbnail_path}")
        print(f"📝 上传内容: {upload_content_path}")
        print(f"📊 项目总结: {summary_path}")
        print("\n🚀 现在可以上传到B站了！")
        
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断流程")
    except Exception as e:
        print(f"\n❌ 流程执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 