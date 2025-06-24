#!/usr/bin/env python3
"""
高级剪映弹幕生成器
为政治喜剧视频定制的弹幕生成工具
"""

import json
import random
import os
import re
from typing import List, Dict, Tuple, Optional
from datetime import timedelta
import argparse

class AdvancedJianyingDanmakuGenerator:
    def __init__(self):
        # 针对政治喜剧视频的弹幕模板
        self.danmaku_templates = {
            "trump_specific": [
                "川普：我不是，我没有，别瞎说",
                "经典川普式发言",
                "川普表情包预定",
                "懂王又开始了",
                "这演技也就骗骗美国人",
                "川普：fake news！",
                "建议川普去说相声",
                "川普的商业头脑",
                "这就是川普style"
            ],
            "daily_show_praise": [
                "Daily Show永远的神",
                "Trevor Noah笑死人",
                "美式政治讽刺天花板",
                "这节目太敢说了",
                "老美的春晚",
                "比SNL还要精彩",
                "政治段子手",
                "美国版今日说法",
                "这节目在国内播不了"
            ],
            "translation_praise": [
                "这翻译太神了",
                "翻译小哥功力深厚",
                "本土化翻译满分",
                "翻译比原版还好笑",
                "这梗翻译绝了",
                "up主翻译水平可以",
                "字幕组辛苦了",
                "翻译很有文化",
                "这翻译有内味了"
            ],
            "political_reactions": [
                "政治就是这么魔幻",
                "现实比小说还离谱",
                "政客都是演员",
                "政治娱乐化的典型",
                "这比电视剧还精彩",
                "政治圈真是大型连续剧",
                "权力的游戏现实版",
                "政客的演技都不错",
                "政治真的很有意思"
            ],
            "viewer_engagement": [
                "求更新这类视频",
                "三连支持up主",
                "已投币收藏",
                "转发给朋友看",
                "求完整版资源",
                "哪里能看原版？",
                "up主品味真不错",
                "期待下期更新",
                "这up主有点东西",
                "关注了，继续更新",
                "求做成合集",
                "建议做个系列"
            ],
            "general_reactions": [
                "笑死我了哈哈哈",
                "绷不住了",
                "真实到离谱",
                "节目效果拉满",
                "这也太搞笑了",
                "我的天哪",
                "无语了",
                "太真实了",
                "笑到肚子疼",
                "神了神了",
                "这什么情况",
                "离大谱了"
            ],
            "emoji_reactions": [
                "😂😂😂😂",
                "🤣🤣🤣",
                "😆😆😆",
                "👏👏👏",
                "🔥🔥🔥",
                "💯💯💯",
                "👍👍👍",
                "😱😱😱",
                "🤔🤔🤔",
                "😏😏😏"
            ]
        }
        
        # 弹幕样式配置
        self.danmaku_styles = {
            "scroll": {"type": 1, "color": "16777215", "size": 25},      # 白色滚动
            "top": {"type": 5, "color": "16777215", "size": 24},         # 白色顶部
            "bottom": {"type": 4, "color": "16777215", "size": 24},      # 白色底部
            "red_scroll": {"type": 1, "color": "16711680", "size": 26},  # 红色滚动
            "yellow": {"type": 1, "color": "16776960", "size": 25},      # 黄色
            "green": {"type": 1, "color": "65280", "size": 25},          # 绿色
            "blue": {"type": 1, "color": "255", "size": 25},             # 蓝色
            "big_red": {"type": 1, "color": "16711680", "size": 30},     # 大红字
            "small_white": {"type": 1, "color": "16777215", "size": 20}  # 小白字
        }

    def create_smart_political_danmaku(self, video_duration: int,
                                     density: str = "medium",
                                     trump_focus: bool = True,
                                     include_emoji: bool = True) -> List[Dict]:
        """
        为政治喜剧视频创建智能弹幕
        
        Args:
            video_duration: 视频时长（秒）
            density: 弹幕密度
            trump_focus: 是否专注川普相关内容
            include_emoji: 是否包含表情符号
        """
        
        # 根据是否专注川普调整分布
        if trump_focus:
            style_distribution = {
                "trump_specific": 0.25,
                "daily_show_praise": 0.20,
                "translation_praise": 0.15,
                "political_reactions": 0.15,
                "viewer_engagement": 0.10,
                "general_reactions": 0.10,
                "emoji_reactions": 0.05 if include_emoji else 0
            }
        else:
            style_distribution = {
                "trump_specific": 0.10,
                "daily_show_praise": 0.25,
                "translation_praise": 0.20,
                "political_reactions": 0.15,
                "viewer_engagement": 0.15,
                "general_reactions": 0.10,
                "emoji_reactions": 0.05 if include_emoji else 0
            }
        
        # 计算弹幕数量
        density_multiplier = {"low": 0.3, "medium": 0.6, "high": 1.0}
        base_count = max(8, int(video_duration / 15))  # 每15秒基础弹幕数
        total_danmaku = int(base_count * density_multiplier.get(density, 0.6))
        
        danmaku_list = []
        
        # 确保开头有欢迎弹幕
        opening_danmaku = {
            "time": random.uniform(3, 8),
            "text": random.choice(["来了来了", "又更新了", "坐等开始", "搬好小板凳"]),
            "style": "scroll",
            "category": "opening"
        }
        danmaku_list.append(opening_danmaku)
        
        # 生成主要弹幕
        for i in range(total_danmaku - 2):  # 减去开头和结尾
            # 选择弹幕类型
            rand = random.random()
            cumulative = 0
            selected_type = "general_reactions"
            
            for danmaku_type, probability in style_distribution.items():
                cumulative += probability
                if rand <= cumulative:
                    selected_type = danmaku_type
                    break
            
            # 如果没有包含emoji，跳过emoji类型
            if not include_emoji and selected_type == "emoji_reactions":
                selected_type = "general_reactions"
            
            # 选择弹幕内容
            content = random.choice(self.danmaku_templates[selected_type])
            
            # 生成时间点（避免太密集）
            time_offset = random.uniform(10, video_duration - 10)
            
            # 选择样式
            style_name = self._choose_style_for_content(selected_type, content)
            
            danmaku_item = {
                "time": time_offset,
                "text": content,
                "style": style_name,
                "category": selected_type
            }
            
            danmaku_list.append(danmaku_item)
        
        # 确保结尾有感谢弹幕
        ending_danmaku = {
            "time": random.uniform(video_duration - 15, video_duration - 5),
            "text": random.choice(["up主辛苦了", "期待下期", "三连走起", "已关注"]),
            "style": "bottom",
            "category": "ending"
        }
        danmaku_list.append(ending_danmaku)
        
        # 按时间排序
        danmaku_list.sort(key=lambda x: x["time"])
        
        # 避免弹幕过于密集
        danmaku_list = self._adjust_timing_to_avoid_overlap(danmaku_list)
        
        return danmaku_list

    def _choose_style_for_content(self, category: str, content: str) -> str:
        """根据内容类型选择合适的样式"""
        
        if category == "trump_specific":
            return random.choice(["red_scroll", "big_red"])
        elif category == "daily_show_praise":
            return random.choice(["yellow", "top"])
        elif category == "translation_praise":
            return random.choice(["green", "scroll"])
        elif category == "political_reactions":
            return random.choice(["blue", "scroll"])
        elif category == "viewer_engagement":
            return "bottom"
        elif category == "emoji_reactions":
            return random.choice(["scroll", "top"])
        else:
            return "scroll"

    def _adjust_timing_to_avoid_overlap(self, danmaku_list: List[Dict], 
                                      min_gap: float = 2.0) -> List[Dict]:
        """调整弹幕时间避免过于密集"""
        
        if len(danmaku_list) <= 1:
            return danmaku_list
        
        adjusted_list = [danmaku_list[0]]
        
        for i in range(1, len(danmaku_list)):
            current_time = danmaku_list[i]["time"]
            last_time = adjusted_list[-1]["time"]
            
            if current_time - last_time < min_gap:
                # 调整时间
                new_time = last_time + min_gap + random.uniform(0, 1)
                danmaku_list[i]["time"] = new_time
            
            adjusted_list.append(danmaku_list[i])
        
        return adjusted_list

    def create_jianying_json(self, danmaku_data: List[Dict], output_path: str) -> str:
        """创建剪映格式的JSON文件"""
        
        jianying_danmaku = {"danmaku_list": []}
        
        for item in danmaku_data:
            style = self.danmaku_styles[item["style"]]
            
            jianying_item = {
                "time": int(item["time"] * 1000),  # 转为毫秒
                "text": item["text"],
                "mode": style["type"],
                "color": str(style["color"]),
                "fontsize": style["size"],
                "border": 1,
                "opacity": 1.0
            }
            jianying_danmaku["danmaku_list"].append(jianying_item)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(jianying_danmaku, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 剪映弹幕文件已生成: {output_path}")
        return output_path

    def create_analysis_report(self, danmaku_data: List[Dict], output_path: str):
        """创建弹幕分析报告"""
        
        # 统计各类弹幕数量
        category_stats = {}
        style_stats = {}
        
        for item in danmaku_data:
            category = item.get("category", "unknown")
            style = item.get("style", "unknown")
            
            category_stats[category] = category_stats.get(category, 0) + 1
            style_stats[style] = style_stats.get(style, 0) + 1
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("🎬 弹幕生成分析报告\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"📊 弹幕总数: {len(danmaku_data)}\n\n")
            
            f.write("📝 内容类型分布:\n")
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(danmaku_data)) * 100
                f.write(f"  {category}: {count} 条 ({percentage:.1f}%)\n")
            
            f.write("\n🎨 样式分布:\n")
            for style, count in sorted(style_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(danmaku_data)) * 100
                f.write(f"  {style}: {count} 条 ({percentage:.1f}%)\n")
            
            f.write("\n⏰ 时间分布:\n")
            time_points = [item["time"] for item in danmaku_data]
            f.write(f"  最早弹幕: {min(time_points):.1f}秒\n")
            f.write(f"  最晚弹幕: {max(time_points):.1f}秒\n")
            f.write(f"  平均间隔: {(max(time_points) - min(time_points)) / len(time_points):.1f}秒\n")
            
            f.write("\n📋 完整弹幕列表:\n")
            f.write("-" * 50 + "\n")
            for item in danmaku_data:
                time_str = f"{int(item['time']//60):02d}:{int(item['time']%60):02d}"
                f.write(f"[{time_str}] {item['text']} ({item['category']}, {item['style']})\n")

    def process_video_with_smart_danmaku(self, video_path: str, 
                                       output_dir: str = "output",
                                       **kwargs) -> Tuple[str, str]:
        """为视频智能生成弹幕"""
        
        # 获取视频信息
        import cv2
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 180
        cap.release()
        
        print(f"🎬 视频时长: {duration:.1f}秒")
        
        # 生成弹幕
        danmaku_data = self.create_smart_political_danmaku(
            int(duration),
            density=kwargs.get("density", "medium"),
            trump_focus=kwargs.get("trump_focus", True),
            include_emoji=kwargs.get("include_emoji", True)
        )
        
        # 创建输出文件名
        os.makedirs(output_dir, exist_ok=True)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # 生成各种格式文件
        jianying_file = os.path.join(output_dir, f"{video_name}_advanced_danmaku.json")
        report_file = os.path.join(output_dir, f"{video_name}_danmaku_report.txt")
        
        # 创建文件
        self.create_jianying_json(danmaku_data, jianying_file)
        self.create_analysis_report(danmaku_data, report_file)
        
        print(f"📊 分析报告: {report_file}")
        print(f"📱 使用方法: 在剪映中导入 {os.path.basename(jianying_file)}")
        
        return jianying_file, report_file


def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(description="高级剪映弹幕生成器")
    parser.add_argument("--video", help="视频文件路径")
    parser.add_argument("--density", choices=["low", "medium", "high"], 
                       default="medium", help="弹幕密度")
    parser.add_argument("--no-trump", action="store_true", 
                       help="减少川普相关弹幕")
    parser.add_argument("--no-emoji", action="store_true", 
                       help="不包含表情符号")
    parser.add_argument("--output", default="output", help="输出目录")
    
    args = parser.parse_args()
    
    generator = AdvancedJianyingDanmakuGenerator()
    
    # 查找视频文件
    video_files = []
    if args.video and os.path.exists(args.video):
        video_files = [args.video]
    else:
        # 在output目录查找
        output_dir = args.output
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    video_files.append(os.path.join(output_dir, file))
    
    if not video_files:
        print("❌ 未找到视频文件，生成示例弹幕")
        # 生成示例
        sample_danmaku = generator.create_smart_political_danmaku(
            180,  # 3分钟
            density=args.density,
            trump_focus=not args.no_trump,
            include_emoji=not args.no_emoji
        )
        
        os.makedirs(args.output, exist_ok=True)
        sample_file = os.path.join(args.output, "sample_advanced_danmaku.json")
        report_file = os.path.join(args.output, "sample_danmaku_report.txt")
        
        generator.create_jianying_json(sample_danmaku, sample_file)
        generator.create_analysis_report(sample_danmaku, report_file)
        
        print(f"✅ 示例文件已生成: {sample_file}")
        return
    
    # 处理找到的第一个视频
    video_path = video_files[0]
    print(f"🎬 处理视频: {os.path.basename(video_path)}")
    
    jianying_file, report_file = generator.process_video_with_smart_danmaku(
        video_path,
        output_dir=args.output,
        density=args.density,
        trump_focus=not args.no_trump,
        include_emoji=not args.no_emoji
    )
    
    print("\n🎉 完成！现在你可以:")
    print("1. 在剪映中导入视频")
    print("2. 添加弹幕效果")
    print("3. 导入生成的JSON文件")
    print("4. 调整弹幕效果并导出视频")


if __name__ == "__main__":
    main() 