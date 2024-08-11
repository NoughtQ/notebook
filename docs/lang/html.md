---
counter: true
---

# HTML

!!! abstract "参考资料"

    - [MDN HTML 学习](https://developer.mozilla.org/zh-CN/docs/Learn/HTML)
    - [MDN HTML 参考](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference)

!!! info "有用的工具"

    - 开发者工具
    - [HTML 语法验证小工具](https://validator.w3.org/)

## 基础知识

这是一个 HTML 元素：

<div style="text-align: center">
    <image src="images/html/1.png" width=50%>
</div>

通常由以下三部分构成：

- 开始标签：声明元素，以及标志该元素开始生效的地方
- 内容
- 结束标签：与开始标签类似，注意元素名前有一个斜杠 `/`

由于是“通常”，所以也会有意外，一些元素只由一个标签组成，这样的元素称为**空元素**，比如标签 `<img>`。

标签内除了元素名外，还可以指定元素的**属性**（attribute），用来改变元素的表现形式等。属性的格式：`<elem atr1="val1" atr2="val2">content</elem>`，注意空格、等号和引号。

??? info "注"

    - 如果只有一个属性，可以省略引号，但<u>强烈建议加上引号</u>
    - 既可以用单引号，也可以用双引号，但不要混搭！
    - HTML 元素的内容中，多个空白字符（空格、换行等）都被视为一个空格

有些属性没有值，或者它只有一个与属性名称相同的值，这种属性被称为**布尔属性**。这两种形式共存，方便起见就写没有值的属性。

HTML 元素可**嵌套**，但要注意标签的位置。

元素类型：

- 块级元素：在网页中以“块”的形式呈现，后面的元素出现在新的一行上，标题、段落、列表等属于此类。块级元素不能嵌套在内联元素内。
- 内联元素：只修饰“块”内某个指定部分的内容，比如一小部分的文本等。

???+ note "HTML 特殊字符的引用"

    下列字符不能被直接被文本包含，我们需要用一种特殊编码来表示它们：

    |字符|等价字符引用|
    |:-|:-|
    |`<`|`&lt;`|
    |`>`|`&gt;`|
    |`"`|`&quot;`|
    |`'`|`&apos;`|
    |`&`|`&amp;`|

注释：`<!-- comments -->`

??? example "一个简单、完整的 HTML 文本"

    ``` html
    <!doctype html>
    <html lang="en-US">
        <head>
            <meta charset="utf-8" />
            <title>Hello, HTML!</title>
        </head>
        <body>
            <p>My first HTML travel!</p>
        </body>
    </html>
    ```

## 头部

HTML 头部指的是用标签 `<head></head>` 包起来的内容，这些内容不会呈现在网页上，用于指定网页的元数据。

- `<title>` 元素：指定网页的标题（这里的标题指的是浏览器标签栏上的标题，或者书签名，不是网页上那些加粗加大的文本）
- `<meta>` 元素：指定一些元数据，比如字符编码、作者、网页描述（后面两者需要指定 `name` 和 `content` 属性）等，有些网站还有专门设计的 `<meta>` 属性，为用户提供更好的体验（例如：[Facebook](https://ogp.me/)、[Twitter](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)）。
    - 字符编码：`<meta charset="utf-8">`
    - 作者：`<meta charset="author" content="NoughtQ">`
    - 描述：`<meta charset="description" content="This is my HTML Doc~">`，描述的内容会在浏览器的搜索结果中显示。
- 网站图标（favicon）设置：`<link rel="icon" href="name.ico" type="path/to/your/favicon"/>`
- 引入外部 CSS 文件：`<link rel="stylesheet" href="my-css-file.css" />`
- 引入外部 JavaScript 文件：`<script src="my-js-file.js" defer></script>`

可以为 HTML 网页设置语言：向`<html>` 元素添加 `lang` 属性来指定语言，比如 `zh-CN`、`en-US` 等

## 文本内容

- `<p>` 元素：指定一个段落
- `<h1>`、`<h2>`、`<h3>`、`<h4>`、`<h5>`、`<h6>` 元素：指定文本的标题，大小依次递减。标题的设置应遵循以下原则：
    - 顶级标题 `<h1>` 最好只用一次
    - 按顺序使用标题，不要出现 `<h3>` 标题后跟 `<h2>` 子标题的奇怪表示
    - 标题层级不宜过多，争取限制在三级以内，最多四级（~~后面两个标题比正文还小~~）
- 列表（列表之间可以嵌套）：
    - 无序列表（**u**nordered **l**ist）（~~这段笔记就是无序列表~~）：外层由 `<ul>` 标签包裹，每行内容用 `<li>` 标签包裹
    - 有序列表（**o**rdered **l**ist）：外层由 `<ol>` 标签包裹，每行内容用 `<li>` 标签包裹
    
    ??? example "例子"

        === "无序列表"

            ``` html
            <ul>
                <li>去骨鸡胸肉：一斤八两</li>
                <li>干红辣椒：八钱</li>
                <li>炸花生米：一两五钱</li>
                <li>花椒粒：两大匙</li>
                <li>葱：两根（切段）</li>
            </ul>
            ```
            <div style="text-align: center">
                <image src="images/html/2.png" width=30%>
            </div>

        === "有序列表"

            ``` html
            <ol>
                <li>先用蛋白一个、盐半茶匙及淀粉两大匙搅拌均匀，调成“腌料”，鸡胸肉切成约一厘米见方的碎丁并用“腌料”搅拌均匀，腌渍半小时。</li>
                <li>用酱油一大匙、淀粉水一大匙、糖半茶匙、盐四分之一茶匙、白醋一茶匙、蒜末半茶匙调拌均匀，调成“综合调味料”。</li>
                <li>鸡丁腌好以后，色拉油下锅烧热，先将鸡丁倒入锅内，用大火快炸半分钟，炸到变色之后，捞出来沥干油汁备用。</li>
            </ol>    
            ```

            <div style="text-align: center">
                <image src="images/html/3.png" width=100%>
            </div>


- 强调文本（内联元素）
    - `<em>` 元素：斜体，有强调语义
    - `<strong>` 元素：粗体，有强调语义
    - `<i>` 元素：斜体
    - `<b>` 元素：粗体
    - `<u>` 元素：下划线
- 上标：`<sup>`，下标：`<sub>` 
- 代码块相关：
    - `<code>` 元素：将文本渲染为代码块（块级、行内均可）
    - `<pre>` 元素：保留空白字符（文本编辑器上有多少空白，网页就显示多少空白，常用于代码块）
    - `<var>` 元素：标记变量名
    - `<kbd>` 元素：标记键盘输入
    - `<samp>` 元素：标记计算机程序输出

    ??? example "例子"

        ``` html
        <pre><code>const para = document.querySelector('p');

        para.onclick = function() {
            alert('Owww, stop poking me!');
        }</code></pre>

        <p>
            You shouldn't use presentational elements like <code>&lt;font&gt;</code> and
            <code>&lt;center&gt;</code>.
        </p>

        <p>
            In the above JavaScript example, <var>para</var> represents a paragraph
            element.
        </p>

        <p>Select all the text with <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>A</kbd>.</p>

        <pre>$ <kbd>ping mozilla.org</kbd>
        <samp>PING mozilla.org (63.245.215.20): 56 data bytes
        64 bytes from 63.245.215.20: icmp_seq=0 ttl=40 time=158.233 ms</samp></pre>
        ```

        <div style="text-align: center">
            <image src="images/html/6.png" width=60%>
        </div>
        
- :star2:无语义元素：本身没有任何意义，但可以通过指定一些属性（比如引入 CSS 样式或 JS 脚本）使其变得有意义，这便于我们进行一些自定义的设计。
    - `<span>` 标签：内联级
    - `<div>` 标签：块级
- 换行符（单独使用）
    - `<br/>`：段落内换行
    - `<hr/>`：换行 + 水平分隔线


??? info "个人认为没啥用的语法"

    - 描述列表：用于指定术语和定义、问题和答案之类的文本。列表最外层用 `<dl>` 标签包裹，术语部分用 `<dt>` 标签包裹，描述部分用 `<dd>` 包裹。单个术语可以对应多个描述

    ??? example "例子"

        ``` html
        <dl>
            <dt>培根</dt>
            <dd>整个世界的粘合剂。</dd>
            <dt>鸡蛋</dt>
            <dd>一块蛋糕的粘合剂。</dd>
            <dt>咖啡</dt>
            <dd>一种浅棕色的饮料。</dd>
            <dd>可以在清晨带来活力。</dd>
        </dl>
        ```

        <div style="text-align: center">
            <image src="images/html/5.png" width=30%>
        </div>

    - 引用（~~貌似没啥用~~）
        - 块引用：使用 `<blockquote>` 标签，并用 `cite` 属性指明 URL，网页上会呈现缩进的内容
        - 行内引用：使用 `<q>` 标签，并用 `cite` 属性指明 URL，网页会将里面的内容用引号包起来
    - 缩略语：使用 `<abbr>` 标签，里面的内容为缩略语，在网页中用下划虚线标注，鼠标光标悬停在上面就会显示设置好的完整解释（在 `title` 属性指出）
    - 联系方式：使用 `<address>` 标签，网页上表现为斜体
    - 时间：使用 `<time>` 标签，`datatime` 属性设置时间格式，以便计算机识别，有许多可选的[时间格式](https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Introduction_to_HTML/Advanced_text_formatting#%E6%A0%87%E8%AE%B0%E6%97%B6%E9%97%B4%E5%92%8C%E6%97%A5%E6%9C%9F)。


## 超链接

`<a>` 元素用来实现超链接的表示，它可以包裹任何内容，甚至是块级内容（比如图片等）。

基本格式：`<a href="https://www.example.com">Content</a>`

- `title` 属性可以指定链接的补充信息，当我们将鼠标悬停在连接上时就会出现这个提示信息。
- `href` 的值可以是：
    - 网页地址（即 URL），有绝对地址和相对地址的表示法
    - 电子邮件地址，以 `mailto:` 开头，后跟邮件地址，还可以在后面添加邮件头字段，比如主题 `subject`、抄送 `cc`、主体 `body`，这里就不展开了
    - 本地地址，建议使用相对地址
    - 某个文档片段。`href` 的值以`#`开头，后面跟上文档片段的 `id`，这个 `id` 的值是该文档片段 `id` 属性的值

    ???+ example "例子"

        ``` html
        <h1>数论基础</h1>

        <!-- 省略一大段文本 -->
        <p>...</p>

        <h2 id="theorem">费马小定理</h2>

        <p>...</p>
        <!-- 省略一大段文本 -->
        <p>...</p>

        这里我们用到了<a href="#theorem" >费马小定理</a>
        ```

        !!! play "动画演示"

            <div style="text-align: center">
                <image src="images/html/4.gif" width=70%>
            </div>  

- `download` 属性：当链接是一个下载链接时，使用该属性可以指定下载文件被保存的文件名  

## 网页架构

下面是 `<body>` 元素该放的内容：

- 页眉 `<header>`：网页顶部的标题、标志
- 导航栏 `<nav>`：各子页面的标题和链接、标签页
- 主内容 `<main>` 只能有一个，且放在 `<body>` 标签内，子内容可用以下元素表示：
    - `<article>`：一篇文章
    - `<section>`：用于组织页面，可按功能划分不同区块
    - `<div>`
- 侧边栏 `<aside>`：辅助信息（作者信息、术语条目、相关链接等）或广告
- 页脚 `<footer>`：版权、联系方式等

## 多媒体

- 图片元素 `<img>`，它是一个空元素，它的属性有：
    - `src`：（必需）指定图片文件路径，类似 `<a>` 元素的 `href` 属性，建议使用相对 URL
    - `alt`：当图片无法加载成功时（图片路径错误、浏览器不支持等原因）显示的替代文本（简单介绍图片内容）
    - `width`：图片宽度，整数值，单位：像素
    - `height`：图片高度，整数值，单位：像素
    >注：如果没有指定图片的宽高，网页加载时若图片加载缓慢，图片下面的部分会先顶上来，等图片加载完后又会回去，很影响阅读，因此建议设置这两个属性。 

    - `title`：（不推荐使用）指定图片标题，当光标悬停在图片上时就会显示图片标题
    - 为图片配上说明文字的推荐方法是使用 `<figure>` 和 `<figcaption>` 元素。`<figure>` 标签将 `<img>` 和 `<figcaption>` 元素包裹起来，而 `<figcaption>` 指定图片说明文字。
    >注：`<figure>` 标签内还可嵌入多张图片，或者代码块、方程、视频等内容。

    ??? example "例子"

        ``` html
        <figure>
            <img
            src="favicon.png"
            alt="This is a favicon, where a young man holds his knife."
            width="100"
            height="100" />
        
            <figcaption>
            This is the favicon of my notebook website.
            </figcaption>
        </figure>
        ```

        <div style="text-align: center">
            <image src="images/html/7.png" width=50%>
        </div> 
    
>注：HTML 图片应该是对内容具有意义的图片，而 CSS 图片仅做装饰使用

- 绘制矢量图形元素 `<svg>`，它可以嵌入以下空元素：
    - `<rect>`：绘制矩形
    - `<circle>`：绘制圆圈
    - `<path>`：绘制路径
    - `<polygon>`：绘制多边形

??? info "关于矢量图片的插入"

    矢量图片有多重插入方式，它们各有优劣，具体分析见 [MDN 文档](https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Multimedia_and_embedding/Adding_vector_graphics_to_the_Web#%E5%B0%86_svg_%E6%B7%BB%E5%8A%A0%E5%88%B0%E9%A1%B5%E9%9D%A2)

    - `<img>` 元素直接引入
    - `<svg>` 元素引入 SVG 代码
    - `<iframe>` 元素嵌入

??? note "设置响应式图片"

    根据屏幕尺寸的不同，我们应该为**同一张图片**设置不同的、合适的尺寸或分辨率，这样能增强访客的阅读体验。这里我们用到 `<image>` 元素的两个属性 `srcset` 和 `sizes` 属性，其中：

    - `srcset`：设置多张图片路径的集合，根据不同情况有不同的设置方法：
        - 按不同的尺寸：
            - 文件名
            - 一个空格
            - 图片的固有宽度，单位为 w
        - 按不同的分辨率：
            - 文件名
            - 一个空格
            - `<double_number>x` 表示分辨率
    - `sizes`：图片的宽和高，用逗号间隔，可以设置一个类似 if 语句的值，根据情况调节尺寸，格式为：
        - 媒体条件（用圆括号包裹，比如 `max-width:600px`）
        - 一个空格
        - 当条件为真时应该设置的宽度或高度
    
    除此之外，还可以使用 `<picture>` 元素，根据屏幕尺寸的不同显示**不同的图片**，它里面包着 `<source>` 元素和 `<img>` 元素（必需），其中 `<source>` 元素有以下属性：
    
    - `media`：设置媒体条件，用括号包裹起来（比如 `(max-width: 799px)`、`min-width: 800px`）
    - `srcset`：图片路径

- 视频元素 `<video>`，它可以嵌入内容（当视频无法加载出来时显示这段内容），它的属性有：
    - `src`：视频路径，同图片元素
    - `controls`：（布尔属性），使视频播放具备基本的控制界面（比如暂停键、全屏键、音量调整等）
    - 可以为同一个视频配置多种播放源，从而提升视频的兼容性。这时不用 `src` 属性，而是在 `<video>` 标签内嵌入多个 `<source>` 空元素。这个元素包括 `src` 和 `type` 属性，前者同上，后者指明视频文件类型（`video/xxx`）

    ??? example "例子"

        ``` html
        <video controls>
            <source src="rabbit320.mp4" type="video/mp4" />
            <source src="rabbit320.webm" type="video/webm" />
            <p>你的浏览器不支持此视频。可点击<a href="rabbit320.mp4">此链接</a>观看</p>
        </video>
        ```

    - `width`、`height`：指定视频尺寸，意义同图片元素
    - `autoplay`：（不推荐，布尔属性）立即播放
    - `loop`：（不推荐，布尔属性）循环播放
    - `muted`：（布尔属性）默认静音
    - `poster`：设置预览图片或广告，其值为文件路径
    - `preload`：用于缓冲较大文件，有三个可选值
        - `none`：不缓冲文件
        - `auto`：缓冲文件
        - `metadata`：仅缓冲元数据

- 音频元素 `<audio>`，使用上几乎与视频元素一样，只有以下视觉上的细微区别：
    - 无法设置 `width` 和 `height` 属性
    - 无法设置 `poster` 属性

!!! note "为视频和音频配上字幕"

    在 `<video>` 或 `<audio>` 标签内嵌入 `<track>` 元素，引入字幕文件（.vtt），它的属性如下：

    - `kind`：字幕类型，有3种
        - `subtitles`：外语翻译字幕
        - `captions`：同步翻译对白
        - `description`：由媒体播放器朗读的文本，供视障人士使用
    - `src`：文件路径
    - `srclang`：字幕语言
    - `label`：标记内容，建议说明视/音频语言
- 嵌入第三方内容（比如在线视频商（B站、Youtube 之类的）的视频、在线地图（Google Maps）、广告、评论系统（Disqus 等））：`<iframe>` 元素
    - 使用前，可以先设置 CSS 样式，使其不显示默认出现的（~~很丑的~~）边框

    ``` css
    iframe {
      border: none;
    }
    ```

    - `allowfullscreen` （布尔）属性：设置全屏模式
    - `src` 属性：指明嵌入内容的 URL
    - `width` 属性：指明嵌入内容的宽高
    - `sandbox` （布尔）属性：（强烈推荐使用）提高安全性设置
    - `<iframe>` 的使用有一定的安全隐患（比如点击劫持等），遵循以下原则可以避免危险的发生：
        - 只有在有必要时嵌入
        - 使用 HTTPS
        - 始终使用 `sandbox` 属性
        - 配置 CSP（内容安全策略）指令

- 其他嵌入方法（嵌入 PDF 等）：`<embed>` 和 `<object>` 元素，它们在使用有一些小区别：
    - `type`（文件类型）、`width`、`height` 属性的意义一致
    - `<embed>` 采用 `src` 属性，对应 `<object>` 的 `data` 属性，指明嵌入文件的 URL
    - 略过一些细枝末节的东西

??? example "例子"

    ``` html
    <object data="mypdf.pdf" type="application/pdf" width="800" height="1200">
    <p>
        You don't have a PDF plugin, but you can
        <a href="mypdf.pdf">download the PDF file. </a>
    </p>
    </object>
    ```

## 表格

- 最外层用 `<table>` 标签包裹
- 表格的每一行内容用 `<tr>` 标签包裹
- 表格的每一个单元格内容用 `<td>` 标签包裹
- 用 `<th>` 标签替代 `<td>` 标签，使单元格内字体变粗，常用于表格标题部分。它有以下属性：
    - `scope` ：可以描述单元格的类型（便于屏幕阅读器识别，为视障人士提供便利）
    - `id`：与 `<td>` 的 `header` 属性搭配使用，`header` 的值为一组 `id` 值，中间用空格隔开，还是为视障人士提供便利
- 在 `<td>` 或 `<th>` 标签内设置 `colspan` 或 `rowspan` 属性，可以使某个单元格占据指定数量单元格的宽度或高度

??? example "例子"

    ``` html
    <table>
        <tr>
        <th colspan="2">Animals</th>
        </tr>
        <tr>
        <th colspan="2">Hippopotamus</th>
        </tr>
        <tr>
        <th rowspan="2">Horse</th>
        <td>Mare</td>
        </tr>
        <tr>
        <td>Stallion</td>
        </tr>
        <tr>
        <th colspan="2">Crocodile</th>
        </tr>
        <tr>
        <th rowspan="2">Chicken</th>
        <td>Hen</td>
        </tr>
        <tr>
        <td>Rooster</td>
        </tr>
    </table>
    ```

    <div style="text-align: center">
        <image src="images/html/8.png" width=25%>
    </div> 

- 在`<table>` 内嵌内容的开头使用 `<colgroup>` 元素，便于为表格的每一列设置共同的样式。`<colgroup>` 内部嵌入 `<col>` 空元素，按顺序设置对应列的样式。因此 `<col>` 会用到 `style` 属性；也可以使用 `span` 属性，用于指明样式生效的列数（如果该值等于列数，则该样式在整张表格上生效）。

??? example "例子"

    ``` html
    <table>
        <colgroup>
        <col />
        <col style="background-color: yellow" />
        </colgroup>
        <tr>
        <th>Data 1</th>
        <th>Data 2</th>
        </tr>
        <tr>
        <td>Calcutta</td>
        <td>Orange</td>
        </tr>
        <tr>
        <td>Robots</td>
        <td>Jazz</td>
        </tr>
    </table>
    ```

    <div style="text-align: center">
        <image src="images/html/9.png" width=20%>
    </div> 

- 在`<table>` 内嵌内容的开头使用 `<caption>` 元素，指定表格的标题
- 为了让表格内容更加结构化，可以使用 `<thead>`、`<tbody>`、`<tfoot>` 三类标签，一般用于表格内容的开头、主体和末尾部分（若没有明确指明这三者，HTML 会隐式添加 `<tbody>`）。虽然直接用没什么效果，但我们可以通过分别指定它们的样式来展现表格的层次感。
- 表格可以嵌套

## 表单

TODO