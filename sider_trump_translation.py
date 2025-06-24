#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Sider AI翻译特朗普搞笑字幕
包含专业提示词，使用Claude Sonnet 4模型
"""

import os
import time

def read_trump_subtitles():
    """读取特朗普视频的英文字幕"""
    subtitle_file = "output/sider__jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_english.srt"
    
    if not os.path.exists(subtitle_file):
        print(f"❌ 字幕文件不存在: {subtitle_file}")
        return None
    
    # 读取字幕并提取英文文本
    english_texts = []
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 解析SRT格式，提取英文文本
    for i, line in enumerate(lines):
        line = line.strip()
        # 跳过序号行和时间行
        if line and not line.isdigit() and '-->' not in line and line:
            english_texts.append(line)
    
    return english_texts

def create_sider_translation_prompt(english_texts):
    """创建Sider翻译的专业提示词"""
    
    # 将所有英文文本合并
    full_english_text = '\n'.join(english_texts)
    
    prompt = f"""请使用Claude Sonnet 4模型翻译以下特朗普视频字幕。

翻译要求：
1. 这些字幕来自特朗普拍摄前的幕后花絮，非常搞笑和轻松
2. 请使用幽默风趣的中文翻译，保持轻松愉快的氛围
3. 保持特朗普独特的说话风格和语气
4. 整个文本作为一个整体进行翻译，保持上下文连贯性
5. 突出搞笑和轻松的元素

英文字幕原文：
{full_english_text}

请将以上内容翻译成中文，保持幽默感和特朗普的独特风格。"""

    return prompt, full_english_text

def save_translation_prompt(prompt, filename="sider_translation_prompt.txt"):
    """保存翻译提示词到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("🌟 Sider AI特朗普搞笑字幕翻译提示词\n")
        f.write("=" * 60 + "\n")
        f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("目标模型: Claude Sonnet 4\n")
        f.write("翻译类型: 搞笑幽默风格\n")
        f.write("=" * 60 + "\n\n")
        f.write(prompt)
    
    print(f"📝 翻译提示词已保存到: {filename}")

def main():
    """主函数"""
    print("🎬 特朗普搞笑字幕Sider翻译准备器")
    print("=" * 50)
    print("🎯 目标: 创建专业的Sider翻译提示词")
    print("🤖 模型: Claude Sonnet 4")
    print("😄 风格: 幽默搞笑")
    print("📝 方式: 整体翻译")
    print("=" * 50)
    
    # 1. 读取特朗普字幕
    print("📖 正在读取特朗普视频字幕...")
    english_texts = read_trump_subtitles()
    
    if not english_texts:
        print("❌ 无法读取字幕文件")
        return
    
    print(f"✅ 成功读取 {len(english_texts)} 条英文字幕")
    
    # 2. 创建翻译提示词
    print("🎯 正在创建Sider翻译提示词...")
    prompt, full_text = create_sider_translation_prompt(english_texts)
    
    # 3. 保存提示词
    save_translation_prompt(prompt)
    
    # 4. 显示预览
    print("\n📋 特朗普搞笑字幕预览:")
    print("-" * 40)
    for i, text in enumerate(english_texts[:5], 1):
        print(f"{i}. {text}")
    if len(english_texts) > 5:
        print(f"... 还有 {len(english_texts) - 5} 条字幕")
    
    print(f"\n🎯 下一步操作:")
    print("1. 复制 sider_translation_prompt.txt 中的提示词")
    print("2. 在Cursor中使用Sider工具进行翻译")
    print("3. 使用Claude Sonnet 4模型")
    print("4. 完成后返回翻译结果")
    
    return {
        "prompt": prompt,
        "english_texts": english_texts,
        "full_text": full_text,
        "status": "ready_for_sider_translation"
    }

if __name__ == "__main__":
    result = main()
    print(f"\n✅ 准备完成！请使用Sider工具进行翻译。") 