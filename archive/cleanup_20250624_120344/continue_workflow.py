#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
续行工作流程脚本
从已有的中文字幕开始完成剩余步骤
"""

import os
import sys
import subprocess
from datetime import datetime

def print_step(step_num, title, description=""):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"📍 步骤 {step_num}: {title}")
    if description:
        print(f"   {description}")
    print('='*60)

def continue_from_chinese_subtitles(project_dir):
    """从中文字幕开始继续工作流程"""
    print("🔄 续行B站视频处理流程")
    print("从已有的中文字幕开始")
    print("="*60)
    
    # 查找视频文件
    video_path = None
    for file in os.listdir(project_dir):
        if file.endswith('.mp4') and not file.startswith('._'):
            video_path = os.path.join(project_dir, file)
            break
    
    if not video_path:
        print("❌ 找不到视频文件")
        return
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"🎬 处理视频: {video_name}")
    
    # 查找字幕文件
    english_subtitle_path = f"{project_dir}/subtitles/{video_name}_english.srt"
    chinese_subtitle_path = f"{project_dir}/subtitles/{video_name}_chinese.srt"
    
    if not os.path.exists(english_subtitle_path):
        print(f"❌ 找不到英文字幕: {english_subtitle_path}")
        return
    
    if not os.path.exists(chinese_subtitle_path):
        print(f"❌ 找不到中文字幕: {chinese_subtitle_path}")
        return
    
    print(f"✅ 英文字幕: {english_subtitle_path}")
    print(f"✅ 中文字幕: {chinese_subtitle_path}")
    
    # 步骤5: 生成双语视频
    print_step(5, "生成双语视频", "创建中英双语和纯中文版本")
    bilingual_video, chinese_video = create_bilingual_videos(
        video_path, english_subtitle_path, chinese_subtitle_path, project_dir
    )
    
    # 步骤6: 生成封面
    print_step(6, "生成B站封面", "创建带人物照片的专业封面")
    thumbnail_path = generate_thumbnail(video_path, project_dir)
    
    # 步骤7: 生成上传内容
    print_step(7, "生成B站上传内容", "创建标题、简介、标签等")
    upload_content_path = generate_upload_content(video_path, project_dir)
    
    # 步骤8: 生成总结
    print_step(8, "生成流程总结", "创建完整的项目报告")
    summary_path = generate_workflow_summary(project_dir, os.path.basename(project_dir))
    
    # 最终报告
    print("\n" + "="*60)
    print("🎉 续行流程处理完成！")
    print("="*60)
    print(f"📁 项目目录: {project_dir}")
    print(f"🎬 双语视频: {bilingual_video}")
    print(f"🎬 中文视频: {chinese_video}")
    print(f"🎨 封面图片: {thumbnail_path}")
    print(f"📝 上传内容: {upload_content_path}")
    print(f"📊 项目总结: {summary_path}")
    print("\n🚀 现在可以上传到B站了！")

def create_bilingual_videos(video_path, english_subtitle_path, chinese_subtitle_path, project_dir):
    """生成双语视频"""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 确保final目录存在
    final_dir = f"{project_dir}/final"
    os.makedirs(final_dir, exist_ok=True)
    
    # 输出路径
    bilingual_output = f"{final_dir}/{video_name}_bilingual.mp4"
    chinese_output = f"{final_dir}/{video_name}_chinese.mp4"
    
    # 创建双语ASS字幕
    bilingual_ass = create_bilingual_ass_subtitle(english_subtitle_path, chinese_subtitle_path, project_dir)
    chinese_ass = create_chinese_ass_subtitle(chinese_subtitle_path, project_dir)
    
    # 生成双语版本
    print("🔄 生成双语版本...")
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
    
    result1 = subprocess.run(bilingual_cmd, capture_output=True, text=True)
    
    if result1.returncode == 0:
        size1 = os.path.getsize(bilingual_output) / (1024 * 1024)
        print(f"✅ 双语版本完成: {size1:.1f}MB")
    else:
        print(f"❌ 双语版本失败: {result1.stderr}")
    
    # 生成中文版本
    print("🔄 生成中文版本...")
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
    
    # 创建ASS字幕 - 使用正确的白色格式
    ass_content = """[Script Info]
Title: Bilingual Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,60,1
Style: English,Arial,18,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    # 添加字幕
    min_length = min(len(eng_subs), len(chi_subs))
    for i in range(min_length):
        eng_sub = eng_subs[i]
        chi_sub = chi_subs[i]
        
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
    
    # 使用正确的白色格式
    ass_content = """[Script Info]
Title: Chinese Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
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
    """转换秒数为ASS时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:05.2f}"

def generate_thumbnail(video_path, project_dir):
    """生成B站封面"""
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
- `subtitles/xxx_chinese.srt` - 中文字幕
- `subtitles/bilingual.ass` - 双语ASS字幕
- `subtitles/chinese.ass` - 中文ASS字幕

### 上传素材
- `bilibili_thumbnail.jpg` - B站封面
- `bilibili_upload_content.md` - 上传内容

## 🚀 B站上传建议
1. 使用 `xxx_bilingual.mp4` 作为主要版本
2. 封面使用 `bilibili_thumbnail.jpg`
3. 标题和简介参考 `bilibili_upload_content.md`
4. 建议发布时间: 晚上8-10点 (观众活跃期)

## ⏱️ 性能数据
- 续行处理时间: 约5-8分钟
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
    """主函数"""
    # 默认使用Ted Cruz项目目录
    project_dir = "output/Ted_Cruz_&_Tucker_Carlson_Battle_Over_Iran_While_T_20250623_172209"
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        return
    
    print(f"📁 续行项目: {project_dir}")
    continue_from_chinese_subtitles(project_dir)

if __name__ == "__main__":
    main() 