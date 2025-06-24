#!/usr/bin/env python3
"""
干净版封面制作脚本
基于75秒处视频帧，去掉多余装饰元素
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import cv2
import os

def extract_video_frame(video_path, frame_time=75):
    """从视频中提取指定时间的帧"""
    cap = cv2.VideoCapture(video_path)
    
    # 获取视频总时长
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if fps > 0 else 0
    
    print(f"视频总时长: {duration:.1f}秒")
    
    # 设置到指定时间（秒）
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # 转换颜色空间从BGR到RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 转换为PIL Image
        pil_image = Image.fromarray(frame_rgb)
        print(f"成功提取 {frame_time}秒 处的视频帧")
        return pil_image
    else:
        print(f"无法提取 {frame_time}秒 处的视频帧")
        return None

def create_clean_thumbnail():
    """创建干净版封面（75秒处，无多余装饰）"""
    
    video_path = 'output/bilibili_hd_dual_2min37s.mp4'
    
    # 提取75秒处的视频帧
    frame = extract_video_frame(video_path, frame_time=75)
    if frame is None:
        print("使用默认背景...")
        frame = Image.new('RGB', (1920, 1080), color=(30, 50, 100))
    
    # 调整到标准封面尺寸
    width, height = 1920, 1080
    frame = frame.resize((width, height), Image.Resampling.LANCZOS)
    
    # 轻微增强对比度和亮度
    enhancer = ImageEnhance.Contrast(frame)
    frame = enhancer.enhance(1.1)  # 轻微增加对比度
    
    enhancer = ImageEnhance.Brightness(frame)
    frame = enhancer.enhance(0.85)  # 稍微降低亮度
    
    # 创建轻微的渐变叠加层
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # 创建从上到下的轻微渐变
    for y in range(height):
        alpha = int(100 * (y / height))  # 更轻的渐变效果
        overlay_draw.rectangle([0, y, width, y+1], fill=(0, 0, 0, alpha))
    
    frame = frame.convert('RGBA')
    frame = Image.alpha_composite(frame, overlay).convert('RGB')
    
    draw = ImageDraw.Draw(frame)
    
    # 字体设置
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 55)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        accent_font = ImageFont.load_default()
    
    # 高级阴影效果
    def draw_text_with_glow(draw, text, position, font, fill_color, glow_color=(0, 0, 0)):
        x, y = position
        # 多层阴影创建发光效果
        for offset in [(5, 5), (3, 3), (1, 1)]:
            draw.text((x + offset[0], y + offset[1]), text, font=font, fill=glow_color)
        # 主文字
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 主标题：特朗普的哈里·温斯顿袖扣？
    title_text = "特朗普的哈里·温斯顿袖扣？"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw_text_with_glow(
        draw, title_text, 
        ((width - title_width) // 2, 120),
        title_font, 
        (255, 255, 255)
    )
    
    # 副标题：查理·辛：假货
    subtitle_text = "查理·辛：假货"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw_text_with_glow(
        draw, subtitle_text, 
        ((width - subtitle_width) // 2, 220),
        subtitle_font, 
        (255, 120, 120)
    )
    
    # 简洁的装饰边框
    border_color = (255, 215, 0)  # 金色
    border_width = 8
    
    # 边框
    draw.rectangle([20, 20, width-20, 20+border_width], fill=border_color)
    draw.rectangle([20, height-20-border_width, width-20, height-20], fill=border_color)
    draw.rectangle([20, 20, 20+border_width, height-20], fill=border_color)
    draw.rectangle([width-20-border_width, 20, width-20, height-20], fill=border_color)
    
    # 水印（简洁版）
    watermark = "董卓主演脱口秀"
    watermark_bbox = draw.textbbox((0, 0), watermark, font=accent_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    draw_text_with_glow(
        draw, watermark, 
        (width - watermark_width - 50, height - 70),
        accent_font, 
        (255, 255, 255)
    )
    
    return frame

def create_clean_tiktok_thumbnail():
    """创建干净版TikTok竖屏封面"""
    
    video_path = 'output/tiktok_version_2min37s.mp4'
    
    # 提取75秒处的视频帧
    frame = extract_video_frame(video_path, frame_time=75)
    if frame is None:
        print("使用默认背景...")
        frame = Image.new('RGB', (1080, 1920), color=(30, 50, 100))
    
    # 调整到TikTok尺寸
    width, height = 1080, 1920
    frame = frame.resize((width, height), Image.Resampling.LANCZOS)
    
    # 轻微增强
    enhancer = ImageEnhance.Contrast(frame)
    frame = enhancer.enhance(1.1)
    
    enhancer = ImageEnhance.Brightness(frame)
    frame = enhancer.enhance(0.85)
    
    # 创建轻微叠加层
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 80))
    frame = frame.convert('RGBA')
    frame = Image.alpha_composite(frame, overlay).convert('RGB')
    
    draw = ImageDraw.Draw(frame)
    
    # 字体设置
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 58)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 42)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        accent_font = ImageFont.load_default()
    
    # 阴影效果
    def draw_text_with_shadow(draw, text, position, font, fill_color, shadow_color=(0, 0, 0)):
        x, y = position
        for offset in [(3, 3), (1, 1)]:
            draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 分行显示文案
    title_line1 = "特朗普的哈里·温斯顿"
    title_line2 = "袖扣？"
    subtitle_line1 = "查理·辛："
    subtitle_line2 = "假货"
    
    # 第一行
    bbox1 = draw.textbbox((0, 0), title_line1, font=title_font)
    width1 = bbox1[2] - bbox1[0]
    draw_text_with_shadow(draw, title_line1, ((width - width1) // 2, 250), 
                         title_font, (255, 255, 255))
    
    # 第二行
    bbox2 = draw.textbbox((0, 0), title_line2, font=title_font)
    width2 = bbox2[2] - bbox2[0]
    draw_text_with_shadow(draw, title_line2, ((width - width2) // 2, 320), 
                         title_font, (255, 255, 255))
    
    # 副标题第一行
    bbox3 = draw.textbbox((0, 0), subtitle_line1, font=subtitle_font)
    width3 = bbox3[2] - bbox3[0]
    draw_text_with_shadow(draw, subtitle_line1, ((width - width3) // 2, 420), 
                         subtitle_font, (255, 255, 120))
    
    # 副标题第二行
    bbox4 = draw.textbbox((0, 0), subtitle_line2, font=subtitle_font)
    width4 = bbox4[2] - bbox4[0]
    draw_text_with_shadow(draw, subtitle_line2, ((width - width4) // 2, 480), 
                         subtitle_font, (255, 120, 120))
    
    # 简洁边框
    border_width = 6
    border_color = (255, 215, 0)
    draw.rectangle([15, 15, width-15, 15+border_width], fill=border_color)
    draw.rectangle([15, height-15-border_width, width-15, height-15], fill=border_color)
    draw.rectangle([15, 15, 15+border_width, height-15], fill=border_color)
    draw.rectangle([width-15-border_width, 15, width-15, height-15], fill=border_color)
    
    # 水印
    watermark = "@董卓主演脱口秀"
    wb_bbox = draw.textbbox((0, 0), watermark, font=accent_font)
    wb_width = wb_bbox[2] - wb_bbox[0]
    draw_text_with_shadow(draw, watermark, ((width - wb_width) // 2, height - 80), 
                         accent_font, (255, 255, 255))
    
    return frame

def main():
    """主函数"""
    print("开始制作干净版封面（75秒处）...")
    
    os.makedirs('output', exist_ok=True)
    
    # 创建横屏封面
    try:
        thumbnail = create_clean_thumbnail()
        thumbnail_path = 'output/clean_thumbnail_75s.jpg'
        thumbnail.save(thumbnail_path, 'JPEG', quality=95)
        print(f"干净版横屏封面已保存: {thumbnail_path}")
        
        # PNG版本
        png_path = 'output/clean_thumbnail_75s.png'
        thumbnail.save(png_path, 'PNG')
        print(f"PNG版本已保存: {png_path}")
        
    except Exception as e:
        print(f"创建横屏封面时出错: {e}")
    
    # 创建竖屏封面
    try:
        tiktok_thumbnail = create_clean_tiktok_thumbnail()
        tiktok_path = 'output/clean_tiktok_thumbnail_75s.jpg'
        tiktok_thumbnail.save(tiktok_path, 'JPEG', quality=95)
        print(f"干净版TikTok封面已保存: {tiktok_path}")
        
        # PNG版本
        tiktok_png = 'output/clean_tiktok_thumbnail_75s.png'
        tiktok_thumbnail.save(tiktok_png, 'PNG')
        print(f"TikTok PNG版本已保存: {tiktok_png}")
        
    except Exception as e:
        print(f"创建竖屏封面时出错: {e}")
    
    print("干净版封面制作完成！")

if __name__ == "__main__":
    main() 