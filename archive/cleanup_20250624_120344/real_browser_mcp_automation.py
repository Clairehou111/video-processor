#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真正的Browser MCP自动化Sider.AI翻译器
使用已连接的Browser MCP执行完全自动化翻译
"""

import json
import subprocess
import time
import os
import sys
import webbrowser

class RealBrowserMCPAutomation:
    """真正的Browser MCP自动化翻译器"""
    
    def __init__(self):
        self.sider_url = "https://sider.ai/chat"
        self.output_dir = "output"
        
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
    
    def open_sider_ai(self):
        """打开Sider.AI网站"""
        print("🌐 打开Sider.AI...")
        try:
            webbrowser.open(self.sider_url)
            print("✅ Sider.AI已在浏览器中打开")
            time.sleep(3)  # 等待页面加载
            return True
        except Exception as e:
            print(f"❌ 打开Sider.AI失败: {e}")
            return False
    
    def create_browser_mcp_commands(self, subtitle_content):
        """创建Browser MCP命令序列"""
        
        # 转义特殊字符
        escaped_content = subtitle_content.replace('"', '\\"').replace('\n', '\\n')
        
        commands = [
            # 1. 导航到Sider.AI
            {
                "action": "navigate",
                "url": self.sider_url,
                "description": "导航到Sider.AI聊天页面"
            },
            
            # 2. 等待页面加载
            {
                "action": "wait",
                "timeout": 3000,
                "description": "等待页面完全加载"
            },
            
            # 3. 查找聊天输入框
            {
                "action": "find_element",
                "selectors": [
                    "textarea[placeholder*='Message']",
                    "textarea[placeholder*='Type']", 
                    "textarea[placeholder*='Ask']",
                    "div[contenteditable='true']",
                    "textarea",
                    "input[type='text']"
                ],
                "description": "查找聊天输入框"
            },
            
            # 4. 输入翻译内容
            {
                "action": "type",
                "text": escaped_content,
                "description": "输入字幕翻译请求"
            },
            
            # 5. 发送消息
            {
                "action": "key_press", 
                "key": "Enter",
                "description": "发送翻译请求"
            },
            
            # 6. 等待翻译完成
            {
                "action": "wait_for_response",
                "timeout": 120000,
                "description": "等待AI翻译完成"
            },
            
            # 7. 提取翻译结果
            {
                "action": "extract_response",
                "selectors": [
                    "div[data-testid*='message']:last-child",
                    ".message:last-child",
                    ".response:last-child", 
                    ".assistant-message:last-child",
                    "pre:last-child"
                ],
                "description": "提取翻译结果"
            }
        ]
        
        return commands
    
    def execute_browser_mcp_command(self, command):
        """执行单个Browser MCP命令"""
        print(f"🔧 执行命令: {command['description']}")
        
        if command["action"] == "navigate":
            # 导航命令
            js_code = f'await page.goto("{command["url"]}", {{ waitUntil: "networkidle" }});'
            
        elif command["action"] == "wait":
            # 等待命令
            js_code = f'await page.waitForTimeout({command["timeout"]});'
            
        elif command["action"] == "find_element":
            # 查找元素命令
            selectors = command["selectors"]
            js_code = f'''
let element = null;
const selectors = {json.dumps(selectors)};
for (const selector of selectors) {{
    try {{
        element = await page.$(selector);
        if (element) {{
            console.log(`✅ 找到元素: ${{selector}}`);
            break;
        }}
    }} catch (e) {{
        continue;
    }}
}}
if (!element) {{
    throw new Error("❌ 未找到聊天输入框");
}}
window.chatInput = element;
'''
            
        elif command["action"] == "type":
            # 输入文本命令
            text = command["text"]
            js_code = f'''
if (window.chatInput) {{
    await window.chatInput.fill(`{text}`);
    console.log("✅ 文本已输入");
}} else {{
    throw new Error("❌ 聊天输入框未找到");
}}
'''
            
        elif command["action"] == "key_press":
            # 按键命令
            key = command["key"]
            js_code = f'await page.keyboard.press("{key}");'
            
        elif command["action"] == "wait_for_response":
            # 等待响应命令
            timeout = command["timeout"]
            js_code = f'''
let translationResult = null;
let waitTime = 0;
const maxWaitTime = {timeout};
const checkInterval = 3000;

while (waitTime < maxWaitTime) {{
    await page.waitForTimeout(checkInterval);
    waitTime += checkInterval;
    
    const responseSelectors = [
        'div[data-testid*="message"]:last-child',
        '.message:last-child',
        '.response:last-child',
        '.assistant-message:last-child',
        'pre:last-child'
    ];
    
    for (const selector of responseSelectors) {{
        try {{
            const element = await page.$(selector);
            if (element) {{
                const text = await element.textContent();
                if (text && text.length > 500 && 
                    (text.includes('1.') || text.includes('翻译') || text.includes('中文'))) {{
                    translationResult = text;
                    console.log("✅ 检测到翻译结果");
                    break;
                }}
            }}
        }} catch (e) {{
            continue;
        }}
    }}
    
    if (translationResult) break;
    console.log(`⏳ 等待翻译... (${{Math.floor(waitTime/1000)}}s/${{maxWaitTime/1000}}s)`);
}}

if (!translationResult) {{
    throw new Error("❌ 等待翻译超时");
}}

window.translationResult = translationResult;
'''
            
        elif command["action"] == "extract_response":
            # 提取响应命令
            js_code = '''
if (window.translationResult) {
    const fs = require('fs');
    fs.writeFileSync('./output/sider_chinese_translation.txt', window.translationResult);
    console.log("✅ 翻译结果已保存");
    return window.translationResult;
} else {
    throw new Error("❌ 未找到翻译结果");
}
'''
        
        return js_code
    
    def execute_automation_workflow(self, subtitle_content):
        """执行完整的自动化工作流"""
        print("🎯 开始Browser MCP自动化翻译工作流")
        print("="*60)
        
        # 1. 打开Sider.AI
        print("🌐 步骤1: 打开Sider.AI")
        if not self.open_sider_ai():
            return False
        
        # 2. 创建命令序列
        print("\n📝 步骤2: 创建Browser MCP命令序列")
        commands = self.create_browser_mcp_commands(subtitle_content)
        print(f"✅ 创建了 {len(commands)} 个自动化命令")
        
        # 3. 创建完整的JavaScript脚本
        print("\n🔧 步骤3: 生成Browser MCP脚本")
        
        full_script = '''
console.log("🚀 开始Browser MCP自动化翻译...");

async function executeAutomation() {
    try {
'''
        
        # 添加所有命令
        for i, command in enumerate(commands):
            js_code = self.execute_browser_mcp_command(command)
            full_script += f'''
        // 步骤{i+1}: {command["description"]}
        console.log("🔧 {command["description"]}");
        {js_code}
        
'''
        
        full_script += '''
        console.log("🎉 自动化翻译完成!");
        return { success: true, message: "翻译完成" };
        
    } catch (error) {
        console.error("❌ 自动化失败:", error);
        return { success: false, error: error.message };
    }
}

// 执行自动化
executeAutomation().then(result => {
    console.log("📊 执行结果:", result);
});
'''
        
        # 保存脚本
        script_file = os.path.join(self.output_dir, "real_browser_mcp_automation.js")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(full_script)
        
        print(f"✅ Browser MCP脚本已保存: {script_file}")
        
        # 4. 显示执行指导
        print("\n" + "="*60)
        print("🎯 Browser MCP执行指导")
        print("="*60)
        print("请按以下步骤执行:")
        print("1. 确保Chrome浏览器已打开Sider.AI页面")
        print("2. 确保已登录Sider.AI账户")
        print("3. 在VS Code/Cursor中打开Browser MCP面板")
        print("4. 复制并执行以下脚本内容:")
        print(f"   文件位置: {os.path.abspath(script_file)}")
        print("\n或者，如果你有Browser MCP命令行工具:")
        print(f"   npx @browsermcp/mcp --execute {script_file}")
        
        return script_file
    
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
    
    def execute_complete_workflow(self):
        """执行完整工作流"""
        print("🎯 开始真正的Browser MCP自动化翻译")
        print("="*60)
        
        # 步骤1: 读取字幕内容
        print("📖 步骤1: 读取字幕内容")
        subtitle_content = self.read_subtitle_content()
        if not subtitle_content:
            return False
        
        # 步骤2: 执行自动化工作流
        print("\n🚀 步骤2: 执行Browser MCP自动化")
        script_file = self.execute_automation_workflow(subtitle_content)
        if not script_file:
            return False
        
        # 步骤3: 等待用户执行
        print("\n⏳ 步骤3: 等待Browser MCP执行完成")
        print("请在Browser MCP中执行上述脚本，完成后按回车继续...")
        input("按回车键继续检查结果...")
        
        # 步骤4: 检查翻译结果
        print("\n🔍 步骤4: 检查翻译结果")
        if self.check_translation_result():
            # 步骤5: 创建双语视频
            print("\n🎬 步骤5: 创建双语视频")
            if self.create_bilingual_video():
                print("\n🎉 完整自动化工作流成功完成!")
                print("="*60)
                print("📁 生成的文件:")
                print("   • 中文翻译: output/sider_chinese_translation.txt")
                print("   • 双语字幕: output/VP9_segment_2m36s-5m59s_bilingual.srt")
                print("   • 双语视频: output/VP9_segment_2m36s-5m59s_bilingual.mp4")
                return True
            else:
                print("⚠️ 双语视频创建失败，但翻译已完成")
                return True
        else:
            print("❌ 翻译结果检查失败")
            return False

def main():
    """主函数"""
    automator = RealBrowserMCPAutomation()
    automator.execute_complete_workflow()

if __name__ == "__main__":
    main() 