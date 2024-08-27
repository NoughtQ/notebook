// 跨源访问网页会打开新的标签页
// Written by ChatGPT
document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', event => {
      const href = link.getAttribute('href');
      if (!href) return; // 忽略没有 href 属性的链接
  
      try {
        const linkUrl = new URL(href, window.location.href);
        const baseUrl = new URL(window.location.href);
        const cleanLinkUrl = new URL(linkUrl.origin + linkUrl.pathname + linkUrl.search, baseUrl.origin);
  
        if (cleanLinkUrl.origin === baseUrl.origin) {
          link.target = '_self';
        } else {
          link.target = '_blank';
        }
      } catch (error) {
        link.target = '_blank';
      }
  
      // 阻止默认行为，防止空白页面的出现
      event.preventDefault();
  
      // 如果不是同源，则手动打开新标签页
      if (link.target === '_blank') {
        window.open(href, '_blank');
      } else {
        window.location.href = href;
      }
    });
  });
  