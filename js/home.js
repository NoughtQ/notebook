// 移除主页中编辑和查看两个按钮
const edit = document.querySelectorAll('[title="编辑此页"]');
const view = document.querySelectorAll('[title="查看本页的源代码"]');

edit.forEach(element => {
    element.remove();
});

view.forEach(element => {
    element.remove();
});

// 时间记录
function updateTime() {
    var date = new Date();
    var now = date.getTime();
    var startDate = new Date("2024/05/25 19:58:19");
    var start = startDate.getTime();
    var diff = now - start;
    var y, d, h, m;
    y = Math.floor(diff / (365 * 24 * 3600 * 1000));
    diff -= y * 365 * 24 * 3600 * 1000;
    d = Math.floor(diff / (24 * 3600 * 1000));
    h = Math.floor(diff / (3600 * 1000) % 24);
    m = Math.floor(diff / (60 * 1000) % 60);
    if (y == 0) {
        document.getElementById("web-time").innerHTML = d + "<span class=\"heti-spacing\"> </span>天<span class=\"heti-spacing\"> </span>" + h + "<span class=\"heti-spacing\"> </span>小时<span class=\"heti-spacing\"> </span>" + m + "<span class=\"heti-spacing\"> </span>分钟";
    } else {
        document.getElementById("web-time").innerHTML = y + "<span class=\"heti-spacing\"> </span>年<span class=\"heti-spacing\"> </span>" + d + "<span class=\"heti-spacing\"> </span>天<span class=\"heti-spacing\"> </span>" + h + "<span class=\"heti-spacing\"> </span>小时<span class=\"heti-spacing\"> </span>" + m + "<span class=\"heti-spacing\"> </span>分钟";
    }
    setTimeout(updateTime, 1000 * 60);
}

updateTime();

// 统计栏
function toggle_statistics() {
    var statistics = document.getElementById("statistics");
    var about = document.getElementById("about");
    var recommend = document.getElementById("recommend");

    // 隐藏 "about" 区块（如果它是可见的）
    if (about.style.display === "block") {
        about.style.display = "none";
    }

    // 隐藏 "recommend" 区块（如果它是可见的）
    if (recommend.style.display === "block") {
        recommend.style.display = "none";
    }

    // 切换 "statistics" 区块的显示状态
    if (statistics.style.display === "none" || statistics.style.display === "") {
        statistics.style.display = "block";
    } else {
        statistics.style.display = "none";
    }
}

// 关于栏
function toggle_about() {
    var about = document.getElementById("about");
    var statistics = document.getElementById("statistics");
    var recommend = document.getElementById("recommend");

    // 隐藏 "statistics" 区块（如果它是可见的）
    if (statistics.style.display === "block") {
        statistics.style.display = "none";
    }

    // 隐藏 "recommend" 区块（如果它是可见的）
    if (recommend.style.display === "block") {
        recommend.style.display = "none";
    }

    // 切换 "about" 区块的显示状态
    if (about.style.display === "none" || about.style.display === "") {
        about.style.display = "block";
    } else {
        about.style.display = "none";
    }
}

// 推荐栏
function toggle_recommend() {
    var about = document.getElementById("about");
    var statistics = document.getElementById("statistics");
    var recommend = document.getElementById("recommend");

    // 隐藏 "about" 区块（如果它是可见的）
    if (about.style.display === "block") {
        about.style.display = "none";
    }

    // 隐藏 "statistics" 区块（如果它是可见的）
    if (statistics.style.display === "block") {
        statistics.style.display = "none";
    }

    // 切换 "recommend" 区块的显示状态
    if (recommend.style.display === "none" || recommend.style.display === "") {
        recommend.style.display = "block";
    } else {
        recommend.style.display = "none";
    }
}

// 笔记漫游（前端部分）
document.addEventListener("DOMContentLoaded", function () {
  setRandomLink();
});

window.addEventListener("pageshow", function (event) {
  if (event.persisted) {
    setRandomLink();
  }
});

document.addEventListener("visibilitychange", function() {
    if (document.visibilityState === "visible") {
      setRandomLink();
    }
});

function setRandomLink() {
    if (window.allNotePaths && window.allNotePaths.length) {
      // 获取随机链接
      let randomLink = window.allNotePaths[Math.floor(Math.random() * window.allNotePaths.length)];
  
      // 去掉后缀名
      let linkWithoutExtension = randomLink.split('.').slice(0, -1).join('.');
  
      // 检测当前网页的 URL 是否为本地地址
      const isLocal = window.location.href.includes("127.0.0.1") || window.location.href.includes("localhost");
  
      // 根据是否为本地地址修改链接
      if (isLocal) {
        linkWithoutExtension += ".html"; // 本地地址添加 .html
      }
  
      console.log("处理后的随机笔记链接: " + linkWithoutExtension);
      document.getElementById("randomLink").href = linkWithoutExtension;
    }
}
