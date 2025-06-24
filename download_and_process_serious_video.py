#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频下载和政治喜剧处理脚本

从YouTube下载指定视频，截取特定时间段，然后应用政治喜剧UP主自动化工具处理
"""

import sys
import os
import subprocess
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from political_comedy_automation import PoliticalComedyAutomator

def main():
    print("📺 YouTube严肃视频政治喜剧处理")
    print("=" * 60)
    
    # 视频信息
    youtube_url = "https://www.youtube.com/watch?v=smemFVe0l5E"
    start_time = "50:00"  # 开始时间
    end_time = "50:40"    # 结束时间
    
    print(f"🔗 视频URL: {youtube_url}")
    print(f"⏰ 截取时间: {start_time} - {end_time} (40秒)")
    
    # 创建输出目录
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = f"political_comedy_output/serious_video_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 输出目录: {output_dir}")
    
    # 第一步：下载完整视频
    print(f"\n📥 第一步：下载YouTube视频...")
    temp_video = os.path.join(output_dir, "temp_full_video.%(ext)s")
    
    download_cmd = [
        "yt-dlp",
        "--format", "best[height<=720]",  # 最大720p
        "--output", temp_video,
        youtube_url
    ]
    
    print("执行视频下载...")
    try:
        result = subprocess.run(download_cmd, capture_output=True, text=True, check=True)
        print("✅ 视频下载成功")
        
        # 找到实际下载的文件
        downloaded_files = [f for f in os.listdir(output_dir) if f.startswith("temp_full_video")]
        if not downloaded_files:
            print("❌ 找不到下载的视频文件")
            return
        
        full_video_path = os.path.join(output_dir, downloaded_files[0])
        print(f"📹 下载文件: {downloaded_files[0]}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 视频下载失败: {e}")
        print(f"错误输出: {e.stderr}")
        return
    
    # 第二步：截取指定时间段
    print(f"\n✂️ 第二步：截取视频片段 ({start_time}-{end_time})...")
    clipped_video = os.path.join(output_dir, f"serious_video_clip_{timestamp}.mp4")
    
    # 将时间转换为秒数
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)
    duration = end_seconds - start_seconds
    
    clip_cmd = [
        "ffmpeg", "-y",
        "-i", full_video_path,
        "-ss", str(start_seconds),
        "-t", str(duration),
        "-c", "copy",  # 快速复制，不重新编码
        clipped_video
    ]
    
    print(f"截取 {duration} 秒片段...")
    try:
        result = subprocess.run(clip_cmd, capture_output=True, text=True, check=True)
        print("✅ 视频截取成功")
        
        # 删除原始大文件
        os.remove(full_video_path)
        print("🗑️ 清理原始大文件")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 视频截取失败: {e}")
        print(f"错误输出: {e.stderr}")
        return
    
    # 第三步：提取音频并生成英文字幕
    print(f"\n🔊 第三步：提取音频并生成字幕...")
    audio_file = os.path.join(output_dir, f"serious_video_audio_{timestamp}.wav")
    
    audio_cmd = [
        "ffmpeg", "-y",
        "-i", clipped_video,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_file
    ]
    
    try:
        result = subprocess.run(audio_cmd, capture_output=True, text=True, check=True)
        print("✅ 音频提取成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 音频提取失败: {e}")
        return
    
    # 第四步：初始化政治喜剧自动化工具
    print(f"\n🎭 第四步：初始化政治喜剧处理工具...")
    automator = PoliticalComedyAutomator()
    
    # 收集热梗
    print("🔥 收集当日热梗...")
    memes = automator.collect_daily_memes()
    current_memes = [meme.content for meme in memes]
    print(f"✅ 收集到 {len(memes)} 个热梗: {', '.join(current_memes[:3])}...")
    
    # 第五步：生成英文字幕（使用Whisper）
    print(f"\n📝 第五步：生成英文字幕...")
    english_srt = os.path.join(output_dir, f"serious_video_english_{timestamp}.srt")
    
    # 这里应该调用Whisper，简化处理，先创建模板
    print("⚠️ 注意：需要手动生成英文字幕或使用Whisper")
    create_english_subtitle_template(english_srt, duration)
    
    # 第六步：创建翻译模板，等待手动翻译
    print(f"\n✋ 第六步：创建中文翻译模板...")
    translation_template = os.path.join(output_dir, f"serious_video_translation_template_{timestamp}.srt")
    create_translation_template(english_srt, translation_template)
    
    # 第七步：生成政治喜剧提示词和弹幕
    print(f"\n🎭 第七步：生成政治喜剧内容...")
    
    video_info = {
        "title": "严肃政治话题片段",
        "duration": duration,
        "description": "从严肃政治视频中截取的40秒精彩片段",
        "characters": "政治人物、发言人、听众"
    }
    
    # 生成提示词
    translation_prompt = automator.prompt_manager.get_subtitle_translation_prompt("严肃政治话题")
    danmaku_prompt = automator.prompt_manager.get_danmaku_generation_prompt("严肃政治", current_memes[:5])
    copy_prompt = automator.prompt_manager.get_upload_copy_prompt(video_info, current_memes)
    
    print("✅ 政治喜剧提示词系统已生成")
    
    # 生成弹幕数据
    danmaku_data = generate_serious_video_danmaku(current_memes, duration)
    
    # 生成B站文案
    upload_copy = generate_serious_video_upload_copy(video_info, current_memes)
    
    # 第八步：保存所有处理结果
    print(f"\n💾 第八步：保存处理结果...")
    
    # 保存弹幕数据
    danmaku_file = os.path.join(output_dir, f"serious_video_danmaku_{timestamp}.json")
    with open(danmaku_file, 'w', encoding='utf-8') as f:
        json.dump(danmaku_data, f, ensure_ascii=False, indent=2)
    
    # 保存B站文案
    copy_file = os.path.join(output_dir, f"serious_video_bilibili_copy_{timestamp}.txt")
    with open(copy_file, 'w', encoding='utf-8') as f:
        f.write(f"标题: {upload_copy['title']}\n\n")
        f.write(f"简介:\n{upload_copy['description']}\n\n")
        f.write(f"标签: {', '.join(upload_copy['tags'])}\n\n")
        f.write("讨论话题:\n")
        for i, topic in enumerate(upload_copy['discussion_topics'], 1):
            f.write(f"{i}. {topic}\n")
    
    # 保存完整处理结果
    result_data = {
        "video_info": video_info,
        "youtube_url": youtube_url,
        "time_range": f"{start_time}-{end_time}",
        "memes_used": current_memes,
        "danmaku_data": danmaku_data,
        "upload_copy": upload_copy,
        "files": {
            "video": os.path.basename(clipped_video),
            "audio": os.path.basename(audio_file),
            "english_srt": os.path.basename(english_srt),
            "translation_template": os.path.basename(translation_template),
            "danmaku": os.path.basename(danmaku_file),
            "copy": os.path.basename(copy_file)
        },
        "processing_time": timestamp
    }
    
    result_file = os.path.join(output_dir, f"serious_video_processing_result_{timestamp}.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    # 创建README
    readme_content = f"""# 严肃政治视频政治喜剧处理结果

## 📺 视频信息
- **源视频**: {youtube_url}
- **截取时间**: {start_time} - {end_time} ({duration}秒)
- **处理时间**: {timestamp}

## 🎭 政治喜剧特色
- 💬 {len(danmaku_data)}条精心设计的弹幕
- 🔥 融入{len(current_memes)}个当前热梗
- 📢 专业B站政治喜剧文案
- ✋ 手动翻译质量控制

## 📁 文件说明
- `{os.path.basename(clipped_video)}` - 截取的视频片段
- `{os.path.basename(english_srt)}` - 英文字幕模板
- `{os.path.basename(translation_template)}` - 中文翻译模板（待填写）
- `{os.path.basename(danmaku_file)}` - 政治喜剧弹幕数据
- `{os.path.basename(copy_file)}` - B站上传文案

## 🔄 下一步操作
1. 完善英文字幕识别（可使用Whisper）
2. 手动填写中文翻译模板
3. 运行最终视频生成脚本

## 🎯 预期效果
严肃政治内容 + 网络化表达 = 既有教育意义又有娱乐性的内容

---
**工具**: 政治喜剧UP主自动化工具
**版本**: v1.0
"""
    
    readme_file = os.path.join(output_dir, "README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # 清理音频文件
    if os.path.exists(audio_file):
        os.remove(audio_file)
    
    # 第九步：展示处理结果
    print(f"\n🎉 严肃视频政治喜剧处理完成！")
    print(f"📂 输出目录: {output_dir}")
    print(f"📊 处理结果:")
    print(f"   📹 视频片段: {os.path.basename(clipped_video)} ({duration}秒)")
    print(f"   📝 翻译模板: {os.path.basename(translation_template)}")
    print(f"   💬 弹幕数量: {len(danmaku_data)}条")
    print(f"   🔥 使用热梗: {len(current_memes)}个")
    print(f"   📢 B站文案: {upload_copy['title']}")
    
    print(f"\n🎭 政治喜剧特色预览:")
    print(f"📋 B站标题: {upload_copy['title']}")
    print(f"💬 弹幕亮点:")
    for dm in danmaku_data[:5]:
        print(f"   {dm['time']}s: {dm['text']} ({dm['type']})")
    
    print(f"\n⚠️ 重要提醒:")
    print(f"   1. 请完善英文字幕识别（建议使用Whisper）")
    print(f"   2. 手动填写中文翻译模板文件")
    print(f"   3. 然后可运行最终视频生成脚本")
    
    return output_dir

def time_to_seconds(time_str):
    """将时间字符串转换为秒数"""
    parts = time_str.split(':')
    if len(parts) == 2:  # MM:SS
        minutes, seconds = parts
        return int(minutes) * 60 + int(seconds)
    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    else:
        return int(time_str)

def create_english_subtitle_template(srt_path, duration):
    """创建英文字幕模板"""
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write("1\n")
        f.write("00:00:00,000 --> 00:00:10,000\n")
        f.write("[需要使用Whisper或手动识别英文语音]\n\n")
        
        f.write("2\n")
        f.write("00:00:10,000 --> 00:00:20,000\n")
        f.write("[请在此添加第二段英文字幕]\n\n")
        
        # 根据时长添加更多条目
        segment_count = max(2, int(duration / 10))
        for i in range(3, segment_count + 1):
            start_time = (i-1) * 10
            end_time = min(i * 10, duration)
            
            f.write(f"{i}\n")
            f.write(f"00:00:{start_time:02d},000 --> 00:00:{end_time:02d},000\n")
            f.write(f"[请在此添加第{i}段英文字幕]\n\n")

def create_translation_template(english_srt, template_path):
    """创建翻译模板"""
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write("# 中文翻译模板\n")
        f.write("# 请根据英文字幕填写对应的政治喜剧风格中文翻译\n\n")
        
        f.write("1\n")
        f.write("00:00:00,000 --> 00:00:10,000\n")
        f.write("EN: [英文内容]\n")
        f.write("CN: [请在此添加政治喜剧风格中文翻译]\n\n")
        
        f.write("2\n")
        f.write("00:00:10,000 --> 00:00:20,000\n")
        f.write("EN: [英文内容]\n")
        f.write("CN: [请在此添加政治喜剧风格中文翻译]\n\n")

def generate_serious_video_danmaku(memes, duration):
    """为严肃视频生成政治喜剧弹幕"""
    danmaku_list = []
    
    # 开场弹幕
    danmaku_list.append({"time": 2, "text": "严肃时刻开始了", "type": "开场型"})
    danmaku_list.append({"time": 5, "text": f"{memes[0] if memes else '又来了'}", "type": "热梗型"})
    
    # 根据时长生成弹幕
    interval = max(3, duration / 8)  # 确保有足够的弹幕间隔
    
    serious_comments = [
        "这表情很认真啊",
        "关键时刻来了",
        "重要发言预警",
        "认真脸模式开启",
        "这波分析到位",
        "专业解读时间",
        "深度内容来了",
        "这就是实力"
    ]
    
    for i, comment in enumerate(serious_comments):
        time_point = int(8 + i * interval)
        if time_point < duration - 3:
            danmaku_list.append({
                "time": time_point,
                "text": comment,
                "type": "解说型"
            })
    
    # 穿插热梗
    if len(memes) > 1:
        mid_time = int(duration / 2)
        danmaku_list.append({"time": mid_time, "text": memes[1], "type": "热梗型"})
    
    # 结尾弹幕
    if duration > 30:
        danmaku_list.append({"time": int(duration - 5), "text": "精彩内容结束", "type": "总结型"})
    
    return sorted(danmaku_list, key=lambda x: x['time'])

def generate_serious_video_upload_copy(video_info, memes):
    """生成严肃视频的B站政治喜剧文案"""
    return {
        "title": f"【{memes[0] if memes else '深度解读'}】严肃政治时刻精选 - 这波分析很到位",
        "description": f"""🔥 又是一期政治深度内容！

📺 本期看点：
- 严肃政治场合的精彩40秒
- 关键发言和重要时刻
- 专业解读+网友视角双重体验

🎯 这期内容比较硬核，但是{memes[1] if len(memes) > 1 else '真的值得看'}！

💬 评论区话题：
1. 这段发言你们怎么理解？
2. 还有哪些类似的经典时刻？
3. 严肃内容也能这样看吗？

🎭 严肃内容轻松看，教育娱乐两不误！

👍 觉得有意思就一键三连吧！
🔔 关注UP主，严肃内容轻松看~

💡 本频道专注政治内容轻量化解读，寓教于乐！

#政治解读 #严肃内容 #深度分析 #{memes[2] if len(memes) > 2 else '教育内容'}""",
        "tags": [
            "政治", "严肃", "解读", "分析", "教育",
            "深度", "政治解读", "时事", "学习", "知识"
        ] + memes[:3],
        "cover_text": f"【{memes[0] if memes else '深度解读'}】严肃政治精选",
        "discussion_topics": [
            "这段发言你们怎么理解？",
            "还有哪些类似的经典时刻？",
            "严肃内容用这种方式看合适吗？"
        ]
    }

if __name__ == "__main__":
    main() 