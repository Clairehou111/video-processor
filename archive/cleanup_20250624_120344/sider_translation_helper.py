#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sider翻译助手
用于测试和调用Sider翻译功能
"""

import time
import re

class SiderTranslationHelper:
    def __init__(self):
        self.translation_cache = {}
        
    def clean_text(self, text):
        """清理文本，移除多余的空格和格式"""
        if not text:
            return ""
        # 移除多余的空格
        clean_text = re.sub(r'\s+', ' ', text.strip())
        # 移除一些常见的噪音字符
        clean_text = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', '', clean_text)
        return clean_text
    
    def translate_single_text(self, text, from_lang="英文", to_lang="中文"):
        """翻译单个文本片段"""
        clean_text = self.clean_text(text)
        
        if not clean_text:
            return ""
        
        # 检查缓存
        cache_key = f"{from_lang}:{to_lang}:{clean_text}"
        if cache_key in self.translation_cache:
            print(f"📖 使用缓存翻译: {clean_text}")
            return self.translation_cache[cache_key]
        
        try:
            print(f"🔄 Sider翻译: {clean_text}")
            
            # 这里会被实际的Sider翻译调用替换
            # 现在返回一个标识
            result = f"[Sider翻译待处理] {clean_text}"
            
            # 缓存结果
            self.translation_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            print(f"❌ Sider翻译失败: {e}")
            return f"[翻译失败] {clean_text}"
    
    def translate_subtitle_batch(self, subtitle_segments):
        """批量翻译字幕段落"""
        print("🌟 开始Sider批量翻译...")
        translated_segments = []
        
        for i, segment in enumerate(subtitle_segments):
            english_text = segment.get("text", "")
            
            if not english_text.strip():
                chinese_text = ""
            else:
                chinese_text = self.translate_single_text(english_text)
            
            translated_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "english": english_text,
                "chinese": chinese_text
            })
            
            if (i + 1) % 5 == 0:
                print(f"   已处理 {i + 1}/{len(subtitle_segments)} 个片段")
                print(f"   最新示例: '{english_text}' -> '{chinese_text}'")
        
        print(f"✅ Sider批量翻译完成，共处理 {len(translated_segments)} 个片段")
        return translated_segments
    
    def test_sider_translation(self):
        """测试Sider翻译功能"""
        print("🧪 Sider翻译功能测试")
        print("=" * 30)
        
        test_texts = [
            "Hello, how are you?",
            "This is a beautiful day.",
            "I love watching movies.",
            "Technology is changing our world.",
            "Thank you for your help."
        ]
        
        for text in test_texts:
            result = self.translate_single_text(text)
            print(f"原文: {text}")
            print(f"译文: {result}")
            print("-" * 20)
    
    def show_translation_stats(self):
        """显示翻译统计"""
        print(f"📊 翻译缓存统计: {len(self.translation_cache)} 条记录")
        if self.translation_cache:
            print("最近翻译:")
            for i, (key, value) in enumerate(list(self.translation_cache.items())[-3:]):
                parts = key.split(":", 2)
                if len(parts) == 3:
                    original = parts[2]
                    print(f"  {i+1}. {original} -> {value}")

def main():
    """主函数"""
    print("🌟 Sider翻译助手")
    print("=" * 30)
    
    helper = SiderTranslationHelper()
    
    while True:
        print("\n选择功能:")
        print("1. 🧪 测试Sider翻译")
        print("2. 📝 单句翻译")
        print("3. 📊 翻译统计")
        print("4. ❌ 退出")
        
        choice = input("请选择 (1-4): ").strip()
        
        if choice == "1":
            helper.test_sider_translation()
        elif choice == "2":
            text = input("请输入要翻译的英文: ").strip()
            if text:
                result = helper.translate_single_text(text)
                print(f"翻译结果: {result}")
        elif choice == "3":
            helper.show_translation_stats()
        elif choice == "4":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main() 