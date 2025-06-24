
// Sider.AI文件上传自动化脚本
console.log("📁 开始文件上传自动化...");

async function uploadFileToSider() {
    try {
        console.log("🔍 查找文件上传方式...");
        
        // 方式1: 查找隐藏的文件输入框
        console.log("📂 方式1: 查找文件输入框...");
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        if (fileInputs.length > 0) {
            console.log(`✅ 找到 ${fileInputs.length} 个文件输入框`);
            
            // 创建文件对象 (这需要实际的文件内容)
            console.log("⚠️ 需要手动选择文件: output/subtitles_for_translation.txt");
            
            // 触发文件选择对话框
            fileInputs[0].click();
            console.log("✅ 已触发文件选择对话框");
            return true;
        }
        
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
        for (const selector of attachmentSelectors) {
            const elements = document.querySelectorAll(selector);
            for (const element of elements) {
                if (element.offsetParent !== null) {
                    attachButton = element;
                    console.log(`✅ 找到附件按钮: ${selector}`);
                    break;
                }
            }
            if (attachButton) break;
        }
        
        if (attachButton) {
            console.log("🔄 点击附件按钮...");
            attachButton.click();
            
            // 等待文件选择对话框出现
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 再次查找文件输入框
            const newFileInputs = document.querySelectorAll('input[type="file"]');
            if (newFileInputs.length > 0) {
                console.log("✅ 附件按钮触发了文件输入框");
                return true;
            }
        }
        
        // 方式3: 查找可能触发上传的图标
        console.log("🔍 方式3: 查找上传相关图标...");
        const allClickableElements = document.querySelectorAll('button, [role="button"], svg, i');
        
        for (const element of allClickableElements) {
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
            
            if (hasUploadKeyword && element.offsetParent !== null) {
                console.log(`🎯 尝试点击可能的上传元素: ${element.tagName} - ${className}`);
                try {
                    element.click();
                    await new Promise(resolve => setTimeout(resolve, 500));
                    
                    // 检查是否出现了文件输入框
                    const triggeredInputs = document.querySelectorAll('input[type="file"]');
                    if (triggeredInputs.length > 0) {
                        console.log("✅ 成功触发文件输入框");
                        return true;
                    }
                } catch (e) {
                    console.log("⚠️ 点击元素失败:", e);
                }
            }
        }
        
        // 方式4: 拖拽上传提示
        console.log("🎯 方式4: 准备拖拽上传...");
        const chatInput = document.querySelector('textarea, div[contenteditable="true"], input[type="text"]');
        
        if (chatInput) {
            console.log("💡 拖拽上传提示:");
            console.log("1. 打开文件管理器，找到文件: output/subtitles_for_translation.txt");
            console.log("2. 将文件拖拽到聊天输入框区域");
            console.log("3. 松开鼠标完成上传");
            
            // 高亮聊天输入区域
            chatInput.style.border = "3px dashed #007bff";
            chatInput.style.backgroundColor = "#f8f9fa";
            
            setTimeout(() => {
                chatInput.style.border = "";
                chatInput.style.backgroundColor = "";
            }, 5000);
            
            return true;
        }
        
        console.log("❌ 未找到文件上传方式");
        return false;
        
    } catch (error) {
        console.error("❌ 文件上传自动化失败:", error);
        return false;
    }
}

// 执行文件上传
uploadFileToSider().then(success => {
    if (success) {
        console.log("🎉 文件上传准备完成!");
        console.log("💡 如果出现文件选择对话框，请选择: output/subtitles_for_translation.txt");
    } else {
        console.log("❌ 文件上传准备失败");
        console.log("💡 请尝试手动拖拽文件到聊天区域");
    }
});
