#!/usr/bin/env python3
"""
TikTok竖屏封面制作脚本
为查理·辛讲述川普假铂金袖扣的故事制作竖屏封面
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_tiktok_thumbnail():
    """创建TikTok竖屏封面"""
    
    # TikTok封面尺寸 (9:16 比例)
    width, height = 1080, 1920
    
    # 创建渐变背景
    img = Image.new('RGB', (width, height), color='white')
    
    # 创建渐变背景 (从深紫到深蓝)
    for y in range(height):
        # 计算渐变色
        ratio = y / height
        r = int(40 + (20 - 40) * ratio)
        g = int(20 + (40 - 20) * ratio)  
        b = int(80 + (120 - 80) * ratio)
        
        # 绘制渐变线条
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    
    draw = ImageDraw.Draw(img)
    
    # 尝试加载中文字体
    try:
        # macOS 系统中文字体
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 70)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 45)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 35)
        watermark_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)
    except:
        try:
            # 备用字体
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 70)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 45)
            accent_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 35)
            watermark_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 30)
        except:
            # 默认字体
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            accent_font = ImageFont.load_default()
            watermark_font = ImageFont.load_default()
    
    # 添加阴影效果的文字函数
    def draw_text_with_shadow(draw, text, position, font, fill_color, shadow_color, shadow_offset=(3, 3)):
        x, y = position
        # 绘制阴影
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
        # 绘制主文字
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 主标题 - 分行显示
    title_line1 = "查理·辛"
    title_line2 = "揭露川普"
    
    # 第一行标题
    title1_bbox = draw.textbbox((0, 0), title_line1, font=title_font)
    title1_width = title1_bbox[2] - title1_bbox[0]
    draw_text_with_shadow(
        draw, title_line1, 
        ((width - title1_width) // 2, 300),
        title_font, 
        (255, 255, 255), 
        (0, 0, 0)
    )
    
    # 第二行标题
    title2_bbox = draw.textbbox((0, 0), title_line2, font=title_font)
    title2_width = title2_bbox[2] - title2_bbox[0]
    draw_text_with_shadow(
        draw, title_line2, 
        ((width - title2_width) // 2, 380),
        title_font, 
        (255, 255, 255), 
        (0, 0, 0)
    )
    
    # 副标题 - 分行显示
    subtitle_line1 = "假铂金袖扣"
    subtitle_line2 = "的真相"
    
    # 第一行副标题
    sub1_bbox = draw.textbbox((0, 0), subtitle_line1, font=subtitle_font)
    sub1_width = sub1_bbox[2] - sub1_bbox[0]
    draw_text_with_shadow(
        draw, subtitle_line1, 
        ((width - sub1_width) // 2, 500),
        subtitle_font, 
        (255, 255, 100), 
        (0, 0, 0)
    )
    
    # 第二行副标题
    sub2_bbox = draw.textbbox((0, 0), subtitle_line2, font=subtitle_font)
    sub2_width = sub2_bbox[2] - sub2_bbox[0]
    draw_text_with_shadow(
        draw, subtitle_line2, 
        ((width - sub2_width) // 2, 560),
        subtitle_font, 
        (255, 255, 100), 
        (0, 0, 0)
    )
    
    # 引人注目的标签
    tagline = "好莱坞巨星亲述"
    tagline_bbox = draw.textbbox((0, 0), tagline, font=accent_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    draw_text_with_shadow(
        draw, tagline, 
        ((width - tagline_width) // 2, 650),
        accent_font, 
        (200, 200, 200), 
        (0, 0, 0)
    )
    
    # 添加装饰性元素 - 金色边框
    border_width = 8
    # 上边框
    draw.rectangle([30, 30, width-30, 30+border_width], fill=(255, 215, 0))
    # 下边框  
    draw.rectangle([30, height-30-border_width, width-30, height-30], fill=(255, 215, 0))
    # 左边框
    draw.rectangle([30, 30, 30+border_width, height-30], fill=(255, 215, 0))
    # 右边框
    draw.rectangle([width-30-border_width, 30, width-30, height-30], fill=(255, 215, 0))
    
    # 添加关键词标签 - 竖向排列
    keywords = ["真实故事", "独家爆料", "必看内容"]
    keyword_start_y = 800
    
    for i, keyword in enumerate(keywords):
        # 绘制标签背景
        kw_bbox = draw.textbbox((0, 0), keyword, font=accent_font)
        kw_width = kw_bbox[2] - kw_bbox[0]
        kw_height = kw_bbox[3] - kw_bbox[1]
        
        # 背景圆角矩形
        tag_y = keyword_start_y + i * 80
        tag_x = (width - kw_width) // 2
        draw.rectangle([tag_x - 15, tag_y - 10, tag_x + kw_width + 15, tag_y + kw_height + 10], 
                      fill=(255, 0, 0), outline=(255, 255, 255), width=2)
        
        # 标签文字
        draw.text((tag_x, tag_y), keyword, font=accent_font, fill=(255, 255, 255))
    
    # 添加大的emoji装饰
    big_emoji = "💰"
    emoji_bbox = draw.textbbox((0, 0), big_emoji, font=title_font)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    draw.text(
        ((width - emoji_width) // 2, 200),
        big_emoji, 
        font=title_font, 
        fill=(255, 255, 255)
    )
    
    # 底部装饰emoji
    bottom_emojis = "🔥💎✨"
    bottom_bbox = draw.textbbox((0, 0), bottom_emojis, font=subtitle_font)
    bottom_width = bottom_bbox[2] - bottom_bbox[0]
    draw.text(
        ((width - bottom_width) // 2, 1100),
        bottom_emojis, 
        font=subtitle_font, 
        fill=(255, 255, 255)
    )
    
    # 添加水印
    watermark = "@董卓主演脱口秀"
    watermark_bbox = draw.textbbox((0, 0), watermark, font=watermark_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    draw_text_with_shadow(
        draw, watermark, 
        ((width - watermark_width) // 2, height - 80),
        watermark_font, 
        (255, 255, 255), 
        (0, 0, 0)
    )
    
    return img

def main():
    """主函数"""
    print("开始制作TikTok竖屏封面...")
    
    # 创建封面
    thumbnail = create_tiktok_thumbnail()
    
    # 确保输出目录存在
    os.makedirs('output', exist_ok=True)
    
    # 保存封面
    thumbnail_path = 'output/tiktok_thumbnail.jpg'
    thumbnail.save(thumbnail_path, 'JPEG', quality=95)
    
    print(f"TikTok封面已保存到: {thumbnail_path}")
    
    # 也创建一个PNG版本
    png_path = 'output/tiktok_thumbnail.png'
    thumbnail.save(png_path, 'PNG')
    print(f"PNG版本已保存到: {png_path}")
    
    # 显示封面信息
    print(f"封面尺寸: {thumbnail.size}")
    print("TikTok竖屏封面制作完成！")

if __name__ == "__main__":
    main() 