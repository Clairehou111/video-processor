#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全自动化Sider.AI翻译器
使用Selenium实现真正的浏览器自动化
"""

import os
import time
import json
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class FullyAutomatedSiderTranslator:
    """完全自动化Sider.AI翻译器"""
    
    def __init__(self, output_dir="output", headless=False):
        self.output_dir = output_dir
        self.sider_url = "https://sider.ai/chat"
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        print("🔧 设置Chrome浏览器驱动...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # 添加其他有用的选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # 使用webdriver-manager自动管理ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            print("✅ Chrome浏览器驱动设置成功")
            return True
        except Exception as e:
            print(f"❌ Chrome浏览器驱动设置失败: {e}")
            print("💡 请确保已安装Chrome浏览器")
            return False
    
    def parse_english_srt(self, srt_file):
        """解析英文SRT字幕文件"""
        segments = []
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分割字幕块
        blocks = content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # 文本内容
                text = ' '.join(lines[2:])
                segments.append({'text': text})
        
        return segments
    
    def create_translation_prompt(self, segments):
        """创建翻译提示词"""
        prompt = """请将以下英文字幕翻译为中文，要求：
1. 保持原有的编号格式
2. 翻译要自然流畅，符合中文表达习惯
3. 保持政治脱口秀的幽默感和讽刺语调
4. 专有名词（人名、地名）保持英文或使用通用中文译名
5. 每行翻译后请换行

英文字幕内容：

"""
        
        for i, segment in enumerate(segments, 1):
            prompt += f"{i}. {segment['text']}\n"
        
        return prompt
    
    def navigate_to_sider(self):
        """导航到Sider.AI网站"""
        print("🌐 导航到Sider.AI网站...")
        
        try:
            self.driver.get(self.sider_url)
            print("✅ 成功打开Sider.AI")
            
            # 等待页面加载
            time.sleep(3)
            
            # 检查是否需要登录
            if self.check_login_required():
                print("🔑 检测到需要登录")
                return self.handle_login()
            else:
                print("✅ 无需登录，直接进入聊天界面")
                return True
                
        except Exception as e:
            print(f"❌ 导航到Sider.AI失败: {e}")
            return False
    
    def check_login_required(self):
        """检查是否需要登录"""
        try:
            # 查找登录相关元素
            login_elements = [
                "//button[contains(text(), 'Login')]",
                "//button[contains(text(), 'Sign in')]",
                "//a[contains(text(), 'Login')]",
                "//a[contains(text(), 'Sign in')]",
                "//input[@type='email']",
                "//input[@type='password']"
            ]
            
            for xpath in login_elements:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element.is_displayed():
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ 检查登录状态时出错: {e}")
            return False
    
    def handle_login(self):
        """处理登录流程"""
        print("🔑 处理登录流程...")
        
        # 这里需要用户提供登录信息
        print("⚠️ 检测到需要登录Sider.AI")
        print("💡 请在浏览器中手动登录，然后按回车继续...")
        
        # 等待用户手动登录
        input("按回车键继续...")
        
        # 检查是否登录成功
        time.sleep(2)
        if self.check_chat_interface():
            print("✅ 登录成功")
            return True
        else:
            print("❌ 登录失败或未完成")
            return False
    
    def check_chat_interface(self):
        """检查聊天界面是否可用"""
        try:
            # 查找聊天输入框
            chat_input_selectors = [
                "//textarea[contains(@placeholder, 'Message')]",
                "//textarea[contains(@placeholder, 'Type')]",
                "//input[contains(@placeholder, 'Message')]",
                "//input[contains(@placeholder, 'Type')]",
                "//div[contains(@contenteditable, 'true')]",
                "textarea",
                "input[type='text']"
            ]
            
            for selector in chat_input_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed() and element.is_enabled():
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ 检查聊天界面时出错: {e}")
            return False
    
    def find_chat_input(self):
        """找到聊天输入框"""
        print("🔍 寻找聊天输入框...")
        
        # 多种可能的选择器
        selectors = [
            "//textarea[contains(@placeholder, 'Message')]",
            "//textarea[contains(@placeholder, 'Type')]",
            "//textarea[contains(@placeholder, 'Ask')]",
            "//textarea[contains(@placeholder, 'Chat')]",
            "//div[contains(@contenteditable, 'true')]",
            "//input[contains(@placeholder, 'Message')]",
            "//input[contains(@placeholder, 'Type')]",
            "textarea",
            "input[type='text']",
            "[data-testid*='chat']",
            "[data-testid*='input']",
            "[data-testid*='message']"
        ]
        
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                elif selector.startswith("["):
                    element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                else:
                    element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                
                if element.is_displayed() and element.is_enabled():
                    print(f"✅ 找到聊天输入框: {selector}")
                    return element
                    
            except TimeoutException:
                continue
            except Exception as e:
                print(f"⚠️ 尝试选择器 {selector} 时出错: {e}")
                continue
        
        print("❌ 未找到聊天输入框")
        return None
    
    def send_translation_request(self, prompt_text):
        """发送翻译请求"""
        print("📝 发送翻译请求...")
        
        try:
            # 找到聊天输入框
            chat_input = self.find_chat_input()
            if not chat_input:
                return False
            
            # 清空输入框
            chat_input.clear()
            
            # 输入翻译提示词
            print("⌨️ 输入翻译提示词...")
            chat_input.send_keys(prompt_text)
            
            # 等待一下让文本完全输入
            time.sleep(2)
            
            # 发送消息（尝试多种方式）
            print("🚀 发送翻译请求...")
            
            # 方式1: 按回车键
            try:
                chat_input.send_keys(Keys.RETURN)
                time.sleep(1)
            except:
                pass
            
            # 方式2: 查找发送按钮
            send_button_selectors = [
                "//button[contains(@aria-label, 'Send')]",
                "//button[contains(text(), 'Send')]",
                "//button[contains(@title, 'Send')]",
                "//button[contains(@class, 'send')]",
                "[data-testid*='send']",
                "button[type='submit']"
            ]
            
            for selector in send_button_selectors:
                try:
                    if selector.startswith("//"):
                        send_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        send_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if send_button.is_displayed() and send_button.is_enabled():
                        send_button.click()
                        print("✅ 点击发送按钮成功")
                        break
                except:
                    continue
            
            print("✅ 翻译请求已发送")
            return True
            
        except Exception as e:
            print(f"❌ 发送翻译请求失败: {e}")
            return False
    
    def wait_for_response(self, timeout=120):
        """等待翻译响应"""
        print("⏳ 等待翻译响应...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # 查找响应内容
                response_selectors = [
                    "//div[contains(@class, 'message')]",
                    "//div[contains(@class, 'response')]",
                    "//div[contains(@class, 'assistant')]",
                    "//div[contains(@class, 'bot')]",
                    "//pre",
                    "//code",
                    "[data-testid*='message']",
                    "[data-testid*='response']"
                ]
                
                for selector in response_selectors:
                    try:
                        if selector.startswith("//"):
                            elements = self.driver.find_elements(By.XPATH, selector)
                        else:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if elements:
                            # 获取最后一个响应
                            last_response = elements[-1]
                            response_text = last_response.text.strip()
                            
                            # 检查响应是否包含翻译内容
                            if self.is_valid_translation(response_text):
                                print("✅ 检测到翻译响应")
                                return response_text
                                
                    except Exception as e:
                        continue
                
                # 等待一下再检查
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ 检查响应时出错: {e}")
                time.sleep(2)
        
        print("❌ 等待翻译响应超时")
        return None
    
    def is_valid_translation(self, text):
        """检查文本是否为有效的翻译结果"""
        if not text or len(text) < 50:
            return False
        
        # 检查是否包含中文字符
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        if chinese_chars < 10:
            return False
        
        # 检查是否包含编号格式
        if re.search(r'\d+\.', text):
            return True
        
        # 检查是否包含翻译相关的关键词
        translation_keywords = ['翻译', '中文', '1.', '2.', '3.']
        if any(keyword in text for keyword in translation_keywords):
            return True
        
        return False
    
    def save_translation_result(self, translation_text):
        """保存翻译结果"""
        output_file = os.path.join(self.output_dir, "chinese_translation.txt")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translation_text)
            print(f"✅ 翻译结果已保存到: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ 保存翻译结果失败: {e}")
            return None
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ 浏览器已关闭")
            except:
                pass
    
    async def process_translation(self, english_srt_file):
        """处理翻译的完整流程"""
        print("🎯 完全自动化Sider.AI翻译开始")
        print("="*50)
        
        try:
            # 1. 设置浏览器驱动
            print("🔧 步骤1: 设置浏览器驱动")
            if not self.setup_driver():
                return None
            
            # 2. 解析英文字幕
            print("\n📖 步骤2: 解析英文字幕")
            segments = self.parse_english_srt(english_srt_file)
            print(f"✅ 解析完成，共 {len(segments)} 个片段")
            
            # 3. 创建翻译提示词
            print("\n📝 步骤3: 创建翻译提示词")
            prompt_text = self.create_translation_prompt(segments)
            print("✅ 翻译提示词创建完成")
            
            # 4. 导航到Sider.AI
            print("\n🌐 步骤4: 导航到Sider.AI")
            if not self.navigate_to_sider():
                return None
            
            # 5. 发送翻译请求
            print("\n🚀 步骤5: 发送翻译请求")
            if not self.send_translation_request(prompt_text):
                return None
            
            # 6. 等待翻译响应
            print("\n⏳ 步骤6: 等待翻译响应")
            translation_result = self.wait_for_response()
            
            if not translation_result:
                print("❌ 未获得翻译响应")
                return None
            
            # 7. 保存翻译结果
            print("\n💾 步骤7: 保存翻译结果")
            result_file = self.save_translation_result(translation_result)
            
            if result_file:
                print(f"\n🎉 完全自动化翻译完成!")
                print(f"📁 翻译结果: {result_file}")
                print("\n🎬 下一步: 运行以下命令生成双语视频:")
                print("   python create_bilingual_video.py")
                return result_file
            else:
                return None
                
        except Exception as e:
            print(f"\n❌ 翻译过程中出现错误: {e}")
            return None
        finally:
            # 清理资源
            self.cleanup()

def install_selenium_if_needed():
    """安装Selenium如果需要"""
    try:
        import selenium
        print("✅ Selenium已安装")
        return True
    except ImportError:
        print("📦 安装Selenium...")
        try:
            import subprocess
            subprocess.check_call(["pip", "install", "selenium"])
            print("✅ Selenium安装成功")
            return True
        except Exception as e:
            print(f"❌ Selenium安装失败: {e}")
            return False

def main():
    """主函数"""
    import sys
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python fully_automated_sider_translator.py <英文字幕文件> [--headless]")
        print("示例: python fully_automated_sider_translator.py output/VP9_segment_2m36s-5m59s_english.srt")
        print("示例: python fully_automated_sider_translator.py output/VP9_segment_2m36s-5m59s_english.srt --headless")
        sys.exit(1)
    
    english_srt_file = sys.argv[1]
    headless = "--headless" in sys.argv
    
    # 检查文件是否存在
    if not os.path.exists(english_srt_file):
        print(f"❌ 文件不存在: {english_srt_file}")
        sys.exit(1)
    
    # 安装Selenium如果需要
    if not install_selenium_if_needed():
        sys.exit(1)
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建翻译器实例
    translator = FullyAutomatedSiderTranslator(output_dir, headless=headless)
    
    # 运行翻译流程
    try:
        import asyncio
        result = asyncio.run(translator.process_translation(english_srt_file))
        
        if result:
            print(f"\n✅ 完全自动化翻译流程完成: {result}")
        else:
            print("\n❌ 完全自动化翻译流程失败")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
        translator.cleanup()
    except Exception as e:
        print(f"\n❌ 翻译过程中出现错误: {e}")
        translator.cleanup()

if __name__ == "__main__":
    main() 