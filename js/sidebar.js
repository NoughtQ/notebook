document.addEventListener('DOMContentLoaded', () => {
    // 获取 DOM 元素
    const selfHidingArea = document.querySelectorAll('.md-sidebar.md-sidebar--secondary');

    // 当鼠标进入该区域时
    selfHidingArea.addEventListener('mouseenter', () => {
        selfHidingArea.classList.add('show');
    });

    // 当鼠标离开该区域时
    selfHidingArea.addEventListener('mouseleave', () => {
        selfHidingArea.classList.remove('show');
    });

    // 获取 DOM 元素
    const selfHidingArea2 = document.querySelectorAll('.md-sidebar.md-sidebar--secondary .md-sidebar__scrollwrap');

    // 当鼠标进入该区域时
    selfHidingArea2.addEventListener('mouseenter', () => {
        selfHidingArea2.classList.add('show');
    });

    // 当鼠标离开该区域时
    selfHidingArea2.addEventListener('mouseleave', () => {
        selfHidingArea2.classList.remove('show');
    });
});