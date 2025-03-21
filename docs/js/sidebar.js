// 改进后的JavaScript实现
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.md-sidebar.md-sidebar--secondary');
    const scrollwrap = document.querySelector('.md-sidebar.md-sidebar--secondary .md-sidebar__scrollwrap');

    // 动态计算宽度
    function updateWidth() {
        const width = scrollwrap.offsetWidth;
        scrollwrap.style.transform = `translateX(${width}px)`;
    }

    // 初始化
    updateWidth();
    window.addEventListener('resize', updateWidth);

    // 鼠标事件处理
    sidebar.addEventListener('mouseenter', function() {
        scrollwrap.style.transform = 'translateX(0)';
    });

    sidebar.addEventListener('mouseleave', function() {
        updateWidth();
    });

    // 保留原有子目录功能
    const navItems = document.querySelectorAll('.md-sidebar.md-sidebar--secondary .md-nav__item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // 阻止事件冒泡，保留原有功能
            e.stopPropagation();
        });
    });
});