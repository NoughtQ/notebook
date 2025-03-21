document.addEventListener('DOMContentLoaded', function () {
    function processLinks() {
        const links = document.querySelectorAll('a');
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return; // 忽略没有 href 属性的链接
  
            // 忽略仅包含空格或不可见字符的链接
            if (href.trim().length === 0) return;
  
            try {
                const linkUrl = new URL(href, window.location.href);
                const baseUrl = new URL(window.location.href);
                const cleanLinkUrl = new URL(linkUrl.origin + linkUrl.pathname + linkUrl.search, baseUrl.origin);
  
                if (cleanLinkUrl.origin === baseUrl.origin) {
                    // 同源链接
                    link.target = '_self';
                    link.style.textDecoration = 'none'; // 确保没有下划线
                } else {
                    // 跨源链接
                    link.target = '_blank';
                    link.classList.add('cross-origin'); // 添加 cross-origin 类以设置下划线
                }
            } catch (error) {
                // 如果 URL 解析失败，处理为跨源
                link.target = '_blank';
                link.classList.add('cross-origin'); // 添加 cross-origin 类以设置下划线
            }
        });
    }
  
    processLinks();
  });
  
  