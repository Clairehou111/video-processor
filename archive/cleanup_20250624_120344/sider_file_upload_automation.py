#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sider.AI文件上传自动化脚本
分析页面元素并实现字幕文件上传功能
"""

import json
import subprocess
import time
import os
import webbrowser
from pathlib import Path

class SiderFileUploadAutomator:
    """Sider.AI文件上传自动化器"""
    
    def __init__(self):
        self.sider_url = "https://sider.ai/chat"
        self.output_dir = "output"
        
    def create_subtitle_file_for_upload(self):
        """创建用于上传的字幕文件"""
        print("📝 准备字幕文件...")
        
        # 读取英文字幕
        english_srt = "output/VP9_segment_2m36s-5m59s_english.srt"
        if not os.path.exists(english_srt):
            print(f"❌ 英文字幕文件不存在: {english_srt}")
            return None
        
        # 创建简化的字幕文本文件用于上传
        upload_file = "output/subtitles_for_translation.txt"
        
        try:
            with open(english_srt, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # 提取纯文本内容
            lines = srt_content.strip().split('\n')
            text_lines = []
            
            for line in lines:
                line = line.strip()
                # 跳过序号和时间戳
                if line and not line.isdigit() and '-->' not in line:
                    text_lines.append(line)
            
            # 创建上传文件
            with open(upload_file, 'w', encoding='utf-8') as f:
                f.write("请将以下英文字幕翻译成中文，保持原有的分段结构：\n\n")
                for i, text in enumerate(text_lines, 1):
                    f.write(f"{i}. {text}\n")
                f.write("\n请提供准确的中文翻译，适合政治喜剧节目的语境。")
            
            print(f"✅ 字幕上传文件已创建: {upload_file}")
            return upload_file
            
        except Exception as e:
            print(f"❌ 创建字幕文件失败: {e}")
            return None
    
    def create_page_analysis_script(self):
        """创建页面元素分析脚本"""
        
        analysis_script = '''
// Sider.AI页面元素分析脚本
console.log("🔍 开始分析Sider.AI页面元素...");

function analyzeSiderPage() {
    console.log("📊 分析页面结构...");
    
    // 1. 查找文件上传相关元素
    console.log("📁 查找文件上传元素...");
    
    const fileUploadSelectors = [
        'input[type="file"]',
        '[data-testid*="upload"]',
        '[data-testid*="file"]',
        '[aria-label*="upload"]',
        '[aria-label*="file"]',
        '.upload-button',
        '.file-upload',
        'button[title*="upload"]',
        'button[title*="file"]',
        '*[class*="upload"]',
        '*[class*="file"]'
    ];
    
    let foundElements = [];
    
    fileUploadSelectors.forEach(selector => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (element.offsetParent !== null || element.type === 'file') {
                    foundElements.push({
                        selector: selector,
                        element: element,
                        tagName: element.tagName,
                        type: element.type,
                        className: element.className,
                        id: element.id,
                        ariaLabel: element.getAttribute('aria-label'),
                        title: element.getAttribute('title'),
                        textContent: element.textContent?.trim()
                    });
                }
            });
        } catch (e) {
            console.log(`查找选择器 ${selector} 时出错:`, e);
        }
    });
    
    if (foundElements.length > 0) {
        console.log("✅ 找到文件上传相关元素:");
        foundElements.forEach((item, index) => {
            console.log(`${index + 1}. ${item.tagName} - ${item.selector}`);
            console.log(`   类名: ${item.className}`);
            console.log(`   ID: ${item.id}`);
            console.log(`   标签: ${item.ariaLabel}`);
            console.log(`   标题: ${item.title}`);
            console.log(`   文本: ${item.textContent}`);
            console.log("---");
        });
    } else {
        console.log("⚠️ 未找到明显的文件上传元素");
    }
    
    // 2. 查找聊天输入区域附近的按钮和图标
    console.log("🔍 查找聊天输入区域附近的元素...");
    
    const chatInputSelectors = [
        'textarea[placeholder*="Message"]',
        'textarea[placeholder*="Type"]',
        'textarea[placeholder*="Ask"]',
        'div[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ];
    
    let chatInput = null;
    for (const selector of chatInputSelectors) {
        const elements = document.querySelectorAll(selector);
        for (const element of elements) {
            if (element.offsetParent !== null && !element.disabled) {
                chatInput = element;
                console.log(`✅ 找到聊天输入框: ${selector}`);
                break;
            }
        }
        if (chatInput) break;
    }
    
    if (chatInput) {
        // 查找输入框附近的按钮和图标
        const parentContainer = chatInput.closest('div, form, section');
        if (parentContainer) {
            console.log("🔍 分析输入框容器内的元素...");
            
            const nearbyButtons = parentContainer.querySelectorAll('button, [role="button"], svg, i, span[class*="icon"]');
            const nearbyElements = [];
            
            nearbyButtons.forEach((element, index) => {
                const rect = element.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    nearbyElements.push({
                        index: index,
                        tagName: element.tagName,
                        className: element.className,
                        id: element.id,
                        ariaLabel: element.getAttribute('aria-label'),
                        title: element.getAttribute('title'),
                        textContent: element.textContent?.trim(),
                        innerHTML: element.innerHTML?.substring(0, 100)
                    });
                }
            });
            
            console.log(`📋 输入框附近找到 ${nearbyElements.length} 个可交互元素:`);
            nearbyElements.forEach(item => {
                console.log(`${item.index + 1}. ${item.tagName} - ${item.className}`);
                console.log(`   文本: ${item.textContent}`);
                console.log(`   标签: ${item.ariaLabel}`);
                console.log(`   HTML: ${item.innerHTML}`);
                console.log("---");
            });
        }
    }
    
    // 3. 查找可能的附件或上传相关图标
    console.log("📎 查找附件相关图标...");
    
    const attachmentKeywords = ['attach', 'clip', 'upload', 'file', 'document', 'paper'];
    const iconElements = document.querySelectorAll('svg, i, span[class*="icon"], [class*="attach"], [class*="clip"], [class*="upload"]');
    
    const attachmentIcons = [];
    iconElements.forEach((element, index) => {
        const classNames = element.className.toLowerCase();
        const ariaLabel = (element.getAttribute('aria-label') || '').toLowerCase();
        const title = (element.getAttribute('title') || '').toLowerCase();
        
        const hasAttachmentKeyword = attachmentKeywords.some(keyword => 
            classNames.includes(keyword) || ariaLabel.includes(keyword) || title.includes(keyword)
        );
        
        if (hasAttachmentKeyword && element.offsetParent !== null) {
            attachmentIcons.push({
                index: index,
                tagName: element.tagName,
                className: element.className,
                ariaLabel: element.getAttribute('aria-label'),
                title: element.getAttribute('title'),
                parentTag: element.parentElement?.tagName
            });
        }
    });
    
    if (attachmentIcons.length > 0) {
        console.log("📎 找到可能的附件图标:");
        attachmentIcons.forEach(item => {
            console.log(`${item.index + 1}. ${item.tagName} - ${item.className}`);
            console.log(`   父元素: ${item.parentTag}`);
            console.log(`   标签: ${item.ariaLabel}`);
            console.log(`   标题: ${item.title}`);
            console.log("---");
        });
    }
    
    // 4. 提供操作建议
    console.log("💡 操作建议:");
    
    if (foundElements.length > 0) {
        console.log("✅ 建议1: 使用找到的文件上传元素");
        const fileInput = foundElements.find(item => item.type === 'file');
        if (fileInput) {
            console.log("   - 直接使用 input[type='file'] 元素上传文件");
        }
    }
    
    if (attachmentIcons.length > 0) {
        console.log("✅ 建议2: 点击附件图标触发文件选择");
        console.log("   - 尝试点击附件相关的图标或按钮");
    }
    
    console.log("✅ 建议3: 使用拖拽方式上传文件");
    console.log("   - 将文件直接拖拽到聊天输入区域");
    
    console.log("🔍 页面分析完成!");
    return {
        fileUploadElements: foundElements,
        attachmentIcons: attachmentIcons,
        chatInput: chatInput ? true : false
    };
}

// 执行分析
const analysisResult = analyzeSiderPage();
console.log("📊 分析结果:", analysisResult);
'''
        
        # 保存分析脚本
        script_file = os.path.join(self.output_dir, "sider_page_analysis.js")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(analysis_script)
        
        print(f"📝 页面分析脚本已保存: {script_file}")
        return script_file
    
    def create_file_upload_automation_script(self, upload_file_path):
        """创建文件上传自动化脚本"""
        
        upload_script = f'''
// Sider.AI文件上传自动化脚本
console.log("📁 开始文件上传自动化...");

async function uploadFileToSider() {{
    try {{
        console.log("🔍 查找文件上传方式...");
        
        // 方式1: 查找隐藏的文件输入框
        console.log("📂 方式1: 查找文件输入框...");
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        if (fileInputs.length > 0) {{
            console.log(`✅ 找到 ${{fileInputs.length}} 个文件输入框`);
            
            // 创建文件对象 (这需要实际的文件内容)
            console.log("⚠️ 需要手动选择文件: {upload_file_path}");
            
            // 触发文件选择对话框
            fileInputs[0].click();
            console.log("✅ 已触发文件选择对话框");
            return true;
        }}
        
        // 方式2: 查找附件按钮
        console.log("📎 方式2: 查找附件按钮...");
        const attachmentSelectors = [
            '[aria-label*="attach"]',
            '[aria-label*="upload"]',
            '[aria-label*="file"]',
            '[title*="attach"]',
            '[title*="upload"]',
            '[title*="file"]',
            'button[class*="attach"]',
            'button[class*="upload"]',
            '*[class*="paperclip"]',
            '*[class*="attachment"]'
        ];
        
        let attachButton = null;
        for (const selector of attachmentSelectors) {{
            const elements = document.querySelectorAll(selector);
            for (const element of elements) {{
                if (element.offsetParent !== null) {{
                    attachButton = element;
                    console.log(`✅ 找到附件按钮: ${{selector}}`);
                    break;
                }}
            }}
            if (attachButton) break;
        }}
        
        if (attachButton) {{
            console.log("🔄 点击附件按钮...");
            attachButton.click();
            
            // 等待文件选择对话框出现
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 再次查找文件输入框
            const newFileInputs = document.querySelectorAll('input[type="file"]');
            if (newFileInputs.length > 0) {{
                console.log("✅ 附件按钮触发了文件输入框");
                return true;
            }}
        }}
        
        // 方式3: 查找可能触发上传的图标
        console.log("🔍 方式3: 查找上传相关图标...");
        const allClickableElements = document.querySelectorAll('button, [role="button"], svg, i');
        
        for (const element of allClickableElements) {{
            const className = element.className.toLowerCase();
            const ariaLabel = (element.getAttribute('aria-label') || '').toLowerCase();
            const title = (element.getAttribute('title') || '').toLowerCase();
            const parentClass = (element.parentElement?.className || '').toLowerCase();
            
            const uploadKeywords = ['upload', 'attach', 'file', 'clip', 'document'];
            const hasUploadKeyword = uploadKeywords.some(keyword => 
                className.includes(keyword) || 
                ariaLabel.includes(keyword) || 
                title.includes(keyword) ||
                parentClass.includes(keyword)
            );
            
            if (hasUploadKeyword && element.offsetParent !== null) {{
                console.log(`🎯 尝试点击可能的上传元素: ${{element.tagName}} - ${{className}}`);
                try {{
                    element.click();
                    await new Promise(resolve => setTimeout(resolve, 500));
                    
                    // 检查是否出现了文件输入框
                    const triggeredInputs = document.querySelectorAll('input[type="file"]');
                    if (triggeredInputs.length > 0) {{
                        console.log("✅ 成功触发文件输入框");
                        return true;
                    }}
                }} catch (e) {{
                    console.log("⚠️ 点击元素失败:", e);
                }}
            }}
        }}
        
        // 方式4: 拖拽上传提示
        console.log("🎯 方式4: 准备拖拽上传...");
        const chatInput = document.querySelector('textarea, div[contenteditable="true"], input[type="text"]');
        
        if (chatInput) {{
            console.log("💡 拖拽上传提示:");
            console.log("1. 打开文件管理器，找到文件: {upload_file_path}");
            console.log("2. 将文件拖拽到聊天输入框区域");
            console.log("3. 松开鼠标完成上传");
            
            // 高亮聊天输入区域
            chatInput.style.border = "3px dashed #007bff";
            chatInput.style.backgroundColor = "#f8f9fa";
            
            setTimeout(() => {{
                chatInput.style.border = "";
                chatInput.style.backgroundColor = "";
            }}, 5000);
            
            return true;
        }}
        
        console.log("❌ 未找到文件上传方式");
        return false;
        
    }} catch (error) {{
        console.error("❌ 文件上传自动化失败:", error);
        return false;
    }}
}}

// 执行文件上传
uploadFileToSider().then(success => {{
    if (success) {{
        console.log("🎉 文件上传准备完成!");
        console.log("💡 如果出现文件选择对话框，请选择: {upload_file_path}");
    }} else {{
        console.log("❌ 文件上传准备失败");
        console.log("💡 请尝试手动拖拽文件到聊天区域");
    }}
}});
'''
        
        # 保存上传脚本
        script_file = os.path.join(self.output_dir, "sider_file_upload.js")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(upload_script)
        
        print(f"📝 文件上传脚本已保存: {script_file}")
        return script_file
    
    def create_manual_instructions(self, upload_file_path):
        """创建手动操作指导"""
        
        instructions = f"""
# Sider.AI文件上传操作指导

## 📁 上传文件信息
- **文件路径**: {os.path.abspath(upload_file_path)}
- **文件类型**: 字幕翻译文本
- **文件大小**: {os.path.getsize(upload_file_path)} 字节

## 🎯 上传方法（按优先级尝试）

### 方法1: 查找上传按钮 ⭐⭐⭐
1. 在Sider.AI聊天界面中查找以下图标或按钮：
   - 📎 回形针图标
   - 📄 文件图标  
   - ⬆️ 上传图标
   - "Attach" 或 "Upload" 按钮

2. 点击找到的上传按钮
3. 在文件选择对话框中选择文件：`{upload_file_path}`

### 方法2: 拖拽上传 ⭐⭐⭐
1. 打开文件管理器，找到文件：`{upload_file_path}`
2. 将文件直接拖拽到Sider.AI的聊天输入框区域
3. 松开鼠标完成上传

### 方法3: 复制粘贴内容 ⭐⭐
如果无法上传文件，可以复制文件内容：
1. 打开文件：`{upload_file_path}`
2. 全选并复制文件内容 (Ctrl+A, Ctrl+C)
3. 在Sider.AI聊天框中粘贴内容 (Ctrl+V)

## 🔍 页面元素查找提示
如果找不到上传按钮，请查找包含以下关键词的元素：
- `attach`, `upload`, `file`, `clip`, `document`
- `paperclip`, `attachment`, `browse`

## ⚡ 自动化脚本
已为你准备了两个脚本：
1. **页面分析脚本**: `output/sider_page_analysis.js`
2. **文件上传脚本**: `output/sider_file_upload.js`

在浏览器开发者工具的控制台中运行这些脚本可以：
- 分析页面结构，找到上传相关元素
- 自动触发文件上传功能

## 📝 上传成功后
文件上传成功后，Sider.AI应该会：
1. 显示文件名或文件内容预览
2. 开始处理翻译请求
3. 返回中文翻译结果

## ❓ 如果遇到问题
1. 确保已登录Sider.AI账户
2. 检查文件大小是否超过限制
3. 尝试刷新页面重新开始
4. 使用复制粘贴方法作为备选方案
"""
        
        # 保存操作指导
        guide_file = os.path.join(self.output_dir, "SIDER_UPLOAD_GUIDE.md")
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📖 操作指导已保存: {guide_file}")
        return guide_file
    
    def execute_complete_workflow(self):
        """执行完整的文件上传工作流"""
        print("🎯 开始Sider.AI文件上传完整工作流")
        print("="*60)
        
        # 1. 创建上传文件
        print("📝 步骤1: 准备上传文件")
        upload_file = self.create_subtitle_file_for_upload()
        if not upload_file:
            return False
        
        # 2. 创建页面分析脚本
        print("\n🔍 步骤2: 创建页面分析脚本")
        analysis_script = self.create_page_analysis_script()
        
        # 3. 创建文件上传脚本
        print("\n📁 步骤3: 创建文件上传脚本") 
        upload_script = self.create_file_upload_automation_script(upload_file)
        
        # 4. 创建操作指导
        print("\n📖 步骤4: 创建操作指导")
        guide_file = self.create_manual_instructions(upload_file)
        
        # 5. 打开Sider.AI
        print("\n🌐 步骤5: 打开Sider.AI")
        try:
            webbrowser.open(self.sider_url)
            print("✅ Sider.AI已在浏览器中打开")
        except Exception as e:
            print(f"⚠️ 无法自动打开浏览器: {e}")
            print(f"请手动访问: {self.sider_url}")
        
        # 6. 显示完成信息
        print("\n" + "="*60)
        print("🎉 文件上传工作流准备完成!")
        print("="*60)
        
        print(f"\n📁 准备好的文件:")
        print(f"   • 上传文件: {os.path.abspath(upload_file)}")
        print(f"   • 页面分析脚本: {os.path.abspath(analysis_script)}")
        print(f"   • 上传自动化脚本: {os.path.abspath(upload_script)}")
        print(f"   • 操作指导: {os.path.abspath(guide_file)}")
        
        print(f"\n🎯 下一步操作:")
        print("1. 🔑 登录你的Sider.AI账户")
        print("2. 📎 查找并点击文件上传按钮，或直接拖拽文件")
        print("3. 📄 选择上传文件进行翻译")
        print("4. ⏳ 等待翻译完成")
        print("5. 💾 保存翻译结果")
        
        print(f"\n💡 详细操作指导请查看: {guide_file}")
        
        return True

def main():
    """主函数"""
    automator = SiderFileUploadAutomator()
    automator.execute_complete_workflow()

if __name__ == "__main__":
    main() 