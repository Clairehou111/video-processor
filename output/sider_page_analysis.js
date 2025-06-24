
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
