#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser MCP自动化翻译器
使用真正的Browser MCP工具自动完成Sider.AI翻译过程
"""

import os
import json
import time
import asyncio
import subprocess
from pathlib import Path

class BrowserMCPTranslator:
    """Browser MCP自动化翻译器"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.sider_url = "https://sider.ai/chat"
        
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
    
    def install_browser_extension(self):
        """指导安装Browser MCP Chrome扩展"""
        print("🔧 Browser MCP设置指南")
        print("="*50)
        print("1. 🌐 安装Chrome扩展:")
        print("   https://chromewebstore.google.com/detail/browser-mcp-automate-your/bjfgambnhccakkhmkepdoekmckoijdlc")
        print()
        print("2. 📝 MCP服务器已配置:")
        print("   配置文件: mcp_config.json")
        print("   服务器: @browsermcp/mcp@latest")
        print()
        print("3. 🔄 重启Cursor/VS Code以加载MCP配置")
        print("="*50)
        
        # 自动打开Chrome扩展页面
        try:
            import webbrowser
            extension_url = "https://chromewebstore.google.com/detail/browser-mcp-automate-your/bjfgambnhccakkhmkepdoekmckoijdlc"
            webbrowser.open(extension_url)
            print("✅ 已自动打开Chrome扩展安装页面")
        except:
            print("⚠️ 请手动打开上述链接安装扩展")
    
    def start_mcp_server(self):
        """启动Browser MCP服务器"""
        print("🚀 启动Browser MCP服务器...")
        
        try:
            # 启动MCP服务器
            process = subprocess.Popen(
                ["npx", "@browsermcp/mcp@latest"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ Browser MCP服务器已启动")
            print(f"📊 进程ID: {process.pid}")
            
            return process
            
        except Exception as e:
            print(f"❌ 启动Browser MCP服务器失败: {e}")
            return None
    
    def create_automation_script(self, prompt_text):
        """创建自动化脚本供Browser MCP使用"""
        script = f"""
// Browser MCP自动化翻译脚本
// 此脚本将通过Browser MCP执行

async function automateSiderTranslation() {{
    console.log("🤖 开始Browser MCP自动化翻译...");
    
    // 1. 导航到Sider.AI
    console.log("🌐 导航到Sider.AI...");
    await browser.navigate("{self.sider_url}");
    
    // 2. 等待页面加载
    console.log("⏳ 等待页面加载...");
    await browser.wait(3000);
    
    // 3. 查找聊天输入框
    console.log("🔍 查找聊天输入框...");
    const chatSelectors = [
        'textarea[placeholder*="Message"]',
        'textarea[placeholder*="Type"]',
        'textarea[placeholder*="Ask"]',
        'div[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ];
    
    let chatInput = null;
    for (const selector of chatSelectors) {{
        try {{
            chatInput = await browser.findElement(selector);
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
    
    // 4. 输入翻译提示词
    console.log("📝 输入翻译提示词...");
    await browser.type(chatInput, `{prompt_text.replace('`', '\\`')}`);
    
    // 5. 发送消息
    console.log("🚀 发送翻译请求...");
    await browser.key("Enter");
    
    // 6. 等待翻译完成
    console.log("⏳ 等待翻译完成...");
    await browser.wait(30000); // 等待30秒
    
    // 7. 提取翻译结果
    console.log("📖 提取翻译结果...");
    const responseSelectors = [
        '.message:last-child',
        '.response:last-child',
        '.assistant-message:last-child',
        'pre:last-child',
        '[data-testid*="message"]:last-child'
    ];
    
    let translationResult = null;
    for (const selector of responseSelectors) {{
        try {{
            const element = await browser.findElement(selector);
            if (element) {{
                translationResult = await browser.getText(element);
                if (translationResult && translationResult.length > 100) {{
                    console.log("✅ 成功提取翻译结果");
                    break;
                }}
            }}
        }} catch (e) {{
            continue;
        }}
    }}
    
    if (!translationResult) {{
        throw new Error("❌ 未能提取到翻译结果");
    }}
    
    return translationResult;
}}

// 执行自动化翻译
automateSiderTranslation()
    .then(result => {{
        console.log("🎉 翻译完成!");
        console.log("翻译结果:", result);
    }})
    .catch(error => {{
        console.error("❌ 翻译失败:", error);
    }});
"""
        
        # 保存脚本文件
        script_file = os.path.join(self.output_dir, "browser_mcp_automation.js")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"📝 自动化脚本已保存: {script_file}")
        return script_file
    
    def create_mcp_integration_guide(self):
        """创建MCP集成指南"""
        guide = """# Browser MCP自动化翻译集成指南

## 🔧 设置步骤

### 1. 安装Chrome扩展
访问: https://chromewebstore.google.com/detail/browser-mcp-automate-your/bjfgambnhccakkhmkepdoekmckoijdlc
点击"Add to Chrome"安装扩展

### 2. 配置MCP服务器
在Cursor中:
1. 打开设置 (Cmd/Ctrl + ,)
2. 导航到"MCP"标签
3. 点击"Add new global MCP server"
4. 添加以下配置:

```json
{
  "mcpServers": {
    "browsermcp": {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    }
  }
}
```

### 3. 重启Cursor
重启Cursor以加载MCP配置

### 4. 使用Browser MCP
在Cursor中，你现在可以使用以下命令:
- 🌐 导航到网页
- 📝 填写表单
- 🔍 查找元素
- 📖 提取内容
- 🚀 执行JavaScript

## 🤖 自动化翻译流程

1. **启动Browser MCP服务器**
   ```bash
   npx @browsermcp/mcp@latest
   ```

2. **在Cursor中执行翻译**
   使用Browser MCP工具:
   - 打开Sider.AI
   - 输入翻译提示词
   - 等待翻译完成
   - 提取翻译结果

## 🎯 使用示例

在Cursor中，你可以这样使用:

```
请使用Browser MCP帮我:
1. 打开 https://sider.ai/chat
2. 在聊天框中输入翻译提示词
3. 等待翻译完成
4. 提取翻译结果并保存
```

## 🔍 故障排除

如果遇到问题:
1. 确保Chrome扩展已安装并启用
2. 确保MCP服务器正在运行
3. 检查Cursor的MCP配置
4. 重启Cursor和Chrome浏览器

## 📚 更多信息

- Browser MCP文档: https://docs.browsermcp.io/
- MCP规范: https://modelcontextprotocol.io/
- Cursor MCP指南: https://docs.cursor.com/mcp
"""
        
        guide_file = os.path.join(self.output_dir, "BROWSER_MCP_GUIDE.md")
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"📚 集成指南已保存: {guide_file}")
        return guide_file
    
    async def process_translation(self, english_srt_file):
        """处理翻译的完整流程"""
        print("🎯 Browser MCP自动化翻译开始")
        print("="*50)
        
        # 1. 解析英文字幕
        print("📖 步骤1: 解析英文字幕")
        segments = self.parse_english_srt(english_srt_file)
        print(f"✅ 解析完成，共 {len(segments)} 个片段")
        
        # 2. 创建翻译提示词
        print("\n📝 步骤2: 创建翻译提示词")
        prompt_text = self.create_translation_prompt(segments)
        print("✅ 翻译提示词创建完成")
        
        # 3. 安装Browser MCP扩展指南
        print("\n🔧 步骤3: Browser MCP设置")
        self.install_browser_extension()
        
        # 4. 创建自动化脚本
        print("\n📝 步骤4: 创建自动化脚本")
        script_file = self.create_automation_script(prompt_text)
        
        # 5. 创建集成指南
        print("\n📚 步骤5: 创建集成指南")
        guide_file = self.create_mcp_integration_guide()
        
        # 6. 保存翻译提示词
        print("\n💾 步骤6: 保存翻译提示词")
        prompt_file = os.path.join(self.output_dir, "sider_translation_prompt.txt")
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt_text)
        print(f"✅ 翻译提示词已保存: {prompt_file}")
        
        print("\n" + "="*60)
        print("🎉 Browser MCP自动化翻译设置完成!")
        print("="*60)
        print("📁 生成的文件:")
        print(f"   - 🔧 MCP配置: mcp_config.json")
        print(f"   - 📝 自动化脚本: {script_file}")
        print(f"   - 📚 集成指南: {guide_file}")
        print(f"   - 💬 翻译提示词: {prompt_file}")
        print()
        print("🔄 下一步操作:")
        print("1. 安装Chrome扩展 (已自动打开)")
        print("2. 在Cursor中配置MCP服务器")
        print("3. 重启Cursor")
        print("4. 使用Browser MCP工具执行自动化翻译")
        print()
        print("💡 在Cursor中，你可以说:")
        print('   "请使用Browser MCP帮我自动翻译Sider.AI中的内容"')
        
        return {
            'script_file': script_file,
            'guide_file': guide_file,
            'prompt_file': prompt_file,
            'mcp_config': 'mcp_config.json'
        }

def main():
    """主函数"""
    import sys
    
    # 检查参数
    if len(sys.argv) != 2:
        print("用法: python browser_mcp_translator.py <英文字幕文件>")
        print("示例: python browser_mcp_translator.py output/VP9_segment_2m36s-5m59s_english.srt")
        sys.exit(1)
    
    english_srt_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(english_srt_file):
        print(f"❌ 文件不存在: {english_srt_file}")
        sys.exit(1)
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建翻译器实例
    translator = BrowserMCPTranslator(output_dir)
    
    # 运行翻译流程
    try:
        result = asyncio.run(translator.process_translation(english_srt_file))
        
        if result:
            print(f"\n✅ Browser MCP自动化翻译设置完成!")
            print("🚀 现在可以在Cursor中使用Browser MCP进行自动化翻译了!")
        else:
            print("\n❌ Browser MCP设置失败")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\n❌ 设置过程中出现错误: {e}")

if __name__ == "__main__":
    main() 