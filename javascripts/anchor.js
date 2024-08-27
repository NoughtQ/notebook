// 点击链接打开新的标签页

document.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', event => {
      const href = link.getAttribute('href');
      const isSameOrigin = new URL(href, window.location.origin).origin === window.location.origin;

      if (isSameOrigin) {
          link.target = '_self';
      } else {
          link.target = '_blank';
      }
  });
});