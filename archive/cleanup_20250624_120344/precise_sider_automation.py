#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确的Sider.AI自动化脚本
基于用户提供的具体页面信息进行自动化
"""

import json
import subprocess
import time
import os

def read_translation_prompt():
    """读取翻译提示词"""
    try:
        with open("output/sider_translation_prompt.txt", 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ 读取翻译提示词失败: {e}")
        return None

def create_browser_automation_script():
    """创建浏览器自动化脚本"""
    
    prompt_text = read_translation_prompt()
    if not prompt_text:
        return None
    
    # 转义特殊字符
    escaped_prompt = prompt_text.replace('`', '\\`').replace('${', '\\${').replace('"', '\\"')
    
    automation_script = f'''
// Sider.AI精确自动化脚本
console.log("🎯 开始Sider.AI自动化翻译...");

async function automateSiderTranslation() {{
    try {{
        // 等待页面完全加载
        console.log("⏳ 等待页面加载...");
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // 步骤1: 检查登录状态 (查找unlimited文字)
        console.log("🔑 检查登录状态...");
        const unlimitedElements = document.querySelectorAll('*');
        let isLoggedIn = false;
        for (let element of unlimitedElements) {{
            if (element.textContent && element.textContent.toLowerCase().includes('unlimited')) {{
                console.log("✅ 已登录 (发现unlimited标识)");
                isLoggedIn = true;
                break;
            }}
        }}
        
        if (!isLoggedIn) {{
            console.log("⚠️ 未检测到登录状态，继续尝试...");
        }}
        
        // 步骤2: 点击Switch Model按钮选择模型
        console.log("🤖 查找Switch Model按钮...");
        const switchModelSelectors = [
            'button:contains("switch model")',
            'button:contains("Switch Model")',
            '[data-testid*="switch"]',
            '[aria-label*="switch"]',
            '.switch-model',
            'button[class*="switch"]'
        ];
        
        let switchButton = null;
        
        // 使用更广泛的查找方法
        const allButtons = document.querySelectorAll('button, div[role="button"], span[role="button"]');
        for (let button of allButtons) {{
            const text = button.textContent || button.innerText || '';
            if (text.toLowerCase().includes('switch') && text.toLowerCase().includes('model')) {{
                switchButton = button;
                console.log("✅ 找到Switch Model按钮");
                break;
            }}
        }}
        
        if (switchButton) {{
            console.log("🔄 点击Switch Model按钮...");
            switchButton.click();
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // 查找Claude选项
            console.log("🔍 查找Claude模型选项...");
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const modelOptions = document.querySelectorAll('*');
            for (let option of modelOptions) {{
                const text = option.textContent || option.innerText || '';
                if (text.toLowerCase().includes('claude') && option.tagName !== 'SCRIPT') {{
                    console.log("✅ 找到Claude选项，点击选择...");
                    option.click();
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    break;
                }}
            }}
        }} else {{
            console.log("⚠️ 未找到Switch Model按钮，使用默认模型");
        }}
        
        // 步骤3: 查找聊天输入框
        console.log("🔍 查找聊天输入框...");
        const inputSelectors = [
            'textarea[placeholder*="Message"]',
            'textarea[placeholder*="Type"]',
            'textarea[placeholder*="Ask"]',
            'textarea[placeholder*="message"]',
            'div[contenteditable="true"]',
            'textarea',
            'input[type="text"]',
            '[data-testid*="input"]',
            '[data-testid*="message"]'
        ];
        
        let chatInput = null;
        for (let selector of inputSelectors) {{
            const elements = document.querySelectorAll(selector);
            for (let element of elements) {{
                if (element.offsetParent !== null && !element.disabled) {{ // 可见且未禁用
                    chatInput = element;
                    console.log(`✅ 找到聊天输入框: ${{selector}}`);
                    break;
                }}
            }}
            if (chatInput) break;
        }}
        
        if (!chatInput) {{
            throw new Error("❌ 未找到聊天输入框");
        }}
        
        // 步骤4: 输入翻译提示词
        console.log("📝 输入翻译提示词...");
        chatInput.focus();
        chatInput.value = '';
        
        // 分段输入以避免长文本问题
        const promptText = `{escaped_prompt}`;
        chatInput.value = promptText;
        
        // 触发input事件
        const inputEvent = new Event('input', {{ bubbles: true }});
        chatInput.dispatchEvent(inputEvent);
        
        console.log("✅ 翻译提示词已输入");
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 步骤5: 发送消息
        console.log("🚀 发送翻译请求...");
        
        // 方式1: 尝试按回车键
        const enterEvent = new KeyboardEvent('keydown', {{
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            bubbles: true
        }});
        chatInput.dispatchEvent(enterEvent);
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 方式2: 查找发送按钮
        const sendSelectors = [
            'button[aria-label*="Send"]',
            'button[title*="Send"]',
            'button:contains("Send")',
            'button:contains("发送")',
            '[data-testid*="send"]',
            'button[type="submit"]',
            '.send-button',
            '[role="button"][aria-label*="send"]'
        ];
        
        let sendButton = null;
        const allSendButtons = document.querySelectorAll('button, div[role="button"], span[role="button"]');
        for (let button of allSendButtons) {{
            const ariaLabel = button.getAttribute('aria-label') || '';
            const title = button.getAttribute('title') || '';
            const text = button.textContent || button.innerText || '';
            
            if (ariaLabel.toLowerCase().includes('send') || 
                title.toLowerCase().includes('send') ||
                text.toLowerCase().includes('send') ||
                text.includes('发送')) {{
                sendButton = button;
                console.log("✅ 找到发送按钮");
                break;
            }}
        }}
        
        if (sendButton) {{
            console.log("🔄 点击发送按钮...");
            sendButton.click();
        }}
        
        console.log("✅ 翻译请求已发送");
        
        // 步骤6: 等待翻译完成
        console.log("⏳ 等待翻译完成...");
        let translationResult = null;
        let maxWaitTime = 60000; // 60秒
        let startTime = Date.now();
        
        while (Date.now() - startTime < maxWaitTime) {{
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            // 查找响应内容
            const responseElements = document.querySelectorAll('div, p, pre, span');
            for (let element of responseElements) {{
                const text = element.textContent || element.innerText || '';
                if (text.length > 200 && 
                    text.includes('1.') && 
                    text.includes('2.') && 
                    text.includes('3.') &&
                    (text.includes('翻译') || text.includes('中文'))) {{
                    translationResult = text;
                    console.log("✅ 检测到翻译结果");
                    break;
                }}
            }}
            
            if (translationResult) break;
        }}
        
        if (!translationResult) {{
            throw new Error("❌ 等待翻译响应超时");
        }}
        
        // 步骤7: 显示结果
        console.log("🎉 翻译完成!");
        console.log("📋 翻译结果预览:", translationResult.substring(0, 200) + "...");
        
        // 将结果复制到剪贴板
        if (navigator.clipboard) {{
            try {{
                await navigator.clipboard.writeText(translationResult);
                console.log("✅ 翻译结果已复制到剪贴板");
            }} catch (e) {{
                console.log("⚠️ 无法复制到剪贴板:", e);
            }}
        }}
        
        return translationResult;
        
    }} catch (error) {{
        console.error("❌ 自动化过程中出错:", error);
        throw error;
    }}
}}

// 执行自动化
automateSiderTranslation()
    .then(result => {{
        console.log("🎊 Sider.AI自动化翻译成功完成!");
        alert("翻译完成!\\n\\n翻译结果已复制到剪贴板，请粘贴到终端程序中保存。");
    }})
    .catch(error => {{
        console.error("❌ 自动化翻译失败:", error);
        alert("自动化翻译失败: " + error.message);
    }});
'''
    
    return automation_script

def save_automation_script():
    """保存自动化脚本到文件"""
    script = create_browser_automation_script()
    if not script:
        return None
    
    script_file = "output/sider_automation_script.js"
    try:
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✅ 自动化脚本已保存到: {script_file}")
        return script_file
    except Exception as e:
        print(f"❌ 保存脚本失败: {e}")
        return None

def execute_automation():
    """执行自动化"""
    print("🎯 精确Sider.AI自动化开始")
    print("="*60)
    
    # 1. 创建并保存自动化脚本
    print("📝 步骤1: 创建自动化脚本")
    script_file = save_automation_script()
    if not script_file:
        return False
    
    # 2. 显示执行指导
    print("\\n🔧 步骤2: 执行自动化脚本")
    print("="*50)
    print("请在Sider.AI页面的浏览器控制台中执行以下操作:")
    print()
    print("1. 🌐 确保Sider.AI页面已打开")
    print("2. 🔧 按F12打开开发者工具")
    print("3. 📝 切换到Console标签")
    print("4. 📋 复制并粘贴以下脚本:")
    print()
    
    # 读取并显示脚本内容
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        print("─" * 60)
        print("// 复制以下完整脚本到浏览器控制台:")
        print("─" * 60)
        print(script_content[:500] + "\\n... (完整脚本请查看文件)")
        print("─" * 60)
        
    except Exception as e:
        print(f"❌ 读取脚本文件失败: {e}")
        return False
    
    print()
    print("5. 🚀 按回车执行脚本")
    print("6. ⏳ 等待自动化完成")
    print("7. 📋 翻译完成后会自动复制到剪贴板")
    print()
    print("🎯 脚本将自动完成:")
    print("   ✅ 检查登录状态 (查找unlimited)")
    print("   ✅ 点击Switch Model选择Claude")
    print("   ✅ 输入翻译提示词")
    print("   ✅ 发送翻译请求")
    print("   ✅ 等待翻译完成")
    print("   ✅ 提取并复制翻译结果")
    
    # 3. 等待用户完成
    print("\\n⏳ 步骤3: 等待翻译完成")
    input("执行脚本并完成翻译后，按回车继续...")
    
    # 4. 保存翻译结果
    print("\\n💾 步骤4: 保存翻译结果")
    print("请粘贴从剪贴板复制的翻译结果:")
    print("(输入完成后按两次回车结束)")
    
    lines = []
    empty_count = 0
    
    try:
        while True:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            lines.append(line)
        
        translation_text = '\\n'.join(lines).strip()
        
        if translation_text:
            output_file = "output/chinese_translation.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translation_text)
            print(f"✅ 翻译结果已保存到: {output_file}")
            
            # 5. 询问是否创建双语视频
            print("\\n🎬 步骤5: 创建双语视频")
            choice = input("是否立即创建双语视频? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                try:
                    subprocess.run(["python", "create_bilingual_video.py"], check=True)
                    print("✅ 双语视频创建完成!")
                except Exception as e:
                    print(f"❌ 创建双语视频失败: {e}")
            
            return True
        else:
            print("❌ 未检测到翻译内容")
            return False
            
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    """主函数"""
    try:
        success = execute_automation()
        if success:
            print("\\n🎉 精确自动化翻译成功完成!")
        else:
            print("\\n❌ 自动化翻译失败")
            
    except KeyboardInterrupt:
        print("\\n\\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\\n❌ 执行过程中出现错误: {e}")

if __name__ == "__main__":
    main() 