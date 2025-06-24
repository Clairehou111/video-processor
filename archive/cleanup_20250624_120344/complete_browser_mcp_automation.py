#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全自动化Browser MCP Sider.AI翻译器
使用Browser MCP实现从文件上传到翻译完成的全流程自动化
"""

import json
import subprocess
import time
import os
import sys
from pathlib import Path

class CompleteBrowserMCPAutomation:
    """完全自动化Browser MCP Sider.AI翻译器"""
    
    def __init__(self):
        self.sider_url = "https://sider.ai/chat"
        self.output_dir = "output"
        self.mcp_config_file = "mcp_config.json"
        
    def read_subtitle_content(self):
        """读取字幕内容"""
        subtitle_file = "output/subtitles_for_translation.txt"
        if not os.path.exists(subtitle_file):
            print(f"❌ 字幕文件不存在: {subtitle_file}")
            return None
        
        try:
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            print("✅ 字幕内容读取成功")
            return content
        except Exception as e:
            print(f"❌ 读取字幕文件失败: {e}")
            return None
    
    def create_browser_mcp_automation_script(self, subtitle_content):
        """创建Browser MCP完全自动化脚本"""
        
        # 转义特殊字符
        escaped_content = subtitle_content.replace('`', '\\`').replace('${', '\\${').replace('"', '\\"')
        
        automation_script = f'''
// 完全自动化Browser MCP Sider.AI翻译脚本
console.log("🚀 开始完全自动化Sider.AI翻译...");

async function completeAutomation() {{
    try {{
        console.log("🌐 导航到Sider.AI...");
        await page.goto("{self.sider_url}", {{ waitUntil: 'networkidle' }});
        await page.waitForTimeout(3000);
        
        console.log("🔍 查找并等待页面加载完成...");
        
        // 步骤1: 等待登录状态检查
        console.log("🔑 检查登录状态...");
        let loginAttempts = 0;
        const maxLoginAttempts = 10;
        
        while (loginAttempts < maxLoginAttempts) {{
            try {{
                // 查找聊天输入框确认已登录
                const chatInput = await page.$('textarea, div[contenteditable="true"], input[type="text"]');
                if (chatInput) {{
                    console.log("✅ 已登录，找到聊天输入框");
                    break;
                }}
                
                await page.waitForTimeout(2000);
                loginAttempts++;
            }} catch (e) {{
                console.log("检查登录状态时出错:", e);
                loginAttempts++;
                await page.waitForTimeout(2000);
            }}
        }}
        
        if (loginAttempts >= maxLoginAttempts) {{
            throw new Error("❌ 登录检查超时，请确保已登录Sider.AI");
        }}
        
        // 步骤2: 查找聊天输入框
        console.log("📝 查找聊天输入框...");
        const chatInputSelectors = [
            'textarea[placeholder*="Message"]',
            'textarea[placeholder*="Type"]',
            'textarea[placeholder*="Ask"]',
            'div[contenteditable="true"]',
            'textarea',
            'input[type="text"]'
        ];
        
        let chatInput = null;
        for (const selector of chatInputSelectors) {{
            try {{
                chatInput = await page.$(selector);
                if (chatInput) {{
                    console.log(`✅ 找到聊天输入框: ${{selector}}`);
                    break;
                }}
            }} catch (e) {{
                continue;
            }}
        }}
        
        if (!chatInput) {{
            throw new Error("❌ 未找到聊天输入框");
        }}
        
        // 步骤3: 输入翻译内容
        console.log("📝 输入翻译内容...");
        await chatInput.fill(`{escaped_content}`);
        console.log("✅ 翻译内容已输入");
        
        // 步骤4: 发送消息
        console.log("🚀 发送翻译请求...");
        
        // 方法1: 按回车键
        try {{
            await page.keyboard.press('Enter');
            console.log("✅ 已按回车键发送");
        }} catch (e) {{
            console.log("⚠️ 回车键发送失败，尝试点击发送按钮");
            
            // 方法2: 查找发送按钮
            const sendSelectors = [
                'button[aria-label*="Send"]',
                'button[title*="Send"]',
                'button:has-text("Send")',
                'button:has-text("发送")',
                'button[type="submit"]'
            ];
            
            let sendButton = null;
            for (const selector of sendSelectors) {{
                try {{
                    sendButton = await page.$(selector);
                    if (sendButton) {{
                        await sendButton.click();
                        console.log("✅ 已点击发送按钮");
                        break;
                    }}
                }} catch (e) {{
                    continue;
                }}
            }}
        }}
        
        // 步骤5: 等待翻译完成
        console.log("⏳ 等待翻译完成...");
        
        let translationResult = null;
        let waitTime = 0;
        const maxWaitTime = 120000; // 2分钟
        const checkInterval = 3000; // 3秒检查一次
        
        while (waitTime < maxWaitTime) {{
            await page.waitForTimeout(checkInterval);
            waitTime += checkInterval;
            
            try {{
                // 查找响应内容
                const responseSelectors = [
                    'div[data-testid*="message"]:last-child',
                    '.message:last-child',
                    '.response:last-child',
                    '.assistant-message:last-child',
                    'pre:last-child',
                    'div:last-child'
                ];
                
                for (const selector of responseSelectors) {{
                    try {{
                        const responseElement = await page.$(selector);
                        if (responseElement) {{
                            const responseText = await responseElement.textContent();
                            
                            // 检查是否是有效的翻译结果
                            if (responseText && 
                                responseText.length > 500 && 
                                (responseText.includes('1.') || responseText.includes('翻译') || responseText.includes('中文'))) {{
                                translationResult = responseText;
                                console.log("✅ 检测到翻译结果");
                                break;
                            }}
                        }}
                    }} catch (e) {{
                        continue;
                    }}
                }}
                
                if (translationResult) break;
                
                console.log(`⏳ 等待中... (${{Math.floor(waitTime/1000)}}s/${{maxWaitTime/1000}}s)`);
                
            }} catch (e) {{
                console.log("检查翻译结果时出错:", e);
            }}
        }}
        
        if (!translationResult) {{
            throw new Error("❌ 等待翻译完成超时");
        }}
        
        // 步骤6: 保存翻译结果
        console.log("💾 保存翻译结果...");
        
        const fs = require('fs');
        const outputFile = './output/sider_chinese_translation.txt';
        fs.writeFileSync(outputFile, translationResult);
        
        console.log("🎉 完全自动化翻译完成!");
        console.log(`📁 翻译结果已保存: ${{outputFile}}`);
        console.log(`📊 翻译内容长度: ${{translationResult.length}} 字符`);
        
        return {{
            success: true,
            translationFile: outputFile,
            translationLength: translationResult.length,
            translationPreview: translationResult.substring(0, 200) + "..."
        }};
        
    }} catch (error) {{
        console.error("❌ 自动化翻译失败:", error);
        return {{
            success: false,
            error: error.message
        }};
    }}
}}

// 执行完全自动化
completeAutomation().then(result => {{
    if (result.success) {{
        console.log("🎉 自动化翻译成功完成!");
        console.log("结果:", result);
    }} else {{
        console.error("❌ 自动化翻译失败:", result.error);
    }}
}});
'''
        
        # 保存自动化脚本
        script_file = os.path.join(self.output_dir, "complete_browser_mcp_automation.js")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(automation_script)
        
        print(f"📝 完全自动化脚本已保存: {script_file}")
        return script_file
    
    def execute_complete_workflow(self):
        """执行完整的自动化工作流"""
        print("�� 开始完全自动化Sider.AI翻译工作流")
        print("="*60)
        
        # 步骤1: 读取字幕内容
        print("📖 步骤1: 读取字幕内容")
        subtitle_content = self.read_subtitle_content()
        if not subtitle_content:
            return False
        
        # 步骤2: 创建自动化脚本
        print("\n📝 步骤2: 创建Browser MCP自动化脚本")
        automation_script = self.create_browser_mcp_automation_script(subtitle_content)
        
        # 步骤3: 执行Browser MCP自动化
        print("\n🚀 步骤3: 执行Browser MCP自动化")
        print("="*60)
        print("🎯 启动Browser MCP自动化翻译")
        print("📋 请确保:")
        print("   1. 已安装Browser MCP扩展")
        print("   2. 已登录Sider.AI账户")
        print("   3. Chrome浏览器已打开")
        print("="*60)
        
        try:
            # 直接运行JavaScript脚本
            print("🔧 执行Browser MCP自动化脚本...")
            
            # 使用node直接运行脚本
            result = subprocess.run(
                ["node", automation_script],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                print("✅ Browser MCP自动化执行成功")
                print(result.stdout)
                
                # 检查翻译结果
                if self.check_translation_result():
                    print("\n🎬 创建双语视频...")
                    self.create_bilingual_video()
                    return True
                else:
                    print("❌ 翻译结果检查失败")
                    return False
            else:
                print(f"❌ Browser MCP自动化执行失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 执行Browser MCP自动化时出错: {e}")
            return False
    
    def check_translation_result(self):
        """检查翻译结果"""
        result_file = "output/sider_chinese_translation.txt"
        
        if not os.path.exists(result_file):
            print("❌ 翻译结果文件不存在")
            return False
        
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if len(content) < 100:
                print("❌ 翻译结果内容太短，可能失败")
                return False
            
            print(f"✅ 翻译结果检查通过，长度: {len(content)} 字符")
            print(f"📄 预览: {content[:200]}...")
            return True
            
        except Exception as e:
            print(f"❌ 检查翻译结果时出错: {e}")
            return False
    
    def create_bilingual_video(self):
        """创建双语视频"""
        print("🎬 开始创建双语视频...")
        
        try:
            # 调用现有的双语视频创建脚本
            result = subprocess.run(
                [sys.executable, "create_bilingual_video.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                print("✅ 双语视频创建成功")
                print(result.stdout)
                return True
            else:
                print(f"❌ 双语视频创建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 创建双语视频时出错: {e}")
            return False

def main():
    """主函数"""
    automator = CompleteBrowserMCPAutomation()
    automator.execute_complete_workflow()

if __name__ == "__main__":
    main()
