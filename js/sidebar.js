// ==UserScript==
// @name         Auto Hide Sidebars Toggle
// @namespace    custom
// @version      1.0
// @description  在右下角添加按钮，可单独控制主/次边栏的自动隐藏
// @match        *://*/*
// @run-at       document-end
// ==/UserScript==

(function () {
  const STYLE_ID = 'auto-hide-sidebar-style';
  const TOGGLE_BTN_ID = 'autoHideSidebarToggleBtn';
  const PANEL_ID = 'autoHideSidebarPanel';

  const PRIMARY_CLASS = 'auto-hide-primary-sidebar';
  const SECONDARY_CLASS = 'auto-hide-secondary-sidebar';

  // 注入 CSS：包含边栏自动隐藏效果 + 控制面板的样式
  function injectCss() {
    if (document.getElementById(STYLE_ID)) return;

    const css = `
/* === 自动隐藏边栏（基于你提供的 CSS，增加 body 类名控制） === */

/* 主边栏（左边） */
body.${PRIMARY_CLASS} .md-sidebar.md-sidebar--primary .md-sidebar__inner {
  opacity: 0;
  transform: translateX(-100%);
  transition: opacity 0.3s ease-out, transform 0.3s ease-out;
  pointer-events: none;
}

body.${PRIMARY_CLASS} .md-sidebar.md-sidebar--primary .md-sidebar__scrollwrap:hover .md-sidebar__inner {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
}

/* 次边栏（右边） */
body.${SECONDARY_CLASS} .md-sidebar.md-sidebar--secondary .md-sidebar__inner {
  opacity: 0;
  transform: translateX(100%);
  transition: opacity 0.3s ease-out, transform 0.3s ease-out;
  pointer-events: none;
}

body.${SECONDARY_CLASS} .md-sidebar.md-sidebar--secondary .md-sidebar__scrollwrap:hover .md-sidebar__inner {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
}

/* === 右下角按钮与控制面板样式 === */

#${TOGGLE_BTN_ID} {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: 99999;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.15);
  background: rgba(255,255,255,0.95);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  line-height: 1;
  padding: 0;
  user-select: none;
  backdrop-filter: blur(8px);
}

#${TOGGLE_BTN_ID}:hover {
  box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

#${PANEL_ID} {
  position: fixed;
  bottom: 64px;
  right: 16px;
  z-index: 99999;
  min-width: 220px;
  max-width: 260px;
  background: rgba(255,255,255,0.98);
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.12);
  box-shadow: 0 10px 25px rgba(0,0,0,0.18);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 13px;
  color: #222;
  overflow: hidden;
}

#${PANEL_ID}.hidden {
  display: none;
}

#${PANEL_ID} .ahs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  background: linear-gradient(to top, #f8f9fa, #ffffff);
}

#${PANEL_ID} .ahs-title {
  font-size: 13px;
  font-weight: 600;
}

#${PANEL_ID} .ahs-close {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0 4px;
}

#${PANEL_ID} .ahs-body {
  padding: 8px 10px 10px;
}

#${PANEL_ID} .ahs-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 6px 0;
}

#${PANEL_ID} label {
  cursor: pointer;
  flex: 1;
}

#${PANEL_ID} input[type="checkbox"] {
  cursor: pointer;
}

#${PANEL_ID} .ahs-desc {
  margin-top: 6px;
  font-size: 11px;
  color: #666;
}
    `;

    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = css;
    document.head.appendChild(style);
  }

  // 创建右下角按钮 & 控制面板
  function createUI() {
    if (document.getElementById(TOGGLE_BTN_ID) || document.getElementById(PANEL_ID)) return;

    // 浮动按钮
    const btn = document.createElement('button');
    btn.id = TOGGLE_BTN_ID;
    btn.title = '边栏自动隐藏设置';
    btn.textContent = '≡'; // 简单图标，可自行修改
    document.body.appendChild(btn);

    // 设置面板
    const panel = document.createElement('div');
    panel.id = PANEL_ID;
    panel.classList.add('hidden');

    panel.innerHTML = `
      <div class="ahs-header">
        <div class="ahs-title">边栏自动隐藏</div>
        <button class="ahs-close" title="关闭">×</button>
      </div>
      <div class="ahs-body">
        <div class="ahs-row">
          <input type="checkbox" id="ahsPrimary">
          <label for="ahsPrimary">自动隐藏主边栏（左侧）</label>
        </div>
        <div class="ahs-row">
          <input type="checkbox" id="ahsSecondary">
          <label for="ahsSecondary">自动隐藏次边栏（右侧）</label>
        </div>
        <div class="ahs-desc">
          鼠标移到边栏区域时会自动滑出，移开后收起。
        </div>
      </div>
    `;

    document.body.appendChild(panel);

    const closeBtn = panel.querySelector('.ahs-close');
    const primaryCheckbox = panel.querySelector('#ahsPrimary');
    const secondaryCheckbox = panel.querySelector('#ahsSecondary');

    // 初始化勾选状态（如果 body 已经有类）
    primaryCheckbox.checked = document.body.classList.contains(PRIMARY_CLASS);
    secondaryCheckbox.checked = document.body.classList.contains(SECONDARY_CLASS);

    // 按钮：显示 / 隐藏设置面板
    btn.addEventListener('click', () => {
      panel.classList.toggle('hidden');
    });

    // 关闭按钮
    closeBtn.addEventListener('click', () => {
      panel.classList.add('hidden');
    });

    // 点击面板本身不要触发其他奇怪事件
    panel.addEventListener('click', (e) => {
      e.stopPropagation();
    });

    // 勾选：控制主边栏自动隐藏
    primaryCheckbox.addEventListener('change', () => {
      if (primaryCheckbox.checked) {
        document.body.classList.add(PRIMARY_CLASS);
      } else {
        document.body.classList.remove(PRIMARY_CLASS);
      }
    });

    // 勾选：控制次边栏自动隐藏
    secondaryCheckbox.addEventListener('change', () => {
      if (secondaryCheckbox.checked) {
        document.body.classList.add(SECONDARY_CLASS);
      } else {
        document.body.classList.remove(SECONDARY_CLASS);
      }
    });
  }

  function init() {
    injectCss();
    createUI();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
