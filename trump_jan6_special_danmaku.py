#!/usr/bin/env python3
"""
川普1月6日事件专用弹幕生成器
针对相关政治视频内容优化
"""

import json
import random
import os
import cv2
from typing import List, Dict

class TrumpJan6DanmakuGenerator:
    def __init__(self):
        # 专门针对川普1月6日事件的弹幕模板
        self.special_templates = {
            "jan6_specific": [
                "1月6日又来了",
                "国会山事件回顾",
                "历史性的一天",
                "democracy in action",
                "这就是美式民主？",
                "川普的最后疯狂",
                "国会暴乱现场",
                "美国政治的黑暗一天",
                "见证历史时刻"
            ],
            "trump_reactions": [
                "川普：我没煽动",
                "懂王又甩锅了",
                "classic Trump denial",
                "川普式解释来了",
                "这演技我服了",
                "川普：都是fake news",
                "推特治国的后果",
                "总统变网红的悲剧",
                "商人不适合从政"
            ],
            "committee_comments": [
                "委员会调查进行中",
                "证据确凿了这次",
                "听证会很精彩",
                "真相终于要出来了",
                "司法程序走起来",
                "法律面前人人平等",
                "美国司法制度test",
                "democracy正在自我修复",
                "制衡机制启动"
            ],
            "filmmaker_focus": [
                "纪录片拍摄者视角",
                "第一手资料珍贵",
                "behind the scenes",
                "导演勇气可嘉",
                "记录历史的重要性",
                "真实影像的力量",
                "documentary的价值",
                "历史不容篡改",
                "影像证据最有说服力"
            ],
            "political_commentary": [
                "美国政治太魔幻了",
                "比电视剧还精彩",
                "现实版纸牌屋",
                "权力的游戏美国版",
                "政治就是这么残酷",
                "民主制度的考验",
                "三权分立在工作",
                "美式政治斗争",
                "这就是politics"
            ],
            "viewer_reactions": [
                "瓜太大了吃不完",
                "历史课本要更新了",
                "见证了活历史",
                "比好莱坞大片刺激",
                "真实比虚构更离奇",
                "我们是历史的见证者",
                "后代会研究这段历史",
                "活在历史转折点",
                "太魔幻现实主义了"
            ]
        }
        
        # 弹幕样式 - 针对严肃政治内容调整
        self.styles = {
            "serious_white": {"type": 1, "color": "16777215", "size": 24},     # 白色标准
            "highlight_red": {"type": 1, "color": "16711680", "size": 26},     # 红色强调
            "comment_blue": {"type": 1, "color": "255", "size": 24},           # 蓝色评论
            "important_yellow": {"type": 1, "color": "16776960", "size": 25},  # 黄色重要
            "top_notice": {"type": 5, "color": "16777215", "size": 23},        # 顶部通知
            "bottom_summary": {"type": 4, "color": "16777215", "size": 23},    # 底部总结
            "big_moment": {"type": 1, "color": "16711680", "size": 28}         # 重大时刻
        }

    def create_jan6_themed_danmaku(self, video_duration: int, density: str = "high") -> List[Dict]:
        """创建1月6日主题弹幕"""
        
        # 内容分布 - 偏重严肃政治评论
        content_distribution = {
            "jan6_specific": 0.25,
            "trump_reactions": 0.25,
            "committee_comments": 0.15,
            "political_commentary": 0.15,
            "filmmaker_focus": 0.10,
            "viewer_reactions": 0.10
        }
        
        # 根据视频时长计算弹幕数量
        density_multiplier = {"low": 0.4, "medium": 0.7, "high": 1.0}
        base_count = max(6, int(video_duration / 12))  # 每12秒一条基础弹幕
        total_count = int(base_count * density_multiplier.get(density, 1.0))
        
        danmaku_list = []
        
        # 开场弹幕
        opening = {
            "time": random.uniform(2, 5),
            "text": random.choice(["历史时刻来了", "重要视频alert", "见证历史"]),
            "style": "top_notice",
            "category": "opening"
        }
        danmaku_list.append(opening)
        
        # 生成主要弹幕内容
        for i in range(total_count - 2):
            # 选择内容类型
            rand = random.random()
            cumulative = 0
            selected_type = "political_commentary"
            
            for content_type, probability in content_distribution.items():
                cumulative += probability
                if rand <= cumulative:
                    selected_type = content_type
                    break
            
            # 选择弹幕文本
            text = random.choice(self.special_templates[selected_type])
            
            # 生成时间点
            time_point = random.uniform(8, video_duration - 8)
            
            # 选择样式
            style = self._choose_style_for_jan6_content(selected_type)
            
            danmaku_item = {
                "time": time_point,
                "text": text,
                "style": style,
                "category": selected_type
            }
            danmaku_list.append(danmaku_item)
        
        # 结尾总结弹幕
        ending = {
            "time": random.uniform(video_duration - 8, video_duration - 3),
            "text": random.choice(["历史会记住这一切", "真相终将大白", "democracy will survive"]),
            "style": "bottom_summary",
            "category": "ending"
        }
        danmaku_list.append(ending)
        
        # 按时间排序并调整间隔
        danmaku_list.sort(key=lambda x: x["time"])
        danmaku_list = self._adjust_timing(danmaku_list)
        
        return danmaku_list

    def _choose_style_for_jan6_content(self, category: str) -> str:
        """为1月6日内容选择合适的样式"""
        
        style_mapping = {
            "jan6_specific": random.choice(["big_moment", "highlight_red"]),
            "trump_reactions": random.choice(["highlight_red", "serious_white"]),
            "committee_comments": "comment_blue",
            "political_commentary": "serious_white",
            "filmmaker_focus": "important_yellow",
            "viewer_reactions": random.choice(["serious_white", "comment_blue"])
        }
        
        return style_mapping.get(category, "serious_white")

    def _adjust_timing(self, danmaku_list: List[Dict], min_gap: float = 3.0) -> List[Dict]:
        """调整时间间隔，确保严肃内容有足够间隔"""
        
        if len(danmaku_list) <= 1:
            return danmaku_list
        
        adjusted = [danmaku_list[0]]
        
        for i in range(1, len(danmaku_list)):
            current_time = danmaku_list[i]["time"]
            last_time = adjusted[-1]["time"]
            
            if current_time - last_time < min_gap:
                new_time = last_time + min_gap + random.uniform(0.5, 1.5)
                danmaku_list[i]["time"] = new_time
            
            adjusted.append(danmaku_list[i])
        
        return adjusted

    def create_jianying_file(self, danmaku_data: List[Dict], output_path: str) -> str:
        """生成剪映格式文件"""
        
        jianying_data = {"danmaku_list": []}
        
        for item in danmaku_data:
            style_config = self.styles[item["style"]]
            
            jianying_item = {
                "time": int(item["time"] * 1000),
                "text": item["text"],
                "mode": style_config["type"],
                "color": str(style_config["color"]),
                "fontsize": style_config["size"],
                "border": 1,
                "opacity": 1.0
            }
            jianying_data["danmaku_list"].append(jianying_item)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(jianying_data, f, ensure_ascii=False, indent=2)
        
        return output_path

    def process_jan6_video(self, video_path: str, output_dir: str = "output") -> str:
        """处理1月6日相关视频"""
        
        # 获取视频时长
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 60
        cap.release()
        
        print(f"🎬 1月6日主题视频时长: {duration:.1f}秒")
        
        # 生成专题弹幕
        danmaku_data = self.create_jan6_themed_danmaku(int(duration), "high")
        
        # 创建输出文件
        os.makedirs(output_dir, exist_ok=True)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file = os.path.join(output_dir, f"{video_name}_jan6_special_danmaku.json")
        
        self.create_jianying_file(danmaku_data, output_file)
        
        # 创建预览
        preview_file = os.path.join(output_dir, f"{video_name}_jan6_preview.txt")
        self._create_preview(danmaku_data, preview_file)
        
        print(f"✅ 1月6日专题弹幕已生成: {output_file}")
        print(f"📋 预览文件: {preview_file}")
        
        return output_file

    def _create_preview(self, danmaku_data: List[Dict], output_path: str):
        """创建预览文件"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("🏛️ 川普1月6日事件专题弹幕预览\n")
            f.write("=" * 50 + "\n\n")
            
            # 统计信息
            category_stats = {}
            for item in danmaku_data:
                category = item.get("category", "unknown")
                category_stats[category] = category_stats.get(category, 0) + 1
            
            f.write("📊 内容分类统计:\n")
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {category}: {count} 条\n")
            
            f.write(f"\n📝 总计: {len(danmaku_data)} 条弹幕\n\n")
            f.write("⏰ 时间轴预览:\n")
            f.write("-" * 50 + "\n")
            
            for item in danmaku_data:
                time_str = f"{int(item['time']//60):02d}:{int(item['time']%60):02d}"
                f.write(f"[{time_str}] {item['text']} ({item['category']}, {item['style']})\n")


if __name__ == "__main__":
    generator = TrumpJan6DanmakuGenerator()
    
    # 处理指定的1月6日视频
    video_path = "/Users/admin/IdeaProjects/video-processor/output/_jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4"
    
    if os.path.exists(video_path):
        output_file = generator.process_jan6_video(video_path)
        print("\n🎯 专题弹幕特色:")
        print("- 针对1月6日事件优化的政治评论")
        print("- 更严肃的弹幕风格和间隔")
        print("- 强调历史意义和民主制度")
        print("- 适合政治分析类视频")
    else:
        print("❌ 视频文件不存在，请检查路径") 