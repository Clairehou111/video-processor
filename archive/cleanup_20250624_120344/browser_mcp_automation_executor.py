#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser MCP自动化执行器
使用Browser MCP完成Sider.AI翻译的完整自动化
"""

import json
import subprocess
import time
import os

class BrowserMCPExecutor:
    """Browser MCP自动化执行器"""
    
    def __init__(self):
        self.sider_url = "https://sider.ai/chat"
        
    def read_translation_prompt(self):
        """读取翻译提示词"""
        try:
            with open("output/sider_translation_prompt.txt", 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"❌ 读取翻译提示词失败: {e}")
            return None
    
    def execute_browser_mcp_command(self, command):
        """执行Browser MCP命令"""
        try:
            # 使用Browser MCP执行命令
            result = subprocess.run(
                ["npx", "@browsermcp/mcp@latest", "--execute", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.returncode == 0 else None
        except Exception as e:
            print(f"❌ 执行Browser MCP命令失败: {e}")
            return None
    
    def navigate_to_sider(self):
        """导航到Sider.AI"""
        print("🌐 导航到Sider.AI...")
        
        # Browser MCP导航命令
        navigate_script = f"""
        // 导航到Sider.AI
        await page.goto('{self.sider_url}');
        await page.waitForLoadState('networkidle');
        console.log('✅ 已导航到Sider.AI');
        """
        
        return self.execute_browser_mcp_command(navigate_script)
    
    def wait_for_login(self):
        """等待用户登录"""
        print("🔑 等待登录...")
        
        # 检查登录状态的脚本
        check_login_script = """
        // 检查是否已登录
        const loginElements = await page.$$('button:has-text("Login"), button:has-text("Sign in"), a:has-text("Login"), a:has-text("Sign in")');
        
        if (loginElements.length > 0) {
            console.log('⚠️ 需要登录');
            return 'need_login';
        } else {
            console.log('✅ 已登录或无需登录');
            return 'logged_in';
        }
        """
        
        result = self.execute_browser_mcp_command(check_login_script)
        
        if result and 'need_login' in result:
            print("⚠️ 检测到需要登录，请在浏览器中完成登录...")
            input("登录完成后按回车继续...")
        
        return True
    
    def select_ai_model(self):
        """选择AI模型"""
        print("🤖 选择AI模型...")
        
        # 选择Claude模型的脚本
        select_model_script = """
        // 查找并选择Claude模型
        const modelSelectors = [
            'button:has-text("Claude")',
            'div:has-text("Claude")',
            'select option:has-text("Claude")',
            '[data-model*="claude"]',
            '.model-selector:has-text("Claude")'
        ];
        
        for (const selector of modelSelectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    await element.click();
                    console.log('✅ 已选择Claude模型');
                    return 'success';
                }
            } catch (e) {
                continue;
            }
        }
        
        console.log('⚠️ 未找到Claude模型选择器，使用默认模型');
        return 'default';
        """
        
        return self.execute_browser_mcp_command(select_model_script)
    
    def input_translation_prompt(self, prompt_text):
        """输入翻译提示词"""
        print("📝 输入翻译提示词...")
        
        # 转义特殊字符
        escaped_prompt = prompt_text.replace('`', '\\`').replace('${', '\\${')
        
        input_script = f"""
        // 查找聊天输入框
        const inputSelectors = [
            'textarea[placeholder*="Message"]',
            'textarea[placeholder*="Type"]',
            'textarea[placeholder*="Ask"]',
            'div[contenteditable="true"]',
            'textarea',
            'input[type="text"]'
        ];
        
        let chatInput = null;
        for (const selector of inputSelectors) {{
            try {{
                chatInput = await page.$(selector);
                if (chatInput && await chatInput.isVisible()) {{
                    console.log(`✅ 找到聊天输入框: ${{selector}}`);
                    break;
                }}
            }} catch (e) {{
                continue;
            }}
        }}
        
        if (!chatInput) {{
            throw new Error('❌ 未找到聊天输入框');
        }}
        
        // 清空并输入翻译提示词
        await chatInput.click();
        await chatInput.fill('');
        await chatInput.type(`{escaped_prompt}`);
        
        console.log('✅ 翻译提示词已输入');
        return 'success';
        """
        
        return self.execute_browser_mcp_command(input_script)
    
    def send_message(self):
        """发送消息"""
        print("🚀 发送翻译请求...")
        
        send_script = """
        // 发送消息
        try {
            // 方式1: 按回车键
            await page.keyboard.press('Enter');
            await page.waitForTimeout(1000);
        } catch (e) {
            // 方式2: 查找发送按钮
            const sendSelectors = [
                'button[aria-label*="Send"]',
                'button:has-text("Send")',
                'button[title*="Send"]',
                '[data-testid*="send"]',
                'button[type="submit"]'
            ];
            
            for (const selector of sendSelectors) {
                try {
                    const sendButton = await page.$(selector);
                    if (sendButton && await sendButton.isVisible()) {
                        await sendButton.click();
                        console.log('✅ 点击发送按钮成功');
                        break;
                    }
                } catch (e) {
                    continue;
                }
            }
        }
        
        console.log('✅ 翻译请求已发送');
        return 'success';
        """
        
        return self.execute_browser_mcp_command(send_script)
    
    def wait_for_translation(self):
        """等待翻译完成"""
        print("⏳ 等待翻译完成...")
        
        wait_script = """
        // 等待翻译响应
        let maxWaitTime = 60000; // 60秒
        let checkInterval = 2000; // 2秒检查一次
        let startTime = Date.now();
        
        while (Date.now() - startTime < maxWaitTime) {
            // 查找响应内容
            const responseSelectors = [
                '.message:last-child',
                '.response:last-child',
                '.assistant-message:last-child',
                '[data-testid*="message"]:last-child',
                'pre:last-child'
            ];
            
            for (const selector of responseSelectors) {
                try {
                    const element = await page.$(selector);
                    if (element) {
                        const text = await element.textContent();
                        if (text && text.length > 100 && text.includes('1.') && text.includes('2.')) {
                            console.log('✅ 检测到翻译响应');
                            return text;
                        }
                    }
                } catch (e) {
                    continue;
                }
            }
            
            await page.waitForTimeout(checkInterval);
        }
        
        throw new Error('❌ 等待翻译响应超时');
        """
        
        return self.execute_browser_mcp_command(wait_script)
    
    def extract_translation_result(self):
        """提取翻译结果"""
        print("📖 提取翻译结果...")
        
        extract_script = """
        // 提取最新的翻译结果
        const responseSelectors = [
            '.message:last-child',
            '.response:last-child', 
            '.assistant-message:last-child',
            '[data-testid*="message"]:last-child',
            'pre:last-child'
        ];
        
        for (const selector of responseSelectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    const text = await element.textContent();
                    if (text && text.length > 100) {
                        console.log('✅ 成功提取翻译结果');
                        return text;
                    }
                }
            } catch (e) {
                continue;
            }
        }
        
        throw new Error('❌ 未能提取到翻译结果');
        """
        
        return self.execute_browser_mcp_command(extract_script)
    
    def save_translation_result(self, translation_text):
        """保存翻译结果"""
        try:
            output_file = "output/chinese_translation.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translation_text)
            print(f"✅ 翻译结果已保存到: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ 保存翻译结果失败: {e}")
            return None
    
    def execute_full_automation(self):
        """执行完整的自动化流程"""
        print("🎯 开始Browser MCP完全自动化翻译")
        print("="*60)
        
        # 1. 读取翻译提示词
        print("📖 步骤1: 读取翻译提示词")
        prompt_text = self.read_translation_prompt()
        if not prompt_text:
            return False
        print("✅ 翻译提示词读取成功")
        
        # 2. 导航到Sider.AI (已经打开，跳过)
        print("\n🌐 步骤2: Sider.AI已打开，继续...")
        
        # 3. 等待登录
        print("\n🔑 步骤3: 检查登录状态")
        if not self.wait_for_login():
            return False
        
        # 4. 选择AI模型
        print("\n🤖 步骤4: 选择AI模型")
        self.select_ai_model()
        
        # 5. 输入翻译提示词
        print("\n📝 步骤5: 输入翻译提示词")
        if not self.input_translation_prompt(prompt_text):
            print("❌ 输入翻译提示词失败")
            return False
        
        # 6. 发送消息
        print("\n🚀 步骤6: 发送翻译请求")
        if not self.send_message():
            print("❌ 发送翻译请求失败")
            return False
        
        # 7. 等待翻译完成
        print("\n⏳ 步骤7: 等待翻译完成")
        translation_result = self.wait_for_translation()
        if not translation_result:
            print("❌ 等待翻译完成失败")
            return False
        
        # 8. 保存翻译结果
        print("\n💾 步骤8: 保存翻译结果")
        output_file = self.save_translation_result(translation_result)
        
        if output_file:
            print(f"\n🎉 Browser MCP自动化翻译完成!")
            print(f"📁 翻译结果: {output_file}")
            print("\n🎬 下一步: 运行以下命令生成双语视频:")
            print("   python create_bilingual_video.py")
            return True
        else:
            return False

def main():
    """主函数"""
    executor = BrowserMCPExecutor()
    
    try:
        success = executor.execute_full_automation()
        if success:
            print("\n✅ 完全自动化翻译成功完成!")
        else:
            print("\n❌ 自动化翻译失败")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\n❌ 执行过程中出现错误: {e}")

if __name__ == "__main__":
    main() 