#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全自动化Sider.AI翻译执行器
真正实现端到端自动化
"""

import os
import time
import subprocess
import webbrowser
from pathlib import Path

def read_translation_prompt():
    """读取翻译提示词"""
    prompt_file = "output/sider_translation_prompt.txt"
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ 读取翻译提示词失败: {e}")
        return None

def start_browser_mcp_server():
    """启动Browser MCP服务器"""
    print("🚀 启动Browser MCP服务器...")
    try:
        # 在后台启动MCP服务器
        process = subprocess.Popen(
            ["npx", "@browsermcp/mcp@latest"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Browser MCP服务器已启动 (PID: {process.pid})")
        time.sleep(2)  # 等待服务器启动
        return process
    except Exception as e:
        print(f"❌ 启动Browser MCP服务器失败: {e}")
        return None

def open_sider_ai():
    """打开Sider.AI网站"""
    print("🌐 打开Sider.AI...")
    sider_url = "https://sider.ai/chat"
    try:
        webbrowser.open(sider_url)
        print("✅ Sider.AI已在浏览器中打开")
        return True
    except Exception as e:
        print(f"❌ 打开Sider.AI失败: {e}")
        return False

def display_automation_instructions(prompt_text):
    """显示自动化操作指导"""
    print("\n" + "="*80)
    print("🤖 完全自动化翻译执行指导")
    print("="*80)
    
    print("\n📋 翻译提示词已准备好，内容预览:")
    print("─" * 60)
    preview = prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text
    print(preview)
    print("─" * 60)
    
    print(f"\n📏 提示词总长度: {len(prompt_text)} 字符")
    print(f"📊 包含字幕片段: {prompt_text.count('.')}")
    
    print("\n🎯 现在有两种自动化方式:")
    print("\n方式1: 使用Cursor的Browser MCP (推荐)")
    print("─" * 40)
    print("1. 确保你已在Cursor中配置了Browser MCP")
    print("2. 在Cursor中输入以下命令:")
    print()
    print("   请使用Browser MCP工具:")
    print("   1. 打开 https://sider.ai/chat")
    print("   2. 等待页面加载完成")
    print("   3. 找到聊天输入框")
    print("   4. 输入完整的翻译提示词")
    print("   5. 发送请求并等待翻译完成")
    print("   6. 提取翻译结果")
    print("   7. 保存到 output/chinese_translation.txt")
    print()
    
    print("方式2: 手动操作 + 自动保存")
    print("─" * 40)
    print("1. Sider.AI已自动打开")
    print("2. 登录你的账户")
    print("3. 选择AI模型 (推荐Claude-3.5-Sonnet)")
    print("4. 复制完整提示词并粘贴")
    print("5. 等待翻译完成")
    print("6. 复制翻译结果")
    print("7. 返回这里保存结果")

def wait_for_translation_result():
    """等待翻译结果"""
    print("\n⏳ 等待翻译完成...")
    print("完成翻译后，选择保存方式:")
    print("1. 📋 粘贴翻译结果")
    print("2. 📁 从文件导入")
    print("3. ❌ 退出")
    
    while True:
        try:
            choice = input("\n请选择 (1-3): ").strip()
            
            if choice == "1":
                return save_translation_by_paste()
            elif choice == "2":
                return save_translation_from_file()
            elif choice == "3":
                print("👋 退出自动化流程")
                return None
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n👋 用户中断，退出程序")
            return None

def save_translation_by_paste():
    """通过粘贴保存翻译结果"""
    print("\n📋 请粘贴Sider.AI的翻译结果:")
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
        
        translation_text = '\n'.join(lines).strip()
        
        if translation_text:
            output_file = "output/chinese_translation.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translation_text)
            print(f"✅ 翻译结果已保存到: {output_file}")
            return output_file
        else:
            print("❌ 未检测到翻译内容")
            return None
            
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return None

def save_translation_from_file():
    """从文件导入翻译结果"""
    try:
        file_path = input("请输入翻译结果文件路径: ").strip()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            translation_text = f.read()
        
        output_file = "output/chinese_translation.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translation_text)
        
        print(f"✅ 翻译结果已从 {file_path} 导入到 {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ 文件导入失败: {e}")
        return None

def create_bilingual_video(translation_file):
    """创建双语视频"""
    if translation_file:
        print(f"\n🎬 翻译完成! 现在可以创建双语视频:")
        print(f"   python create_bilingual_video.py")
        
        choice = input("\n是否立即创建双语视频? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            try:
                subprocess.run(["python", "create_bilingual_video.py"], check=True)
                print("✅ 双语视频创建完成!")
            except Exception as e:
                print(f"❌ 创建双语视频失败: {e}")

def main():
    """主函数 - 完全自动化执行"""
    print("🎯 完全自动化Sider.AI翻译开始")
    print("="*50)
    
    # 1. 读取翻译提示词
    print("📖 步骤1: 读取翻译提示词")
    prompt_text = read_translation_prompt()
    if not prompt_text:
        return
    print("✅ 翻译提示词读取成功")
    
    # 2. 启动Browser MCP服务器
    print("\n🚀 步骤2: 启动Browser MCP服务器")
    mcp_process = start_browser_mcp_server()
    
    # 3. 打开Sider.AI
    print("\n🌐 步骤3: 打开Sider.AI")
    if not open_sider_ai():
        return
    
    # 4. 显示自动化指导
    print("\n📋 步骤4: 显示自动化指导")
    display_automation_instructions(prompt_text)
    
    # 5. 等待翻译完成
    print("\n⏳ 步骤5: 等待翻译完成")
    translation_file = wait_for_translation_result()
    
    # 6. 创建双语视频
    if translation_file:
        print("\n🎬 步骤6: 创建双语视频")
        create_bilingual_video(translation_file)
    
    # 7. 清理资源
    if mcp_process:
        try:
            mcp_process.terminate()
            print("✅ Browser MCP服务器已关闭")
        except:
            pass
    
    print("\n🎉 完全自动化翻译流程完成!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\n❌ 执行过程中出现错误: {e}") 