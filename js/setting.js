// 使用立即执行函数（IIFE）来避免污染全局作用域
(function() {
    // 确保在 DOM 加载完成后再执行脚本
    document.addEventListener('DOMContentLoaded', function() {
    
        // =================================================================
        // 1. 定义所有需要的 CSS 样式
        //    您可以在这里修改颜色和样式
        // =================================================================
        const cssStyles = `
            /* --- 颜色和基本设置 (在这里自定义) --- */
            :root {
                --fab-main-bg: #5a67d8;          /* 主按钮背景色 */
                --fab-main-icon-color: #ffffff; /* 主按钮图标颜色 */
                --fab-option-bg: #7f8de1;        /* 选项按钮背景色 */
                --fab-option-icon-color: #ffffff;/* 选项按钮图标颜色 */
                --fab-shadow: rgba(0, 0, 0, 0.25); /* 按钮阴影 */
            }

            /* --- 悬浮按钮容器 --- */
            .fab-container-generated {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
                display: flex;
                flex-direction: column-reverse;
                align-items: center;
            }

            /* --- 主按钮 --- */
            .fab-main-button-generated {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: var(--fab-main-bg);
                border: none;
                cursor: pointer;
                box-shadow: 0 4px 8px var(--fab-shadow);
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                position: relative;
                z-index: 2;
            }

            .fab-main-button-generated:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 12px var(--fab-shadow);
            }

            #fab-icon-generated {
                transition: transform 0.3s ease;
                color: var(--fab-main-icon-color);
            }

            #fab-icon-generated.rotate {
                transform: rotate(45deg);
            }

            /* --- 选项按钮容器 --- */
            .fab-options-generated {
                display: flex;
                flex-direction: column;
                align-items: center;
                list-style: none;
                padding: 0;
                margin: 0 0 15px 0;
                visibility: hidden;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s ease;
            }

            .fab-options-generated.active {
                visibility: visible;
                opacity: 1;
                transform: translateY(0);
            }

            /* --- 单个选项按钮 --- */
            .fab-option-item-generated {
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background-color: var(--fab-option-bg);
                border: none;
                cursor: pointer;
                box-shadow: 0 2px 5px var(--fab-shadow);
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 10px;
                transition: all 0.2s ease-in-out;
                color: var(--fab-option-icon-color);
            }
            
            .fab-option-item-generated:hover {
                background-color: var(--fab-main-bg);
                transform: scale(1.1);
            }
            
            .fab-option-item-generated:last-child {
                margin-bottom: 0;
            }
        `;

        // =================================================================
        // 2. 动态创建并注入 <style> 标签到 <head>
        // =================================================================
        const styleElement = document.createElement('style');
        styleElement.textContent = cssStyles;
        document.head.appendChild(styleElement);

        // =================================================================
        // 3. 动态创建 HTML 结构并插入到 <body>
        // =================================================================
        const fabContainer = document.createElement('div');
        fabContainer.className = 'fab-container-generated';

        // 这里定义了按钮的 HTML 结构，您可以在这里增删按钮或修改图标
        fabContainer.innerHTML = `
            <div class="fab-options-generated">
                <button class="fab-option-item-generated" onclick="alert('点击了设置')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 0 2.82l-.15.08a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.38a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1 0-2.82l.15-.08a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                </button>
                <button class="fab-option-item-generated" onclick="alert('点击了帮助')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                </button>
                <button class="fab-option-item-generated" onclick="alert('返回顶部'); window.scrollTo({top: 0, behavior: 'smooth'});">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
                </button>
            </div>
            <button class="fab-main-button-generated" id="fab-main-button-generated">
                <svg id="fab-icon-generated" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19.14 12.94c.04-.3.06-.61.06-.94s-.02-.64-.07-.94l2.03-1.58a.5.5 0 0 0 .12-.63l-1.34-2.32a.5.5 0 0 0-.63-.19l-2.4 1.03a8.2 8.2 0 0 0-1.66-.94L14.4 3.5a.5.5 0 0 0-.5-.5h-2.8a.5.5 0 0 0-.5.5l-.34 2.84a8.2 8.2 0 0 0-1.66.94l-2.4-1.03a.5.5 0 0 0-.63.19L2.8 5.79a.5.5 0 0 0 .12.63l2.03 1.58c-.05.3-.07.64-.07.94s.02.64.07.94l-2.03 1.58a.5.5 0 0 0-.12.63l1.34 2.32a.5.5 0 0 0 .63.19l2.4-1.03a8.2 8.2 0 0 0 1.66.94l.34 2.84a.5.5 0 0 0 .5.5h2.8a.5.5 0 0 0 .5-.5l.34-2.84a8.2 8.2 0 0 0 1.66-.94l2.4 1.03a.5.5 0 0 0 .63-.19l1.34-2.32a.5.5 0 0 0-.12-.63l-2.03-1.58z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                </svg>
            </button>
        `;
        document.body.appendChild(fabContainer);

        // =================================================================
        // 4. 获取刚刚创建的元素并添加事件监听器
        // =================================================================
        const mainFabButton = document.getElementById('fab-main-button-generated');
        const fabOptions = document.querySelector('.fab-options-generated');
        const fabIcon = document.getElementById('fab-icon-generated');

        mainFabButton.addEventListener('click', () => {
            fabOptions.classList.toggle('active');
            fabIcon.classList.toggle('rotate');
        });

        window.addEventListener('click', (e) => {
            if (!e.target.closest('.fab-container-generated')) {
                if (fabOptions.classList.contains('active')) {
                    fabOptions.classList.remove('active');
                    fabIcon.classList.remove('rotate');
                }
            }
        });
    });
})();