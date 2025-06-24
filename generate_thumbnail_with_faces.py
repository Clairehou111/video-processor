#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带人物照片的B站封面生成器
从视频中提取关键帧，制作专业封面
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import os
import numpy as np

def extract_frames_from_video(video_path, times=[30, 60, 120]):
    """从视频中提取指定时间点的帧"""
    print(f"🎬 从视频中提取关键帧: {os.path.basename(video_path)}")
    
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ 无法打开视频文件")
        return frames
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    for time_sec in times:
        frame_number = int(fps * time_sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        ret, frame = cap.read()
        if ret:
            # 转换BGR到RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append((time_sec, frame_rgb))
            print(f"✅ 提取 {time_sec}s 处的帧")
        else:
            print(f"⚠️ 无法提取 {time_sec}s 处的帧")
    
    cap.release()
    return frames

def create_person_cutout(frame, position='left', size=(300, 400)):
    """从帧中创建人物剪影"""
    height, width = frame.shape[:2]
    
    # 根据位置选择区域
    if position == 'left':
        # 左侧人物 (假设Ted Cruz在左边)
        start_x = int(width * 0.1)
        end_x = int(width * 0.4)
    else:
        # 右侧人物 (假设Tucker Carlson在右边)
        start_x = int(width * 0.6)
        end_x = int(width * 0.9)
    
    start_y = int(height * 0.1)
    end_y = int(height * 0.9)
    
    # 裁剪人物区域
    person_region = frame[start_y:end_y, start_x:end_x]
    
    # 转换为PIL图像
    pil_image = Image.fromarray(person_region)
    
    # 调整大小
    pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
    
    # 添加圆角效果
    pil_image = add_rounded_corners(pil_image, radius=20)
    
    return pil_image

def add_rounded_corners(image, radius):
    """添加圆角效果"""
    # 创建圆角遮罩
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], 
                          radius=radius, fill=255)
    
    # 应用遮罩
    result = Image.new('RGBA', image.size, (0, 0, 0, 0))
    result.paste(image, (0, 0))
    result.putalpha(mask)
    
    return result

def create_enhanced_thumbnail(video_path, output_path="enhanced_thumbnail.jpg"):
    """生成带人物照片的增强封面"""
    print("🎨 开始生成增强版B站封面...")
    
    # 从视频提取关键帧
    frames = extract_frames_from_video(video_path, times=[30, 60, 120])
    
    if len(frames) < 2:
        print("⚠️ 提取的帧数不足，将生成简化版封面")
        return create_simple_thumbnail(output_path)
    
    # 创建画布
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # 创建渐变背景
    create_gradient_background(img, draw, width, height)
    
    # 添加人物照片
    add_character_photos(img, frames, width, height)
    
    # 添加主标题和特效
    add_enhanced_title(img, draw, width, height)
    
    # 添加副标题
    add_subtitle(img, draw, width, height)
    
    # 添加爆炸特效
    add_explosion_effects(img, draw, width, height)
    
    # 添加品牌标识
    add_show_branding(img, draw, width, height)
    
    # 保存
    img.save(output_path, 'JPEG', quality=95)
    print(f"✅ 增强封面已生成: {output_path}")
    
    return output_path

def add_character_photos(img, frames, width, height):
    """添加人物照片到封面"""
    if len(frames) >= 2:
        # 使用第一帧和第二帧
        frame1 = frames[0][1]  # Ted Cruz (左侧)
        frame2 = frames[1][1]  # Tucker Carlson (右侧)
        
        # 创建人物剪影
        ted_cutout = create_person_cutout(frame1, 'left', (280, 350))
        tucker_cutout = create_person_cutout(frame2, 'right', (280, 350))
        
        # 添加阴影效果
        ted_shadow = create_shadow(ted_cutout)
        tucker_shadow = create_shadow(tucker_cutout)
        
        # 计算位置
        ted_x = width // 8
        ted_y = height // 2 - 100
        
        tucker_x = width - width // 8 - 280
        tucker_y = height // 2 - 50
        
        # 粘贴阴影
        img.paste(ted_shadow, (ted_x + 10, ted_y + 10), ted_shadow)
        img.paste(tucker_shadow, (tucker_x + 10, tucker_y + 10), tucker_shadow)
        
        # 粘贴主图
        img.paste(ted_cutout, (ted_x, ted_y), ted_cutout)
        img.paste(tucker_cutout, (tucker_x, tucker_y), tucker_cutout)
        
        # 添加人物标签
        add_character_labels(img, ted_x, ted_y, tucker_x, tucker_y, width, height)

def create_shadow(image):
    """创建阴影效果"""
    # 创建黑色版本
    shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    
    # 如果原图有alpha通道，使用它创建阴影
    if image.mode == 'RGBA':
        # 创建黑色阴影
        shadow.paste((0, 0, 0, 128), (0, 0), image)
        # 模糊阴影
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    
    return shadow

def add_character_labels(img, ted_x, ted_y, tucker_x, tucker_y, width, height):
    """添加人物标签"""
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 32)
    except:
        font = ImageFont.load_default()
    
    # Ted Cruz 标签 (带表情)
    ted_label = "Ted Cruz 😅"
    label_bg_color = '#ff4444'
    
    # 计算标签位置
    ted_label_x = ted_x
    ted_label_y = ted_y - 50
    
    # 绘制标签背景
    bbox = draw.textbbox((ted_label_x, ted_label_y), ted_label, font=font)
    padding = 8
    draw.rounded_rectangle([bbox[0]-padding, bbox[1]-padding, 
                           bbox[2]+padding, bbox[3]+padding], 
                          radius=15, fill=label_bg_color)
    
    # 绘制标签文字
    draw.text((ted_label_x, ted_label_y), ted_label, font=font, fill='white')
    
    # Tucker Carlson 标签 (带表情)
    tucker_label = "Tucker Carlson 🤔"
    tucker_label_x = tucker_x
    tucker_label_y = tucker_y - 50
    
    # 绘制标签背景
    bbox = draw.textbbox((tucker_label_x, tucker_label_y), tucker_label, font=font)
    draw.rounded_rectangle([bbox[0]-padding, bbox[1]-padding, 
                           bbox[2]+padding, bbox[3]+padding], 
                          radius=15, fill='#4444ff')
    
    # 绘制标签文字
    draw.text((tucker_label_x, tucker_label_y), tucker_label, font=font, fill='white')

def add_enhanced_title(img, draw, width, height):
    """添加增强版标题"""
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 100)
    except:
        title_font = ImageFont.load_default()
    
    main_text = "被爆破了"
    
    # 位置
    x = width // 3
    y = height // 6
    
    # 多层阴影效果
    for offset in [8, 6, 4, 2]:
        shadow_color = f'#{20:02x}{20:02x}{20:02x}'
        draw.text((x + offset, y + offset), main_text, 
                 font=title_font, fill=shadow_color)
    
    # 外描边
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), main_text, 
                         font=title_font, fill='#000000')
    
    # 主文字 (渐变效果用纯红色替代)
    draw.text((x, y), main_text, font=title_font, fill='#ff2222')

def add_explosion_effects(img, draw, width, height):
    """添加爆炸特效"""
    # 💥 符号效果
    try:
        explosion_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
    except:
        explosion_font = ImageFont.load_default()
    
    explosion_positions = [
        (width * 0.7, height * 0.25),
        (width * 0.8, height * 0.45),
        (width * 0.75, height * 0.65)
    ]
    
    for x, y in explosion_positions:
        # 阴影
        draw.text((x + 3, y + 3), "💥", font=explosion_font, fill='#000000')
        # 主体
        draw.text((x, y), "💥", font=explosion_font, fill='#ffff00')
    
    # 添加闪光线条
    for i in range(8):
        start_x = width * 0.75
        start_y = height * 0.4
        
        import math
        angle = i * (2 * math.pi / 8)
        end_x = start_x + 80 * math.cos(angle)
        end_y = start_y + 80 * math.sin(angle)
        
        draw.line([(start_x, start_y), (end_x, end_y)], 
                 fill='#ffff44', width=4)

def create_gradient_background(img, draw, width, height):
    """创建渐变背景"""
    for y in range(height):
        # 深蓝到深红的政治色彩渐变
        blue_ratio = 1 - (y / height)
        red_ratio = y / height
        
        r = int(20 + red_ratio * 80)
        g = int(20 + blue_ratio * 15)
        b = int(40 + blue_ratio * 80)
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        draw.line([(0, y), (width, y)], fill=color)

def add_subtitle(img, draw, width, height):
    """添加副标题"""
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 48)
    except:
        font = ImageFont.load_default()
    
    subtitle = "连人口都不知道还想开战？"
    
    x = width // 3
    y = height // 6 + 130
    
    # 阴影
    draw.text((x + 2, y + 2), subtitle, font=font, fill='#000000')
    # 主文字
    draw.text((x, y), subtitle, font=font, fill='#ffffff')

def add_show_branding(img, draw, width, height):
    """添加节目标识"""
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
    except:
        font = ImageFont.load_default()
    
    # Daily Show精选
    branding = "Daily Show精选"
    x = width - 280
    y = height - 80
    
    bbox = draw.textbbox((x, y), branding, font=font)
    padding = 8
    draw.rounded_rectangle([bbox[0]-padding, bbox[1]-padding, 
                           bbox[2]+padding, bbox[3]+padding], 
                          radius=10, fill='#000000', outline='#ffffff', width=2)
    draw.text((x, y), branding, font=font, fill='#ffffff')
    
    # 董卓主演脱口秀水印
    watermark = "董卓主演脱口秀"
    wm_x = width - 250
    wm_y = 25
    
    draw.text((wm_x + 1, wm_y + 1), watermark, font=font, fill='#000000')
    draw.text((wm_x, wm_y), watermark, font=font, fill='#ffffff')

def create_simple_thumbnail(output_path):
    """创建简化版封面（无人物照片）"""
    print("🎨 生成简化版封面...")
    
    # 复用之前的简化逻辑
    from generate_thumbnail import create_bilibili_thumbnail
    return create_bilibili_thumbnail(output_path)

def main():
    """主函数"""
    print("🎨 增强版B站封面生成器")
    print("特色: 自动提取视频人物照片")
    print("="*50)
    
    # 项目目录
    project_dir = "output/Ted_Cruz_&_Tucker_Carlson_Battle_Over_Iran_While_T_20250623_172209"
    video_path = f"{project_dir}/Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show.mp4"
    output_path = f"{project_dir}/enhanced_bilibili_thumbnail.jpg"
    
    if not os.path.exists(video_path):
        print(f"❌ 找不到视频文件: {video_path}")
        return
    
    # 生成增强封面
    create_enhanced_thumbnail(video_path, output_path)
    
    print(f"\n📁 增强封面已保存: {output_path}")
    print("📏 尺寸: 1920x1080")
    print("📊 格式: JPEG (高质量)")
    print("🎯 包含真实人物照片")
    print("💫 带有特效和标签")

if __name__ == "__main__":
    main() 