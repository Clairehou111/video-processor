#!/usr/bin/env python3
"""
高级翻译演示 - 集成多种AI翻译服务
使用OpenAI GPT、DeepL、Google Translate等API改善翻译质量
"""

import os
import sys
import time
from video_processor import VideoProcessor
from typing import Dict, List, Optional

class AdvancedTranslator:
    """集成多种翻译服务的高级翻译器"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.deepl_api_key = os.getenv('DEEPL_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
        
    def translate_with_openai(self, text: str, target_lang: str = "Chinese") -> str:
        """使用OpenAI GPT进行翻译 - 质量最高但有成本"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following English text to {target_lang}. Provide only the translation, no explanations."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI 翻译失败: {e}")
            return None
    
    def translate_with_deepl(self, text: str, target_lang: str = "ZH") -> str:
        """使用DeepL API翻译 - 质量很高，专业翻译"""
        try:
            import requests
            
            url = "https://api-free.deepl.com/v2/translate"
            headers = {
                "Authorization": f"DeepL-Auth-Key {self.deepl_api_key}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "text": text,
                "target_lang": target_lang,
                "source_lang": "EN"
            }
            
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                result = response.json()
                return result["translations"][0]["text"]
            return None
        except Exception as e:
            print(f"DeepL 翻译失败: {e}")
            return None
    
    def translate_with_google(self, text: str, target_lang: str = "zh") -> str:
        """使用Google Translate API翻译 - 免费额度，质量良好"""
        try:
            from googletrans import Translator
            
            translator = Translator()
            result = translator.translate(text, src='en', dest=target_lang)
            return result.text
        except Exception as e:
            print(f"Google 翻译失败: {e}")
            return None
    
    def translate_with_local_model(self, text: str) -> str:
        """使用本地模型翻译 - 免费但需要下载模型"""
        try:
            from transformers import pipeline
            
            # 使用Helsinki-NLP的翻译模型
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-zh")
            result = translator(text, max_length=512)
            return result[0]['translation_text']
        except Exception as e:
            print(f"本地模型翻译失败: {e}")
            return None
    
    def translate_best_available(self, text: str) -> tuple[str, str]:
        """尝试多种翻译方法，返回最佳结果"""
        methods = [
            ("OpenAI GPT", self.translate_with_openai),
            ("DeepL", self.translate_with_deepl),
            ("Google Translate", self.translate_with_google),
            ("Local Model", self.translate_with_local_model)
        ]
        
        for method_name, method_func in methods:
            try:
                if method_name == "OpenAI GPT" and not self.openai_api_key:
                    continue
                if method_name == "DeepL" and not self.deepl_api_key:
                    continue
                    
                result = method_func(text)
                if result and result.strip():
                    print(f"✅ 使用 {method_name} 翻译成功")
                    return result.strip(), method_name
            except Exception as e:
                print(f"❌ {method_name} 翻译失败: {e}")
                continue
        
        # 如果所有方法都失败，返回原文标记
        return f"[翻译失败] {text}", "Fallback"

class EnhancedVideoProcessor(VideoProcessor):
    """增强版视频处理器，集成高级翻译功能"""
    
    def __init__(self):
        super().__init__()
        self.advanced_translator = AdvancedTranslator()
    
    def translate_to_chinese_advanced(self, text):
        """使用高级翻译器进行翻译"""
        result, method = self.advanced_translator.translate_best_available(text)
        print(f"📝 翻译: '{text[:50]}...' -> '{result[:50]}...' (使用: {method})")
        return result

def setup_translation_apis():
    """设置翻译API密钥的指南"""
    print("🔧 翻译API设置指南:")
    print("\n1. OpenAI GPT (推荐 - 质量最高):")
    print("   - 访问: https://platform.openai.com/api-keys")
    print("   - 创建API密钥")
    print(f"   - 设置环境变量: export OPENAI_API_KEY='your-key'")
    
    print("\n2. DeepL API (专业翻译):")
    print("   - 访问: https://www.deepl.com/pro-api")
    print("   - 免费版每月50万字符")
    print(f"   - 设置环境变量: export DEEPL_API_KEY='your-key'")
    
    print("\n3. Google Translate (免费但有限制):")
    print("   - 使用googletrans库 (pip install googletrans==3.1.0a0)")
    print("   - 或申请Google Cloud Translation API")
    
    print("\n4. 本地模型 (完全免费):")
    print("   - 使用Transformers库下载Helsinki-NLP模型")
    print("   - 需要较大存储空间但无API费用")
    
    print("\n💡 推荐策略:")
    print("   - 开发测试: 使用本地模型或Google Translate")
    print("   - 生产环境: OpenAI GPT或DeepL (质量更高)")
    print("   - 大批量: 考虑Azure AI Translator或AWS Translate")

def check_api_status():
    """检查各种翻译API的可用状态"""
    print("\n🔍 检查翻译API状态:")
    
    translator = AdvancedTranslator()
    test_text = "Hello, this is a test."
    
    # 测试OpenAI
    if translator.openai_api_key:
        print("✅ OpenAI API Key 已配置")
        try:
            result = translator.translate_with_openai(test_text)
            if result:
                print(f"   测试翻译: '{test_text}' -> '{result}'")
            else:
                print("   ❌ 翻译测试失败")
        except Exception as e:
            print(f"   ❌ OpenAI API 错误: {e}")
    else:
        print("⚠️  OpenAI API Key 未配置")
    
    # 测试DeepL
    if translator.deepl_api_key:
        print("✅ DeepL API Key 已配置")
    else:
        print("⚠️  DeepL API Key 未配置")
    
    # 测试Google Translate
    try:
        result = translator.translate_with_google(test_text)
        if result:
            print(f"✅ Google Translate 可用: '{test_text}' -> '{result}'")
        else:
            print("❌ Google Translate 不可用")
    except Exception as e:
        print(f"❌ Google Translate 错误: {e}")
    
    # 测试本地模型
    try:
        print("📥 正在测试本地翻译模型...")
        result = translator.translate_with_local_model(test_text)
        if result:
            print(f"✅ 本地模型可用: '{test_text}' -> '{result}'")
        else:
            print("❌ 本地模型不可用")
    except Exception as e:
        print(f"❌ 本地模型错误: {e}")

def main():
    """主函数演示高级翻译功能"""
    print("🚀 高级翻译视频处理器演示")
    print("=" * 50)
    
    # 检查API状态
    check_api_status()
    
    print("\n" + "=" * 50)
    
    # 显示设置指南
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_translation_apis()
        return
    
    # 处理视频
    youtube_url = "https://www.youtube.com/watch?v=dp6BIDCZRic"
    watermark_text = "高级翻译版"
    quality = "720p"
    embed_subtitles = True
    
    print(f"\n🎬 开始处理视频:")
    print(f"   URL: {youtube_url}")
    print(f"   水印: {watermark_text}")
    print(f"   质量: {quality}")
    print(f"   嵌入字幕: {embed_subtitles}")
    
    try:
        # 创建增强版处理器
        processor = EnhancedVideoProcessor()
        
        # 替换翻译方法
        processor.translate_to_chinese_simple = processor.translate_to_chinese_advanced
        
        print("\n🔄 开始视频处理...")
        start_time = time.time()
        
        result = processor.process_video(
            url=youtube_url,
            watermark_text=watermark_text,
            quality=quality,
            embed_subtitles=embed_subtitles
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if result:
            print(f"\n✅ 处理完成!")
            print(f"   耗时: {processing_time:.1f} 秒")
            print(f"   输出文件: {result}")
            print(f"\n💡 翻译质量显著提升! 使用了AI驱动的翻译服务。")
        else:
            print(f"\n❌ 处理失败")
            
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断处理")
    except Exception as e:
        print(f"\n❌ 处理出错: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("用法:")
        print("  python advanced_translation_demo.py           # 运行演示")
        print("  python advanced_translation_demo.py --setup   # 显示API设置指南")
        print("  python advanced_translation_demo.py --help    # 显示帮助")
    else:
        main() 