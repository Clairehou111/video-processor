#!/usr/bin/env python3
"""
弹幕坐标系统演示工具
详细解释ASS字幕格式中的坐标参数
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_coordinate_visualization():
    """创建弹幕坐标系统可视化图"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # 设置视频屏幕区域 (假设1920x1080分辨率)
    screen_width = 1920
    screen_height = 1080
    
    # 绘制屏幕边框
    screen_rect = patches.Rectangle((0, 0), screen_width, screen_height, 
                                  linewidth=3, edgecolor='black', 
                                  facecolor='lightgray', alpha=0.3)
    ax.add_patch(screen_rect)
    
    # 标注屏幕尺寸
    ax.text(screen_width/2, -50, f'屏幕尺寸: {screen_width}x{screen_height}', 
            ha='center', va='top', fontsize=12, weight='bold')
    
    # 绘制坐标轴
    ax.plot([0, screen_width], [screen_height/2, screen_height/2], 
            'b--', alpha=0.5, label='水平中线 (Y=540)')
    ax.plot([screen_width/2, screen_width/2], [0, screen_height], 
            'g--', alpha=0.5, label='垂直中线 (X=960)')
    
    # 标注关键坐标点
    key_points = [
        (0, 0, '(0,0)\n左上角'),
        (screen_width, 0, f'({screen_width},0)\n右上角'),
        (0, screen_height, f'(0,{screen_height})\n左下角'),
        (screen_width, screen_height, f'({screen_width},{screen_height})\n右下角'),
        (screen_width/2, screen_height/2, f'({int(screen_width/2)},{int(screen_height/2)})\n屏幕中心')
    ]
    
    for x, y, label in key_points:
        ax.plot(x, y, 'ro', markersize=8)
        ax.annotate(label, (x, y), xytext=(10, 10), 
                   textcoords='offset points', fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # 演示弹幕轨迹
    # 1. 滚动弹幕轨迹
    scroll_y = 540  # 中央位置
    ax.arrow(screen_width, scroll_y, -screen_width + 100, 0, 
             head_width=30, head_length=50, fc='red', ec='red', linewidth=3)
    ax.text(screen_width/2, scroll_y + 50, 
            '滚动弹幕轨迹\n{\\move(1920,540,0,540)}', 
            ha='center', va='bottom', fontsize=11, color='red', weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # 2. 顶部弹幕位置
    top_y = 100
    ax.plot(screen_width/2, top_y, 'bs', markersize=12)
    ax.text(screen_width/2, top_y + 50, 
            '顶部弹幕\n{\\pos(960,100)}', 
            ha='center', va='bottom', fontsize=11, color='blue', weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # 3. 底部弹幕位置
    bottom_y = 980
    ax.plot(screen_width/2, bottom_y, 'gs', markersize=12)
    ax.text(screen_width/2, bottom_y - 50, 
            '底部弹幕\n{\\pos(960,980)}', 
            ha='center', va='top', fontsize=11, color='green', weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # 设置图形属性
    ax.set_xlim(-100, screen_width + 100)
    ax.set_ylim(-100, screen_height + 100)
    ax.set_aspect('equal')
    ax.invert_yaxis()  # Y轴向下为正，符合屏幕坐标系
    ax.set_xlabel('X坐标 (像素)', fontsize=12)
    ax.set_ylabel('Y坐标 (像素)', fontsize=12)
    ax.set_title('弹幕坐标系统详解\nASS字幕格式中的 {\\move(x1,y1,x2,y2)} 参数说明', 
                fontsize=14, weight='bold', pad=20)
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('output/danmaku_coordinates_explanation.png', dpi=300, bbox_inches='tight')
    print("✅ 坐标系统图已保存: output/danmaku_coordinates_explanation.png")
    
    return fig

def explain_ass_parameters():
    """详细解释ASS参数"""
    
    explanation = """
🎯 弹幕坐标参数详解

1. 📐 坐标系统
   - 原点 (0,0) 在屏幕左上角
   - X轴：从左到右 (0 → 1920)
   - Y轴：从上到下 (0 → 1080)

2. 🎬 常见弹幕效果

   滚动弹幕: {\\move(1920,540,0,540)}
   ├── 1920,540 = 起始位置 (屏幕右侧中央)
   ├── 0,540 = 结束位置 (屏幕左侧中央)
   └── 效果：从右到左水平滚动

   顶部弹幕: {\\pos(960,100)}
   ├── 960 = 水平居中
   ├── 100 = 距离顶部100像素
   └── 效果：固定在屏幕上方

   底部弹幕: {\\pos(960,980)}
   ├── 960 = 水平居中
   ├── 980 = 距离顶部980像素
   └── 效果：固定在屏幕下方

3. 🎨 关键数值含义
   - 540 = 1080÷2，屏幕垂直中心线
   - 960 = 1920÷2，屏幕水平中心线
   - 100 = 顶部边距
   - 980 = 底部位置 (1080-100)

4. 📏 自定义位置示例
   - 左上角: {\\pos(100,100)}
   - 右上角: {\\pos(1820,100)}
   - 左下角: {\\pos(100,980)}
   - 右下角: {\\pos(1820,980)}
   - 随机滚动: {\\move(1920,300,0,300)}
"""
    
    return explanation

def create_parameter_comparison():
    """创建不同参数效果对比"""
    
    examples = {
        "滚动弹幕（标准）": "{\\move(1920,540,0,540)}",
        "滚动弹幕（上方）": "{\\move(1920,300,0,300)}",
        "滚动弹幕（下方）": "{\\move(1920,780,0,780)}",
        "顶部固定": "{\\pos(960,100)}",
        "底部固定": "{\\pos(960,980)}",
        "左侧固定": "{\\pos(200,540)}",
        "右侧固定": "{\\pos(1720,540)}",
        "对角移动": "{\\move(0,0,1920,1080)}",
        "反向滚动": "{\\move(0,540,1920,540)}",
        "垂直滚动": "{\\move(960,0,960,1080)}"
    }
    
    print("\n🎭 弹幕效果参数对比")
    print("=" * 50)
    
    for name, param in examples.items():
        print(f"{name:12} → {param}")
    
    return examples

def main():
    """主函数"""
    print("🎬 弹幕坐标系统详解")
    print("=" * 50)
    
    # 创建可视化图
    try:
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端
        fig = create_coordinate_visualization()
        print("📊 坐标系统可视化图已生成")
    except ImportError:
        print("⚠️ matplotlib未安装，跳过图形生成")
        print("安装方法: pip install matplotlib")
    
    # 输出详细说明
    explanation = explain_ass_parameters()
    print(explanation)
    
    # 参数对比
    examples = create_parameter_comparison()
    
    # 保存说明文档
    with open('output/danmaku_coordinates_guide.txt', 'w', encoding='utf-8') as f:
        f.write("弹幕坐标系统完整指南\n")
        f.write("=" * 50 + "\n\n")
        f.write(explanation)
        f.write("\n\n弹幕效果参数对比\n")
        f.write("-" * 30 + "\n")
        for name, param in examples.items():
            f.write(f"{name:15} → {param}\n")
    
    print(f"\n📋 完整指南已保存: output/danmaku_coordinates_guide.txt")
    
    print(f"\n🎯 总结:")
    print(f"- 你看到的 540,0,540 是弹幕从右到左滚动的坐标")
    print(f"- 540 是屏幕垂直中心线的Y坐标")
    print(f"- 1920,540 → 0,540 表示从右侧中央滚动到左侧中央")
    print(f"- 这些数字控制弹幕在屏幕上的位置和移动轨迹")

if __name__ == "__main__":
    main() 