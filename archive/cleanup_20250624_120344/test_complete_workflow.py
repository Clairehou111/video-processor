#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整流程测试脚本
使用Ted Cruz视频验证端到端自动化
"""

import subprocess
import sys
import os

def main():
    """测试完整流程"""
    print("🧪 完整B站视频处理流程测试")
    print("="*60)
    
    # 使用之前成功的Ted Cruz视频
    test_url = "https://www.youtube.com/watch?v=YIlL0T2yTss"
    
    print(f"🎯 测试视频: {test_url}")
    print("📝 这是Ted Cruz vs Tucker Carlson关于伊朗的争论视频")
    print("⏱️ 预计处理时间: 10-15分钟")
    print("\n是否继续测试？(y/n): ", end="")
    
    response = input().strip().lower()
    if response != 'y':
        print("❌ 测试取消")
        return
    
    print("\n🚀 开始完整流程测试...")
    
    # 执行完整流程
    cmd = [sys.executable, "complete_bilibili_workflow.py", test_url]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ 完整流程测试成功！")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 测试失败: {e}")
        return
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断测试")
        return

if __name__ == "__main__":
    main() 