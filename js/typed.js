// 打字机效果

// 动态加载 CDN 脚本
const script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/typed.js@2.0.11';
script.onload = () => {
  // 在脚本加载完成后初始化 Typed.js
  const options = {
    strings: ['欢迎来到 NoughtQ 的笔记本~'],
    typeSpeed: 50,
    startDelay: 300,
    loop: false,
  };

  const typed = new Typed('#typed', options);
};
script.onerror = (err) => {
  console.error('Error loading Typed.js:', err);
};

// 将 <script> 标签添加到 DOM 中
document.head.appendChild(script);