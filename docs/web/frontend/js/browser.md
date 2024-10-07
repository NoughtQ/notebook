---
counter: ture
---

# JavaScript 浏览器相关

## Document

JS 在浏览器运行时的架构图

<figure style=" width: 50%" markdown="span">
    ![](../images/js/7_dark.png#only-dark)
    ![](../images/js/7_light.png#only-light)
    <figcaption></figcaption>
</figure>

- `window` 既作为 JS 代码的全局对象，也代表“浏览器窗口”，并提供了控制它的方法
- DOM(文档对象模型)：将每个 HTML 标签，以及标签内的文本视为对象，这些对象都可以被 JS 访问和控制
    - DOM 树：将这些对象根据 HTML 内部结构画成一棵树，这棵树也可以看作是由各种节点构成，下面是常见的几种节点：
        - `document`：DOM 的入口点
        - 元素节点：HTML 标签
        - 文本节点：文本
        - 注释：虽然不显示，但是 JS 可以从 DOM 树中读取


- BOM(浏览器对象模型)：DOM 之外的其他对象，比如
    - navigator 对象：提供有关浏览器和操作系统的背景信息
    - location 对象：允许读取当前 URL，并可以将浏览器重定向到新的 URL
    - `alert/confirm/prompt` 函数也是 BOM 的一部分

### DOM 导航属性
    
下面列出的导航属性引用**所有节点**：

<figure style=" width: 50%" markdown="span">
    ![](../images/js/8_dark.png#only-dark)
    ![](../images/js/8_light.png#only-light)
    <figcaption></figcaption>
</figure>

- 顶层
    - `<html>` = `document.documentElement`
    - `<body>` = `document.body`
        - 如果 `<body>` 内运行不在 `<body>` 内的脚本（比如 `<header>` 里有 JS 代码），那么 `document.body` 的值为 `null`
    - `<head>` = `document.head`
- 子节点
    - `.childNodes`：列出所有子节点（可看做集合），包括文本节点
        - 可以使用 `for...of` 循环遍历子节点
        - 可以使用方括号括起来的索引访问单个子节点
        - `.childNodes.length`：子节点个数
        - 无法使用数组方法
    - `.firstChild`：第一个子元素
    - `.lastChild`：最后一个子元素
    - `.hasChildNodes()`：检查是否有子节点
- 兄弟节点
    - `nextSibling`：下一个兄弟节点
    - `previousSibling`：上一个兄弟节点
- 父节点：`parentNode`

---
下面列出的导航属性只考虑**元素节点**：

<figure style=" width: 50%" markdown="span">
    ![](../images/js/9_dark.png#only-dark)
    ![](../images/js/9_light.png#only-light)
    <figcaption></figcaption>
</figure>

- 子节点
    - `children`：列出所有子元素节点
    - `firstElementChild`：第一个子元素节点
    - `lastElementChild`：最后一个子元素节点
- 兄弟节点
    - `previousElementSibling`：前一个兄弟元素节点
    - `nextElementSibling`：后一个兄弟元素节点
- 父元素节点：`parentElement`

---
**表格**

- `<table>` 
    - `table.rows`：`<tr>` 元素的集合
    - `table.caption`：引用元素 `<caption>`
    - `table.tHead`：引用元素 `<thead>`
    - `table.tFoot`：引用元素 `<tfoot>`
    - `table.tBodies`：`<tbody>` 元素的集合
- `<thead>`、`<tfoot>`、`<tbody>` 元素的 `rows` 属性
    - `thead.rows`
    - `tfoot.rows`
    - `tbody.rows`  
- `<tr>`
    - `tr.cells`：在给定 `<tr>` 中 `<td>` 和 `<th>` 单元格的集合
    - `tr.sectionRowIndex`：给定 `<tr>` 在封闭的 `<thead>/<tbody>/<tfoot>` 元素内的位置（索引）
    - `tr.rowIndex` —— 在整个表格中 `<tr>` 的位置（索引）
- `<td>` 和 `<th>`
    - `td.cellIndex`：在封闭的 `<tr>` 中单元格的编号


!!! waring "注意"

    - 在 DOM 中，值为 `null` 不代表节点不存在
    - DOM 集合（比如 `.childNodes`）是只读的（不可修改）、实时的

### 获取元素

- `document.getElementById(elem)`：获取 `id` 属性值为 `elem` 的元素
- `document.querySelectorAll(selector)`：获取与给定 CSS 选择器匹配的所有元素（一个静态的集合），选择器可以是伪类
- `document.querySelector(selector)`：获取与给定 CSS 选择器匹配的第一个元素
- `elem.matches(selector)`：检查元素 `elem` 是否与给定的 CSS 选择器匹配，返回布尔值
- `elem.closest(selector)`：查找与 CSS 选择器匹配的最近的祖先（包括元素 `elem`）

??? example "例子"

    ``` html
    <h1>Contents</h1>

    <div class="contents">
        <ul class="book">
            <li class="chapter">Chapter 1</li>
            <li class="chapter">Chapter 2</li>
        </ul>
    </div>

    <script>
        let chapter = document.querySelector('.chapter'); // LI

        alert(chapter.closest('.book')); // UL
        alert(chapter.closest('.contents')); // DIV

        alert(chapter.closest('h1')); // null（因为 h1 不是祖先）
    </script>
    ```

- `getElementsBy*` 方法系列（返回的是一个实时的集合）：
    - `elem.getElementsByTagName(tag)` 查找具有给定标签的元素，并返回它们的集合。若 `tag` 值为 `*`，则查找所有标签
    - `elem.getElementsByClassName(className)` 查找具有给定 CSS 类的元素
    - `document.getElementsByName(name)` 查找在文档范围内具有给定 name 特性的元素（很少使用）

### 属性

下面是一些常用的 **DOM 属性**（大小写敏感，有多种类型的值）：

- `.nodeType`：获取 DOM 节点的类型，有以下几种返回值（数字型）
    - `1`：元素节点
    - `3`：文本节点
    - `9`：document 对象
    - 其他，见[规范](https://dom.spec.whatwg.org/#node)
- `.nodeName` 和 `tagName`：读取 DOM 节点的标签名（全部大写），它们的区别在于：
    - `.tagName` 仅适用于元素节点（若读取其他节点返回 `undefined`）
    - `.nodeName` 适用于任意节点
        - 元素节点：同 `.tagName`
        - 其他节点：有一个对应节点类型的字符串
- `.innerHTML`：获取元素节点内的 HTML 内容，并以字符串的形式呈现
    - 对 `.innerHTML` 进行 `+=` 运算会完全覆写原来的内容，而不是在后面加上新内容，所以不要这么做
    - 它会将获取的元素标签转化为有意义的内容，而不是把它当作字符串处理
- `.outerHTML`：获取完整的 HTML 代码（包括标签），并以字符串的形式呈现
    - 与 `.innerHTML` 不同，写入 `.outerHTML` 不会修改 DOM 元素，而是将其从 DOM 中删除并在该位置插入新的 HTML。

??? example "例子"

    ``` html
    <div>Hello, world!</div>

    <script>
        let div = document.querySelector('div');

        // 使用 <p>...</p> 替换 div.outerHTML
        div.outerHTML = '<p>A new element</p>'; // (*)

        // 'div' 的值没有变化
        alert(div.outerHTML); // <div>Hello, world!</div> (**)
    </script>
    ```

    `(*)` 行进行了以下过程：

    - `div` 被从文档（document）中移除
    - 另一个 HTML 片段 `<p>A new element</p>` 被插入到其位置上
    - `div` 仍拥有其旧的值。新的 HTML 没有被赋值给任何变量

- `.nodeValue` 和 `.nodeData`：可获取除元素节点之外的节点（比如文本节点、注释等）内的 HTML 内容，并以字符串的形式呈现
- `.textContent`：对元素内的文本进行访问（不包括标签）
    - 它允许以安全方式写入文本，所有符号都被看作一般的字符
- `.hidden`：指定元素是否可见，接受布尔值（类似 CSS `display: none` 语句）
- `.value`：获取 `<input>`、`<select>`、`<textarea>` 等元素的值
- `.href`：获取 `<a>` 元素 `href` 属性的值
- `id`：获取所有元素 `id` 属性的值

--- 
由于 DOM 节点本质上是一个 JS 对象，所以我们可以更改 DOM 节点的属性，比如：

``` js
document.body.myData = {
  name: 'Caesar',
  title: 'Imperator'
};

// 还可以添加方法
document.body.sayTagName = function() {
  alert(this.tagName);
};
```

可以通过 `Element.prototype` 为所有元素添加新属性：

``` js
Element.prototype.sayHi = function() {
  alert(`Hello, I'm ${this.tagName}`);
};

document.documentElement.sayHi(); // Hello, I'm HTML
document.body.sayHi();            // Hello, I'm BODY
```

---
关于 **HTML 属性**（大小写不敏感，值为字符串型）：

- `elem.haAttribute(attr)`：检查该元素是否有 `attr` 属性
- `elem.getAttribute(attr)`：获取该元素 `attr` 属性的值
- `elem.setAttribute(attr, value)`：设置该元素 `attr` 属性的值为 `value`
- `elem.removeAttribute(attr)`：移除该元素 `attr` 属性的值
- `elem.attributes`：读取该元素所有的属性，这会创建一个 Attr 类对象的集合，每个对象都有名为 `name` 和 `value` 的属性

!!! note "注"

    所有以 "data-" 的 HTML 属性被保留供程序员使用（我们可以用这类名称设置自定义 HTML 属性），可以用 `.dataset` DOM 属性使用
    
    - 比如 `<body>` 元素有一个名为 `data-about` 的 HTML 属性，那么可以通过 `document.body.dataset.about` 来获取它的值
    - 如果属性名类似 `data-order-state` 由多词构成，那么它对应的 DOM 属性为 `dataset.orderState`（驼峰式）

!!! success "建议"

    在大多数情况下，最好使用 DOM 属性，仅当 DOM 属性无法满足开发需求，并且真的需要特性时，才使用特性。

### 修改页面

- 创建 DOM 节点（不会直接出现在页面）
    - `document.createElement(tag)`：创建元素节点
    - `document.createTextNode(text)`：创建文本节点
- 插入（多个） DOM 节点或字符串（自动转为文本节点）
    - `node.append(...nodes or strings)`：在节点末尾（内部）插入
    - `node.prepend(...nodes or strings)`：在节点开头（内部）插入
    - `node.before(...nodes or strings)`：在节点前面（外部）插入
    - `node.after(...nodes or strings)`：在节点后面（外部）插入
    - `node.replaceWith(...nodes or strings)`：将节点替换为给定的节点或字符串
    >如果插入的字符串是一些特殊字符（比如 `<`、`>` 等），那么插入页面后会被转化为特殊编码（对应为 `&lt;`、`&gt;`）
- 在相邻位置插入内容
    - HTML 字符串（插入的 HTML 标签有意义）：`elem.insertAdjacentHTML(where, html)`
    - 文本：`elem.insertAdjacentText(where, text)`
    - 元素：`elem.insertAdjacentElement(where, elem)`
    - 第一个参数 `where` 是代码字(code word)，指定相对于 `elem` 的插入位置，可用值有：
        - `"beforebegin"`：在 `elem` 前面（外部）插入
        - `"afterbegin"`：在 `elem` 开头（内部）插入
        - `"beforeend"`：在 `elem` 末尾（内部）插入
        - `"afterend"`：在 `elem` 后面（外部）插入
- 节点移除：`node.remove()`
    - 移动节点到另外的位置时，无需将其从原来的位置中删除
- 克隆节点：`elem.cloneNode(bool)`，可接受的值有
    - `true`：克隆元素的所有 HTML 属性和子元素
    - `false`：不会克隆子元素
- 老式的 DOM 操作（平时不用，仅作了解）：
    - `parentElem.appendChild(node)`：将 `node` 插入 `parentElem` 的末尾（内部）
    - `parentElem.insertBefore(node, nextSibling)`：在 `parentElem` 的 `nextSibling` 前插入 `node`
    - `parentElem.replaceChild(node, oldChild)`：替换子节点 `oldChild` 为 `node`
    - `parentElem.removeChild(node)`：移除子节点 `node`
    - `document.write(html)`：在页面加载完成之前将 HTML 附加到页面。若在页面加载后调用该函数则会覆写原来页面的内容
- 管理 CSS 样式（开头为元素 `elem`）：
    - `.className`：返回 HTML `class` 属性的值
    - `.classList`：用于控制单个类，可遍历。它有以下方法：
        - `.add(class)`、`.remove(class)`：添加/移除类
        - `.toggle(class)`：若不存在类 `class` 就添加，若存在则删除该类
        - `.contains(class)`：检查类是否存在，返回布尔值
    - `.style`：对应 HTML `style` 属性
        - 后面可以接着它包含的 CSS 属性，比如 `elem.style.width` 对应 `style` 的 `width` 属性
        - 对于多词属性（比如 `background-color`），需要使用驼峰表示法（对应 `elem.style.backgroundColor`）
        - 移除样式属性：
            - 将其赋值为空字符串（比如 `elem.style.display = ""`）
            - `elem.style.removeProperty('style_property')`
        - `.cssText`：对样式进行完全的覆写，比如：

        ``` html
        <div id="div">Button</div>

        <script>
            div.style.cssText=`color: red !important;
                background-color: yellow;
                width: 100px;
                text-align: center;
            `;
        </script>
        ```

        - 读取样式：`getComputedStyle(elem[, pseudo])` 函数
            - 其中 `elem` 为要读取样式值的元素，`pseudo` 表示伪元素（）
            - 返回值是一个类似 `elem.style` 的对象，只读，无法修改
    - 调整元素大小：下面是 CSS 盒子模型与 JS 几何属性的对应图

        <figure style=" width: 50%" markdown="span">
            ![](../images/js/12_dark.png#only-dark)
            ![](../images/js/12_light.png#only-light)
            <figcaption></figcaption>
        </figure>
        <figure style=" width: 50%" markdown="span">
            ![](../images/js/13_dark.png#only-dark)
            ![](../images/js/13_light.png#only-light)
            <figcaption></figcaption>
        </figure>

        - `offsetParent` 是外面最接近的祖先，包括：
            - CSS 定位（`position`，可选值有 `absolute`、`relative`、`fixed`、`sticky`）
            - `<td>`、`<th>`、`<table>`
            - `<body>`
        - `.offsetLeft`、`offsetTop`：相对于 `offsetParent` 左上角的 x/y 坐标（类似外边距吧）

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/14_dark.png#only-dark)
            ![](../images/js/14_light.png#only-light)
            <figcaption></figcaption>
        </figure>

        - `offsetWidth`、`offsetHeight`：包括元素外部的宽高（内容 + 内边距 + 边框厚度）

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/15_dark.png#only-dark)
            ![](../images/js/15_light.png#only-light)
            <figcaption></figcaption>
        </figure>

        - `clientTop`、`clientLeft`：分别表示上边框宽度和左边框宽度

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/16_dark.png#only-dark)
            ![](../images/js/16_light.png#only-light)
            <figcaption></figcaption>
        </figure>

        - `clientWidth`、`clientHeight`：分别表示边框内的宽和高，包括的区域是盒子内容 + 内边距，但不包括垂直/水平滚动条的宽度

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/17_dark.png#only-dark)
            ![](../images/js/17_light.png#only-light)
            <figcaption></figcaption>
        </figure>

        - `scrollWidth`、`scrollHeight`：在 `clientWidth/clientHeight` 的基础上还算上了滚动条隐藏的内容的宽高

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/18_dark.png#only-dark)
            ![](../images/js/18_light.png#only-light)
            <figcaption></figcaption>
        </figure>    

        - `scrollLeft`、`scrollTop`：分别表示左方和上方被隐藏内容的宽度/高度（即已经滚动了多少内容）
            - 这里列出的“调整元素大小”的属性中，只有该属性是可以修改的，可以决定浏览器滚动到何种程度

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/19_dark.png#only-dark)
            ![](../images/js/19_light.png#only-light)
            <figcaption></figcaption>
        </figure>    

    - 坐标：有两套坐标系，分别是相对于窗口（用 `clientX` 和 `clientY` 表示）和相对于文档（用 `pageX` 和 `pageY` 表示）的坐标系，如图所示（上图为滚动前的页面，下图为滚动后的页面）
        <figure style=" width: 50%" markdown="span">
            ![](../images/js/20_dark.png#only-dark)
            ![](../images/js/20_light.png#only-light)
            <figcaption></figcaption>
        </figure> 

        - `elem.getBoundingClientRect()`：返回该元素盒子的窗口坐标，包括以下 8 个属性：
            - `x/y`：盒子原点相对于窗口的 x/y 坐标
            - `width/height`：盒子的宽高
            - `top/bottom`：盒子顶部/底部的 y 坐标
            - `left/right`：盒子左侧/右侧的 x 坐标

        <figure style=" width: 40%" markdown="span">
            ![](../images/js/21_dark.png#only-dark)
            ![](../images/js/21_light.png#only-light)
            <figcaption></figcaption>
        </figure>  

        - `document.elementFromPoint(x, y)`：返回在窗口坐标 `(x, y)` 处嵌套最多的元素（随当前滚动位置的不同而发生变化）
            - 若要根据文档坐标计算，那么还需要加上当前页面滚动（`scrollLeft` 和 `scrollTop`）

## 事件

### 基础部分

事件**处理程序**(handler)：在事件发生时运行的函数，有以下几种方法：

- HTML 属性 `on<event>`：它的值为一个 JS 函数代码的字符串
    - 这里的 `<event>` 包括 `click` 等
    - 仅适用于代码量很少的情况
    - 字符串内不要出现双引号，用单引号替代
    - 属性值里面的 `this` 指的是处理程序所在的元素
    - 不要使用 JS 的 `.setAttribute('on<event>', func)` 来设置，这样做是无效的
- DOM 属性 `elem.on<event>`
    - 这里的 `<event>` 包括 `click` 等
    - 从结果来看与上一种方法类似，从实现上看该方法采用的是 JS 脚本
    - 移除处理程序：`elem.on<event> = null`
    - 虽然后面没带括号，但本质上是一个函数，所以用其他函数赋值时不要加括号，只要函数名就行（否则就是函数调用了）
- 方法 :+1:
    - `elem.addEventListener(event, handler[, options])`：为元素添加一个处理程序（多次调用可为单个元素添加多个处理程序，执行顺序同创建顺序）
        - `event`：事件名，比如 `click`
        - `handler`：处理程序，一般是一个函数
        - `options`：（可选）格式：`{val: boolean}`，可用值 `val` 如下：
            - `once`：若为 `true`，则在触发后自动删除监听器
            - `capture`：见下面“[捕获和冒泡](#捕获和冒泡)”一节
            - `passive`
    - `elem.removeEventListener(event, handler[, options])`：为元素移除处理程序（语法同上）
        - 请确保删除的处理程序和添加的处理程序是同一个函数，否则删除操作无效（所以如果添加匿名函数就没法被删除）

---
**事件对象** `event`：当事件发生时，浏览器会创建一个 `event` 对象并放入信息，该对象可作为参数传递给处理程序。`event` 有以下属性：

- `.type`：事件类型（比如 `click`）
- `.currentTarget`：处理事件的元素，等同于 `this`
- `.clientX`、`.clientY`：指针事件(pointer event)的指针的窗口相对坐标
- ...

`addEventListener()` 的处理程序参数还可以是一个包含 `handleEvent` 方法的对象，此时 `addEventListener()` 会调用 `obj.handleEvent(event)` 来处理时间。

### 捕获和冒泡

**冒泡**(bubbling)的原理：当一个事件发生在一个元素上，它会首先运行在该元素上的处理程序，然后运行其父元素上的处理程序，然后一直向上到其他祖先上的处理程序（一直上升到 `<html>`，再到 document 对象，有的甚至到 window）。几乎所有的事件都会冒泡。

<figure style=" width: 40%" markdown="span">
    ![](../images/js/22_dark.png#only-dark)
    ![](../images/js/22_light.png#only-light)
    <figcaption></figcaption>
</figure>  

引发事件的且嵌套最深的元素被称为**目标元素**，可用 `event.target` 访问，它与 `this` 的区别在于：

- `this` 等同于 `event.currentTarget`，它指的是处理程序所在的当前元素
- `event.target` 指的是引发事件的元素，它在冒泡过程中不会发生变化

停止冒泡的方法：

-  `event.stopPropagation()`：用于停止单个处理程序的冒泡，但当前元素的其他程序不受影响
- `event.stopImmediatePropagation()`：用于停止当前元素所有处理程序的冒泡
- 注意：一般情况下我们没有必要停止冒泡。有些看似需要停止冒泡的任务可以用其他方法解决，比如自定义事件等

---
事件传播的三个阶段：

1. 捕获阶段(capture phase)：事件（从 window）向下走进元素
2. 目标阶段(target phase)：事件到达目标元素
3. 冒泡阶段(bubbling phase)：事件从目标元素开始向上冒泡

<figure style=" width: 40%" markdown="span">
    ![](../images/js/23_dark.png#only-dark)
    ![](../images/js/23_light.png#only-light)
    <figcaption></figcaption>
</figure>

其中捕获阶段很少被使用，之前提到的三种处理程序的方法都不会用到捕获。如果要在捕获阶段捕获事件，需要在 `elem.addEventListener()` 设置参数 `{capture: true}`（`false` 为默认值，表示在冒泡阶段捕获事件）。

??? example "例子"

    ``` html
    <style>
        body * {
            margin: 10px;
            border: 1px solid blue;
        }
    </style>

    <form>FORM
        <div>DIV
            <p>P</p>
        </div>
    </form>

    <script>
        for(let elem of document.querySelectorAll('*')) {
            elem.addEventListener("click", e => alert(`Capturing: ${elem.tagName}`), true);
            elem.addEventListener("click", e => alert(`Bubbling: ${elem.tagName}`));
        }
    </script>
    ```

    将这段代码放入 HTML 文件并用浏览器打开，点击 P 所在的方块，可以发现执行顺序为：

    1. HTML → BODY → FORM → DIV（捕获阶段，第一个监听器）
    2. P（目标阶段，触发两次，因为设置了两个监听器：捕获和冒泡）
    3. DIV → FORM → BODY → HTML（冒泡阶段，第二个监听器）

---
**事件委托**：若有多个元素需要执行相同的处理程序，那么可以将单个处理程序它们的共同祖先上，无需为每一个元素放一个一模一样的处理程序。

??? example "例子"

    ``` html
    <div id="menu">
        <button data-action="save">Save</button>
        <button data-action="load">Load</button>
        <button data-action="search">Search</button>
    </div>

    <script>
        class Menu {
            constructor(elem) {
            this._elem = elem;
            elem.onclick = this.onClick.bind(this); // (*)
            }

            save() {
            alert('saving');
            }

            load() {
            alert('loading');
            }

            search() {
            alert('searching');
            }

            onClick(event) {
            let action = event.target.dataset.action;
            if (action) {
                this[action]();
            }
            };
        }

        new Menu(menu);
    </script>
    ```

    这个例子采用了事件委托的方法，没有为每个按钮写一个处理程序，而是让它们共用一个类，由类根据情况调用特定的程序，这样修改代码较为方便。

---
阻止浏览器行为：

- `event.preventDefault()` 方法
    - 当 `addEventListener()` 函数的 `options` 参数值为 `{passive: ture}` 时，处理程序不会调用 `event.preventDefault()` 方法，因为某些事件需要浏览器的默认行为才能正常进行
- 如果处理程序是用 `on<event>` 分配而非 `addEventListener()`，那么 `return false;` 也能阻止（其他情况下处理程序的 `return` 语句没有任何意义）
- `event.defaultPrevented` 属性：若默认行为被阻止返回 `true`，否则返回 `false`
- 某些事件会相互转化：若阻止了第一个事件，也就没有第二个事件了

### 鼠标事件

- `mousedown/mouseup`：在元素上点击/释放鼠标按钮
- `mouseover/mouseout`：鼠标指针在一个元素上移入/移出
    - 对于前者，`event.target` 是鼠标移入的元素，`event.relatedTarget` 是鼠标出发的元素（`relatedTarget` -> `target`）
    - 对于后者，`event.target` 是鼠标出发的元素，`event.relatedTarget` 是鼠标到达的元素（`target` -> `relatedTarget`）
    - 将鼠标从父元素移动到子元素会经历两个事件：
        - `mouseout`：`[target: parent]`
        - `mouseover`：`[target: child]`
- `mouseenter/mouseleave`：与上一种属性的重要区别：
    - 元素内部和后代之间的转换不会产生影响
    - 不会冒泡（所以不能使用事件委托）
- `mousemove`：鼠标在元素上移动
- `click`：鼠标左键点击元素，`mousedown` 和 `mouseup` 相继触发
- `dbclick`：短时间内双击同一元素（很少使用）
    - 事件顺序：`mousedown` -> `mouseup` -> `click` -> `dbclick`
- `contextmenu`：鼠标右键被按下时触发（用于打开菜单）
- 鼠标按钮：与点击相关（`click`、`contextmenu` 等）具有 `button` 属性，所有可能值有：
    - 0：鼠标左键
    - 1：鼠标中键（即滚轮）
    - 2：鼠标右键
    - 3：X1 键
    - 4：X2 键
- 组合键：一些键盘上的特殊按键也对应鼠标事件的属性，如果在事件发生期间按下特殊键，对应的属性值为 `true`，否则为 `false`。有以下几种属性：
    - `shiftKey`：`Shift`
    - `altKey`：`Alt`
    - `ctrlKey`：`Ctrl`
- 坐标：
    - 相对于窗口：`clientX`、`clientY`
    - 相对于文档：`pageX`、`pageY`

## 表单

### 属性、方法

- 网页所有的表单都在 `document.forms` 的集合内
- 访问特定表单：
    - 使用名字（`name` 属性值）：`document.forms.name`
    - 使用索引：`document.forms[i]`
- 表单内的元素（比如 `<input>` 等）都放在 `form.elements` 的集合内（这里的 `form` 是存储表单的变量）
    - 使用名字（`name` 属性值）访问特定元素：`form.elements.name`
    - 如果有多个名字相同的元素，那么上述访问方法得到的是一个集合，可以用索引获取单个元素
- `elem.form`：访问元素对应的表单

???+ info "表单和元素的引用关系"

    <figure style=" width: 50%" markdown="span">
        ![](../images/js/25_dark.png#only-dark)
        ![](../images/js/25_light.png#only-light)
        <figcaption></figcaption>
    </figure>

- 关于表单组件 
    - `input` 和 `textarea`
        - `.value`（字符串）：输入值
        - `input.checked`（布尔值）：表示是否选中复选框或单选按钮的选项
        - `input.blur()`：移除元素焦点
        - `input.focus`：设置元素焦点

    ??? waring "JS 造成焦点丢失的情况"

        - `alert()` 等交互函数会将焦点移至自身，导致元素失去焦点。但是当取消模态窗后，焦点又会回到原来的元素上
        - 如果一个元素从 DOM 中移除，焦点自然消失；即使之后又重新插入 DOM 中，焦点也不会回来

    - `select`：包括以下属性
        - `.options`：`<option>` 子元素的集合，可用索引访问单个选项。单个选项具有以下属性：
            - `selected`（布尔值）：表示该选项是否被选中
            - `index`：表示该选项的索引号
            - `text`：选项文本内容
        - `.value`：当前选中的 `<option>` 的 `value` 值
        - `.selectedIndex`：当前选中的 `<option>` 的索引号
        - `new Option(text, value, defaultSelected, selected)` 函数：用于创建 `<option>` 元素
            - `text`：`<option>` 的文本
            - `value`：`<option>` 的 `value`
            - `defaultSelected`：若值为 `true` 则创建 `selected` HTML 属性
            - `selected`：若值为 `true`，则选中该 `<option>`。它的值应和前一个参数一致（要么都是 `true`，要么都是 `false`，要么都没有）
- 创建和发送表单

``` js
let form = document.createElement('form');
form.action = 'https://google.com/search';
form.method = 'GET';

form.innerHTML = '<input name="q" value="test">';

// 该表单必须在文档中才能提交
document.body.append(form);

form.submit();
```


### 事件

- `onblur`：元素失去焦点
- `onfocus`：元素聚焦
>注：这两个事件不会冒泡

- `onchange`：元素完成更改，包括：
    - `<input type=text>`：文本输入框失去焦点，但是往文本框输入内容不会触发该事件
    - `<select>`、`<input type=checkbox/radio>`：选项更改
    - ...
- `oninput`：用户对输入值的修改
- `oncut/oncopy/onpaste`：剪切/复制/粘贴
    - `event.clipboardData.getData('text/plain')`：获取剪贴板的文本字符串（这段文本已被成功复制或剪切的情况下使用）
    - `document.getSelection()`：获取被选中的文本，可以是被复制或剪切但未能成功放入剪切板的内容
- `onsubmit`：提交表单，可以通过点击按钮或按下回车键触发事件

## 异步

### 同步和异步

- 同步编程：浏览器按照书写代码的顺序一行行地执行程序
    - 调用函数时也是这样同步执行的，这样的函数被称为**同步函数**
    - 有些同步函数的效率低下，产生耗时问题：在函数运行的时候，程序无法做任何事情（无法处理其他的事件等）
- 异步编程
    - 异步函数的特点：
        - 调用该函数可启动一个长期运行的操作
        - 函数开始运行并立刻返回，这样程序可以对其他事件做出反应
        - 操作完成后，返回操作结果
    - **事件处理程序**便是异步函数的一种形式：提供的函数在事件发生时被调用，而不是立即被调用
    - 回调函数(callbacks)：一种被传递到另一个函数中，会在适当的时候被调用的函数
        - 事件处理程序也是回调函数的一种
        - 回调函数本身也可以调用其他同样接受回调函数的函数，但这样会使代码难以理解
        ??? example "例子"

            ``` js
            function doStep1(init, callback) {
                const result = init + 1;
                callback(result);
            }
            function doStep2(init, callback) {
                const result = init + 2;
                callback(result);
            }
            function doStep3(init, callback) {
                const result = init + 3;
                callback(result);
            }
            function doOperation() {
                doStep1(0, (result1) => {
                    doStep2(result1, (result2) => {
                        doStep3(result2, (result3) => {
                            console.log(`结果：${result3}`);
                        });
                    });
                });
            }
            doOperation();
            ```

            像这样，如果回调函数中嵌套调用多层回调函数，会使代码难以阅读和调试，这样的函数被称为“**厄运金字塔**”（这样的嵌套回调函数看起来像一个倒下的金字塔）。处理嵌套回调函数的错误比较困难，因为要对每一层被调用的回调函数都要做一次错误处理，所以现在的异步 API 都不使用毁回调函数了，而是使用下面讲到的 `Promise`。

### Promise

相关术语：

- 生产者代码(producing code)：需要一定时间来做一些事情
- 消费者代码(consuming code)：立即获取生产者代码的执行结果
- Promise：一种将生产者代码和消费者代码连在一起的一个特殊的 JS 对象

- 构造函数：创建 Promise 对象
    ``` js
    let promise = new Promise(function(resolve, reject) {
        // executor (producing code, name)
    })
    ```

    - **执行函数(executor)**：传递给 `new Promise` 的函数，包含应产出结果的生产者代码。当 `new Promise` 创建后，该函数会自动执行
        - 执行函数获得结果后，会调用以下两种回调函数之一：
            - `resolve(value)`：如果执行成功并返回结果 `value`
            - `reject(error)`：如果出现错误，`error` 即为 error 对象
        - 一个执行函数内只能调用一次 `resolve` 或一次 `reject`，其他的调用都会被忽略
        - `resolve` 和 `reject` 只需要一个参数，额外的参数会被忽略
        - `resolve` 和 `reject` 可以立即执行而无需放在执行函数内

    - Promise 对象有以下内部属性：
        - `state`：初始为 `pending`；若调用 `resolve` 则变为 `fulfilled`，若调用 `reject` 则变为 `rejected`
        - `result`：初始为 `undefined`；若调用 `resolve` 则变为 `value`，若调用 `reject` 则变为 `error`
        - 但这些属性无法被直接访问，需要用其他的方法来访问

        <figure style=" width: 60%" markdown="span">
            ![](../images/js/26_dark.png#only-dark)
            ![](../images/js/26_light.png#only-light)
            <figcaption></figcaption>
        </figure>

    ??? example "例子"

        === "成功"

            ``` js
            let promise = new Promise(function(resolve, reject) {
                setTimeout(() => resolve("done"), 1000);
            });
            ```

            <figure style=" width: 60%" markdown="span">
                ![](../images/js/27_dark.png#only-dark)
                ![](../images/js/27_light.png#only-light)
                <figcaption></figcaption>
            </figure>

        === "失败"

            ``` js
            let promise = new Promise(function(resolve, reject) {
                setTimeout(() => reject(new Error("Whoops!")), 1000);
            });
            ```

            <figure style=" width: 70%" markdown="span">
                ![](../images/js/28_dark.png#only-dark)
                ![](../images/js/28_light.png#only-light)
                <figcaption></figcaption>
            </figure>

- 消费函数
    - `.then`

    ``` js
    // 两个参数都是函数
    // 可以只有一个参数，仅处理一种情况
    promise.then(
        function(result) { /* handle a successful result */ },
        function(error) { /* handle an erro */ }
    );
    ```

    ??? example "例子"

        ``` js
        let promise = new Promise(function(resolve, reject) {
            setTimeout(() => resolve("done!"), 1000);
        });

        promise.then(
            result => alert(result), // 1 秒后显示 "done!"
            error => alert(error) // 不运行
        );
        ```

    - `.catch`：只处理错误情况，即 `.catch(f)` 等价于 `.then(null, f)`

- `finally`：用于执行清理/终结操作，比如停止加载指示器，关闭不再需要的连接等
    - `finally(f)` 类似 `then(f, f)`，但是有以下区别：
        - `finally` 处理程序 `f` 没有参数，且我们不知道 promise 是否成功
        - `finally` 处理程序将结果或 error 传递给下一个合适的处理程序
        - `finally` 处理程序不返回任何内容（如果有返回值则会被忽略）
    ??? example "例子"

        ``` js
        new Promise((resolve, reject) => {
            throw new Error("error");
        })
            .finally(() => alert("Promise ready")) // 先触发
            .catch(err => alert(err));  // <-- .catch 显示这个 error
        ```

- Promise 链
    - 格式类似下面的代码：
    ``` js
    new Promise(function(resolve, reject) {
        setTimeout(() => resolve(1), 1000); 
    }).then(function(result) { 
        alert(result);                // 1
        return result * 2;
    }).then(function(result) { 
        alert(result);                // 2
        return result * 2;
    }).then(function(result) {
        alert(result);                // 4
        return result * 2;
    });
    ```

    执行过程如下图所示，可以发现 `result` 在一系列 `.then` 处理程序中出传递下去（事实上 `.catch` 和 `.finally` 也可以，且它们可以混搭）

    <figure style=" width: 30%" markdown="span">
        ![](../images/js/29_dark.png#only-dark)
        ![](../images/js/29_light.png#only-light)
        <figcaption></figcaption>
    </figure>

    下面是 promise 链的通用流程图：

    <figure style=" width: 60%" markdown="span">
        ![](../images/js/31_dark.png#only-dark)
        ![](../images/js/31_light.png#only-light)
        <figcaption></figcaption>
    </figure>

    - 误区：一个有多个处理函数的 promise 可以实现上面的 promise 链。实际上，这些处理函数是独立的执行的，并不是链式传递的，所以平时也不会用到这种形式。

    ??? example "例子"

        ``` js
        let promise = new Promise(function(resolve, reject) {
            setTimeout(() => resolve(1), 1000);
        });

        promise.then(function(result) {
            alert(result);                  // 1
            return result * 2;
        });

        promise.then(function(result) {
            alert(result);                  // 1
            return result * 2;
        });

        promise.then(function(result) {
            alert(result);                  // 1
            return result * 2;
        });
        ```

        <figure style=" width: 60%" markdown="span">
            ![](../images/js/30_dark.png#only-dark)
            ![](../images/js/30_light.png#only-light)
            <figcaption></figcaption>
        </figure>

    - promise 的处理程序（`.then`、`.catch` 和 `.finally`）可以创建并返回一个 promise。如果 promise 链中有这样的处理程序，那么它后面的处理程序需要等待它 settled（非 pending 状态）后再获取结果

    ??? example "例子"

        ``` js
        new Promise(function(resolve, reject) {
            setTimeout(() => resolve(1), 1000);
        }).then(function(result) {
            alert(result);              // 1
            return new Promise((resolve, reject) => { 
                setTimeout(() => resolve(result * 2), 1000);
        });

        }).then(function(result) { 
            alert(result);              // 2
            return new Promise((resolve, reject) => {
                setTimeout(() => resolve(result * 2), 1000);
        });

        }).then(function(result) {
            alert(result);              // 4
        });
        ```

        这段代码与第一次给出的 promise 链代码相比，在每次调用 `alert` 时都会有 1s 的延迟

    ???+ note "Thenable"

        实际上，处理程序返回的所谓 promise 其实是一个被称为 Thenable 的对象，它是一个具有方法 `.then` 的任意对象，且被当作一个 promise 来对待。这允许我们将自定义的对象和 promise 链集成在一起，而不必继承自 promise

    - 与 fetch API 相关
- 错误处理相关
    - 将 `.catch` 方法放在整条 promise 链的末尾，这样无论前面哪一个方法有问题，`.catch` 就会捕获到它
    - 隐式 try...catch：执行函数和处理程序发生的异常（比如手动抛出错误，或者有编程上的错误等）会被自动捕获，并将 promise 视为 `rejected`；当然也可以用 `.catch` 手动捕获
    - 再次抛出：如果 promise 链中的 `.catch` 如果无法处理错误，将会将该错误抛给下一个 `.catch`（如果成功处理错误就会继续到最近成功的处理程序）
    ??? example "例子"

        ``` js
        // 执行流：catch -> catch
        new Promise((resolve, reject) => {
            throw new Error("Whoops!");
        }).catch(function(error) { // (*)
            if (error instanceof URIError) {
                // 处理它
            } else {
                alert("Can't handle such error");
                throw error; // 再次抛出此 error 或另外一个 error，执行将跳转至下一个 catch
            }
        }).then(function() {
        /* 不在这里运行 */
        }).catch(error => { // (**)
            alert(`The unknown error has occurred: ${error}`);
            // 不会返回任何内容 => 执行正常进行
        });
        ```

    - 如果抛出的 error 没有 `.catch` 方法接住的话，该 promise 就会「卡死」，并在控制台给出相关信息。这类错误是无法恢复的，需要告知用户和服务器
    - 此外还会触发 `unhandledrejection` 事件
    ``` js
    window.addEventListener('unhandledrejection', event => alert(event.reason));
    ```

- Promise API
    - `Promise.all`
        - 语法：
        ``` js
        let promise = Promise.all(iterable);
        ```

        其中 `iterable` 通常是一个 promise 可迭代对象（比如数组、映射等），该方法返回一个新的 promise

        - 如果 `iterable` 中有非 promise 对象，那么它将被“按原样”传递给结果数组
        - 只有当所有给定的 promise 都 resolve 时，新的 promise 才会 resolve，且返回结果为包含所有 promise 返回结果的一个数组，其元素顺序同 promise 数组元素顺序
        - 只要有一个 promise 被 reject，那么 promise 也立即被 reject，且它的 error 就是那个 promise 的 error；剩下的 promise 将会被忽略，不再执行（但可能会 settle）
        

    ??? example "例子"

        ``` js
        let names = ['iliakan', 'remy', 'jeresig'];

        let requests = names.map(name => fetch(`https://api.github.com/users/${name}`));

        Promise.all(requests)
        .then(responses => {
            // 所有响应都被成功 resolved
            for(let response of responses) {
            alert(`${response.url}: ${response.status}`); // 对应每个 url 都显示 200
            }

            return responses;
        })
        // 将响应数组映射（map）到 response.json() 数组中以读取它们的内容
        .then(responses => Promise.all(responses.map(r => r.json())))
        // 所有 JSON 结果都被解析："users" 是它们的数组
        .then(users => users.forEach(user => alert(user.name)));
        ```

    - `Promise.allSettled`
        - 语法同 `Promise.all`
        - 与 `Promise.all` 不同的是，它会等待所有的 promise 都 settle，其结果数组为：
            - 成功执行的 promise 对应的数组元素为 `{status: "fulfilled", value: result}`
            - 出现 error 的 promise 对应的数组元素为 `{status: "rejected", value: error}`
    - `Promise.race`：语法同 `Promise.all`，但它只等待第一个 settled 的 promise 并获取其结果（或 error）
    - `Promise.any`：类似 `Promise.any`，但只等待第一个成功执行的 promise 并返回它的结果。如果没有 promise 成功执行，则返回的 promise 带有特殊 error 对象 `AggregateError`，在它的 `errors` 属性中存储所有的 promise error
    ??? example "例子"

        ``` js
        Promise.any([
            new Promise((resolve, reject) => setTimeout(() => reject(new Error("Ouch!")), 1000)),
            new Promise((resolve, reject) => setTimeout(() => reject(new Error("Error!")), 2000))
        ]).catch(error => {
            console.log(error.constructor.name); // AggregateError
            console.log(error.errors[0]); // Error: Ouch!
            console.log(error.errors[1]); // Error: Error!
        });
        ```

    - `Promise.resolve`
        - 语法：`Promise.resolve(value)`，同：`let promise = new Promise(resolve => resolve(value))`，即用结果 `value` 创建一个 resolved 的 promise
    - `Promise.reject`
        - 语法：`Promise.reject(error)`，同：`let promise = new Promise((resolve, reject) => reject(error))`，即用 `error` 创建一个 rejected 的 promise
    >注：后两种方法很少被用到，一般用 `async` 或 `await` 替代

- Promisification：一个接受回调的函数 -> 一个返回 promise 的函数
    - 转换模板（或者辅助函数(helper)）
    ``` js
    // promisify(f, true) 来获取结果数组
    function promisify(f, manyArgs = false) {
        return function (...args) {
            return new Promise((resolve, reject) => {
                function callback(err, ...results) { // 我们自定义的 f 的回调
                    if (err) {
                        reject(err);
                    } else {
                    // 如果 manyArgs 被指定，则使用所有回调的结果 resolve
                        resolve(manyArgs ? results : results[0]);
                    }
                }

                args.push(callback);

                f.call(this, ...args);
            });
        };
    }

    // 用法：
    f = promisify(f, true); // 或者 promisify(f)
    f(...).then(arrayOfResults => ..., err => ...);
    ```

- 微任务(microtask)：所有的 promise 行为（`.then`、`.catch`、`.finally`）都会经过一个名为 "promise jobs" 的队列（也被称为“微任务队列”），因此程序在当前代码完成之后才会调用队列里的处理程序

??? example "例子"

    ``` js
    let promise = Promise.resolve();
    promise.then(() => alert("promise done!"));
    alert("code finished"); 
    ```

    这段代码对应的程序先执行第 3 行，后执行第 2 行。因为 promise 的处理程序暂时放在队列里，并不会立即执行；先执行最后一行，之后从队列中获取任务并执行。

    <figure style=" width: 60%" markdown="span">
        ![](../images/js/32_dark.png#only-dark)
        ![](../images/js/32_light.png#only-light)
        <figcaption></figcaption>
    </figure>

### async/await

- `async`：在函数前加该关键词，返回值被包装在一个 promise 里
- `await`：让 JS 等待某个 promise，直到 promise 被 settle 并返回结果

    ``` js
    async function f() {
        let promise = new Promise((resolve, reject) => {
            setTimeout(() => resolve("done!"), 1000)
        });
        let result = await promise; // 等待，直到 promise resolve 
        alert(result); // "done!"
    }
    f();
    ```

    - 仅用在 `async` 函数内的 promise 上，否则会报错
    - JS 还可以处理其他的任务，仅仅暂停执行带 `await` 的 promise
    - 也可以用在 thenable 对象
    - 如果 promise 被 reject，那么它会抛出错误，类似 `throw error` 语句
        - 可以用 `try...catch` 来捕获错误
        - 如果没有 `try...catch`，那么异步函数 `f()` 生成的 promise 将变为 rejected，可以在后面添加 `.catch` 来处理这个 error
        - 如果忘记添加 `.catch`，就会出现一个未处理的 promise error

!!! note "注"

    - 若使用 `async/await`，几乎就不会用到 `.then`
    - `async/await` 可以和 `Promise.all` 一起使用

### worker

前面提到过[耗时的同步函数的问题](#同步和异步)，导致整个窗口完全没有响应，这是因为这种程序是单线程的。所谓「**线程**」，指的是程序遵循的一系列指令，而单线程的程序在同一时间只能做一件事。

而 worker 可以使程序拥有多线程，这样的好处是可以同时处理多个任务，而无需等待某个耗时长的任务。但要有一定限制：主代码的变量和 worker 的变量必须隔离，只能通过相互发送消息来进行交互（这也意味着 worker 不能访问 DOM）

worker 种类：

- 专用(dedicated) worker：仅用于一个脚本
- 共用(shared) worker：可以由运行在不同窗口的多个不同脚本共享
- 服务(service) worker：类似代理服务器，缓存资源以便 web app 在离线时工作

下面以专用 worker 为例介绍 worker 的工作流程：

- 将主代码和 worker 代码放在不同的文件内
- 主代码：
    ``` js
    // 在 "generate.js" 中创建一个新的 worker
    const worker = new Worker("./generate.js");

    // 当用户点击 "Generate primes" 时，给 worker 发送一条消息。
    // 消息中的 command 属性是 "generate", 还包含另外一个属性 "quota"，即要生成的质数。
    document.querySelector("#generate").addEventListener("click", () => {
        const quota = document.querySelector("#quota").value;
        worker.postMessage({
            command: "generate",
            quota: quota,
        });
    });

    // 当 worker 给主线程回发一条消息时，为用户更新 output 框，包含生成的质数（从 message 中获取）。
    worker.addEventListener("message", (message) => {
        document.querySelector("#output").textContent =
            `Finished generating ${message.data} primes!`;
    });

    document.querySelector("#reload").addEventListener("click", () => {
        document.querySelector("#user-input").value =
            'Try typing in here immediately after pressing "Generate primes"';
        document.location.reload();
    });
    ```

    - 构造函数 `Worker()` 用于创建 worker，参数为 worker 代码的地址
    - 使用 `work.postMessage()` 向 worker 发送消息，它的参数
    - 有一个 `message` 消息处理器，用于告知 worker 的完成时间和结果数据（通过 `message.data` 获取） 
- worker 代码：
    ``` js
    // 监听主线程中的消息。
    // 如果消息中的 command 是 "generate"，则调用 `generatePrimse()`
    addEventListener("message", (message) => {
        if (message.data.command === "generate") {
            generatePrimes(message.data.quota);
        }
    });

    // 生成质数 (非常低效)
    function generatePrimes(quota) {
        function isPrime(n) {
            for (let c = 2; c <= Math.sqrt(n); ++c) {
                if (n % c === 0) {
                    return false;
                }
            }
            return true;
        }

        const primes = [];
        const maximum = 1000000;

        while (primes.length < quota) {
            const candidate = Math.floor(Math.random() * (maximum + 1));
            if (isPrime(candidate)) {
                primes.push(candidate);
            }
        }

        // 完成后给主线程发送一条包含我们生成的质数数量的消息消息。
        postMessage(primes.length);
    }
    ```

    - worker 首先要通过 `addEventListener()` 来监听来自主代码的消息
    - 使用 `postMessage` 向主代码发送消息，替代原来用 `return` 语句返回值

## Web API

[AJAX](https://en.wikipedia.org/wiki/Ajax_(programming))(Asynchronous JavaScript And XML)

### Fetch

- 基本语法：
    ``` js
    // url：（字面意思），options：可选参数，有 method, headers 等
    // 没有 options 的话就是一个简单的 GET 请求，下载 url 的内容
    let response = fetch(url, options);
    let result = await response.json();

    // 或者 promise 链的形式
    fetch(url, options)
        .then(response => response.json())
        .then(result => /* process result */)
    ```

    其他参数有：

    - `headers`：设置请求头(request header)一个带有输出头的对象，但有[一些头](https://fetch.spec.whatwg.org/#forbidden-header-name)无法被设置
    ``` js
    let response = fetch(protectedUrl, {
        headers: {
            Authentication: 'secret'
        }
    });  
    ```

    - `method`：HTTP 方法，可用值有 `'POST'` 等
    - `body`：设置请求体，可用值有
        - （JSON 编码的）字符串
        - `FormData` 对象，以 `multipart/form-data` 形式发送数据（可用于发送 HTML 表单）
        - `Blob/BufferSource` 发送二进制数据（可用于发送图片）
        - URLSearchParams，以 `x-www-form-unlencoded` 编码发送数据（很少使用）
    - `signal`：在“中止”一节中会提到
    - [其他参数](https://zh.javascript.info/fetch-api)（由于很少使用就不在这里介绍了）
    

    ??? example "例子"

        ``` js
        let user = {
            name: 'John',
            surname: 'Smith'
        };

        let response = await fetch('/article/fetch/post/user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(user)
        });

        let result = await response.json();
        alert(result.message);
        ```

- 获取响应的流程
    - 当服务器发送响应头(response header)时，`fetch` 返回的 promise 使用内建的 Response class 对象来解析响应头
        - 在该阶段，可以通过检查响应头来查看 HTTP 状态已确定请求是否成功、有没有响应体
        - 通过以下 response 的属性查看 HTTP 状态
            - `status`：HTTP 状态码
            - `ok`：布尔值，若状态码在 200-299 之间，则为 `true`
        ??? example "例子"

            ``` js
            let response = await fetch(url);

            if (response.ok) { // 如果 HTTP 状态码为 200-299
                // 获取 response body（此方法会在下面解释）
                let json = await response.json();
            } else {
                alert("HTTP-Error: " + response.status);
            }
            ```

    - 使用其他方法获取响应体(response body)，包括：
        - `response.text()`：以文本形式返回 response
        - `response.json()`：以 JSON 格式返回 response
        - `response.formData()`：以 `FormData` 对象的形式返回 response
        - `response.blob()`：以 Blob（带有类型的二进制数据）的形式返回 response
        - `response.arrayBuffer()`：以 ArrayBuffer（低级别的二进制数据）形式返回 response
        - `response.body`：ReadableStream 对象，允许逐块读取响应体（后面会介绍）
        >注意：对同一个 response 只能使用上述方法中的一种

- 响应头：位于 `response.headers` 中，是一个类似映射的 header 对象
``` js
let response = await fetch('https://www.example.com/haha');

// 获取一个 header
alert(response.headers.get('Content-Type')); 
// application/json; charset=utf-8

// 迭代所有 header
for (let [key, value] of response.headers) {
  alert(`${key} = ${value}`);
}
```

- FormData：用于发送 HTML 表单
    - 构造函数：
    ``` js
    let formData = new FormData([form]);
    // formData 是一个 FormData 对象
    // 如果提供了 HTML form 元素，它会自动捕获 form 元素字段
    ```

    - 相关方法
        - `formData.append(name, value[, filename])`：添加具有给定 `name` 和 `value` 的表单字段；可选参数 `filename` 用于设置文件名，此时该表单类似 `<input type="file">`
        - `formData.set(name, value)` / `formData.set(name, blob, filename)`：与上一种方法类似，但它确保只有一个 `name` 字段。所以如果原来有 `name` 字段就会被移除，并附加一个新的 `name` 字段
        - `formData.delete(name)`：移除 `name` 字段
        - `formData.get(name)`：获取 `name` 字段
        - `formData.has(name)`：若存在 `name` 字段，则返回 `true`，否则返回 `false` 
        - 使用 `for...of` 循环迭代 formData 字段
        ``` js
        let formData = new FormData();
        formData.append('key1', 'value1');
        formData.append('key2', 'value2');

        // 列出 key/value 对
        for(let [name, value] of formData) {
            alert(`${name} = ${value}`); // key1 = value1，然后是 key2 = value2
        }
        ```

    - 发送文件
    ``` html
    <form id="formElem">
        <input type="text" name="firstName" value="John">
        Picture: <input type="file" name="picture" accept="image/*">
        <input type="submit">
    </form>

    <script>
        formElem.onsubmit = async (e) => {
            e.preventDefault();

            let response = await fetch('/article/formdata/post/user-avatar', {
                method: 'POST',
                body: new FormData(formElem)
            });

            let result = await response.json();

            alert(result.message);
        };
    </script>
    ```

    - 可以将二进制数据作为表单的一部分发送
    ??? example "例子"

        ``` html
        <body style="margin:0">
            <canvas id="canvasElem" width="100" height="80" style="border:1px solid"></canvas>

            <input type="button" value="Submit" onclick="submit()">

            <script>
                canvasElem.onmousemove = function(e) {
                    let ctx = canvasElem.getContext('2d');
                    ctx.lineTo(e.clientX, e.clientY);
                    ctx.stroke();
                };

                async function submit() {
                    let imageBlob = await new Promise(resolve => canvasElem.toBlob(resolve, 'image/png'));

                    let formData = new FormData();
                    formData.append("firstName", "John");
                    formData.append("image", imageBlob, "image.png");

                    let response = await fetch('/article/formdata/post/image-form', {
                        method: 'POST',
                        body: formData
                    });
                    let result = await response.json();
                    alert(result.message);
                }

            </script>
        </body>
        ```

- 跟踪下载进度：使用 `response.body` 属性，它是一个 `ReadableStream` 对象，逐块(chunk)提供响应体
    ``` js hl_lines="8"
    // 流读取器(stream reader)
    const reader = response.body.getReader();

    // 在 body 下载时，一直为无限循环
    while(true) {
        // 当最后一块下载完成时，done 值为 true
        // value 是块字节的 Uint8Array
        const {done, value} = await reader.read();

        if (done) {
            break;
        }

        console.log(`Received ${value.length} bytes`)
    }
    ```

    - 循环接收响应块(response chunk)，直到加载完成（`done` 为 `true`）
    - 要打印进度，只需将每个接收到的片段 `value` 长度（`.length`）加到计数器上即可

    ??? example "更复杂的例子"

        ``` js
        // Step 1：启动 fetch，并获得一个 reader
        let response = await fetch('https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits?per_page=100');

        const reader = response.body.getReader();

        // Step 2：获得总长度（length）
        const contentLength = +response.headers.get('Content-Length');

        // Step 3：读取数据
        let receivedLength = 0; // 当前接收到了这么多字节
        let chunks = []; // 接收到的二进制块的数组（包括 body）
        while(true) {
            const {done, value} = await reader.read();

            if (done) {
                break;
            }

            chunks.push(value);
            receivedLength += value.length;

            console.log(`Received ${receivedLength} of ${contentLength}`)
        }

        // Step 4：将块连接到单个 Uint8Array
        let chunksAll = new Uint8Array(receivedLength); // (4.1)
        let position = 0;
        for(let chunk of chunks) {
            chunksAll.set(chunk, position); // (4.2)
            position += chunk.length;
        }

        // Step 5：解码成字符串
        let result = new TextDecoder("utf-8").decode(chunksAll);

        // 我们完成啦！
        let commits = JSON.parse(result);
        alert(commits[0].author.login);
        ```

- 中止(abort)：`AbortController` 内建对象可用于中止 `fetch`（也可以中止其他异步任务）
    - 创建控制器(controller)，它有单个方法 `abort()`，和单个属性 `signal`
        ``` js
        let controller = new AbortController();
        ```

        - 调用 `abort()` 时，`controller.signal` 就会触发 `abort` 事件，`controller.signal.aborted` 属性变为 `true`
    - 与 `fetch` 一起使用：使用 `fetch` 的可选参数 `signal`，它的值为 `AbortController` 的 `signal` 属性
        ``` js
        let controller = new AbortController();
        fetch(url, {
            signal: controller.signal
        });

        // 中止 fetch
        controller.abort();
        ```

        - 当 `fetch` 被中止时，它的 promise 就被 reject 了，并返回 `AbortError` 错误，需要用 `try...catch` 来处理
        ??? example "例子"

            ``` js
            // 1 秒后中止
            let controller = new AbortController();
            setTimeout(() => controller.abort(), 1000);

            try {
                let response = await fetch('/article/fetch-abort/demo/hang', {
                    signal: controller.signal
                });
            } catch(err) {
                if (err.name == 'AbortError') { // handle abort()
                    alert("Aborted!");
                } else {
                    throw err;
                }
            }
            ```
    - `AbortController` 的可伸缩(scalable)性：单个 `AbortController` 可以一次性取消多个 `fetch`，也可以同时取消我们自己设置的异步任务
    ??? example "例子"

        ``` js
        let urls = [...];
        let controller = new AbortController();

        let ourJob = new Promise((resolve, reject) => { // 我们的任务
            // ...
            controller.signal.addEventListener('abort', reject);
        });

        let fetchJobs = urls.map(url => fetch(url, { // fetches
            signal: controller.signal
        }));

        // 等待完成我们的任务和所有 fetch
        let results = await Promise.all([...fetchJobs, ourJob]);

        // controller.abort() 被从任何地方调用，
        // 它都将中止所有 fetch 和 ourJob
        ```

- 跨源请求
    - 回顾知识：[CORS（跨源资源共享）](../../security.md#cors)
    - 简单请求
    ??? example "例子"

        - 请求头
        ``` http
        GET /request
        Host: anywhere.com
        Origin: https://javascript.info
        ...
        ```

        - 响应头
        ``` http
        200 OK
        Content-Type:text/html; charset=UTF-8
        Access-Control-Allow-Origin: https://javascript.info
        ```

        <figure style=" width: 60%" markdown="span">
            ![](../images/js/33_dark.png#only-dark)
            ![](../images/js/33_light.png#only-light)
            <figcaption></figcaption>
        </figure>

    - 非简单请求

    <figure style=" width: 60%" markdown="span">
        ![](../images/js/34_dark.png#only-dark)
        ![](../images/js/34_light.png#only-light)
        <figcaption></figcaption>
    </figure>

### URL 对象

 URL 对象可以用来替代 `fetch` 或 `XMLHttpRequest` 中的 URL 字符串。虽然稍微麻烦些，但是有时它比字符串形式更加有用。

- 创建 URL 对象
    ``` js
    let url = new URL(url[, base]);
    ```

    - 如果只有一个参数，那么 `url` 应为完整的 URL 字符串
    - 如果有两个参数，那么 `base` 为基础 URL（字符串或 URL 对象），`url` 为该 URL 的路径（字符串）
    ``` js
    // 这两个 URL 是一样的
    let url1 = new URL('https://javascript.info/profile/admin');
    let url2 = new URL('/profile/admin', 'https://javascript.info');
    ```

- URL 对象的一些属性：

    <figure style=" width: 70%" markdown="span">
        ![](../images/js/35_dark.png#only-dark)
        ![](../images/js/35_light.png#only-light)
        <figcaption></figcaption>
    </figure>

    - `.href`：完整的 URL，同 `url.toString()`
    - `.protocol`：协议，以冒号结尾
    - `.search`：以问号 `?` 开头的一系列参数
    - `.hash`：以 `#` 开头的字符串
    - 若有 HTTP 身份验证，则可能还有 `.user` 和 `.password` 属性（很少用）
    - `url.searchParams`：一种 URLSearchParams 类型的对象，与搜索参数相关，有以下几种方法：
        - `append(name, value)`：添加
        - `delete(name)`：移除
        - `get(name)`：获取
        - `getAll(name)`：获取相同名称的所有参数
        - `has(name)`：检查是否存在
        - `set(name, value)`：添加/移除原参数后再添加
        - `sort()`：按名称对参数排序（很少使用）
        - 可迭代，类似映射
        - 参数中的特殊字符（`!`、`:` 等）会被转换为 UTF-8 编码，以百分号开头
- 编/解码 URL 的内建函数
    - `encodeURI`：仅编码 URL 中完全禁止的字符
    - `decodeURI`：解码，回到之前的状态
    - `encodeURIComponent`：在 `encodeURI` 的基础上，还编码 `#`、`$`、`&`、`+`、`,`、`/`、`:`、`;`、`=`、`?`、`@` 字符，更适用于带搜索参数的 URL
    - `decodeURIComponent`：解码，回到之前的状态
 
### XMLHttpRequest

`XMLHttpRequest` 是一个内建的浏览器对象，允许使用 JS 发送 HTTP 请求。


- 发送请求的流程：
    - 创建对象
    ``` js
    // 该构造函数没有参数
    let xhr = new XMLHttpRequest();
    ```

    - 初始化（紧跟构造函数之后）
        ``` js
        xhr.open(method, URL[, async, user, password]);
        ```

        - `method`：HTTP 方法，通常是 `"GET"` 或 `"POST"`
        - `URL`：要请求的 URL（字符串/URL 对象）
        - `async`：（可选）如果值为 `false`，则变成同步请求（此时 JS 执行到 `send()` 处时会暂停，接收到响应后恢复执行，很少使用），否则是异步请求（默认）
        - `user`，`password`：HTTP 身份验证的登录名和密码
    - 发送请求
    ``` js
    xhr.send([body])
    // 可选参数 body 包含了请求体
    ```

    - 监听 `xhr` 事件并获取响应，有以下常用事件：
        - `load`：请求完成（即使状态码为 400、500 之类的）且响应已完全下载
        - `error`：无法发出请求（比如网络中断或访问无效的 URL）
        - `progress`：在下载响应期间定期触发，报告下载进度
        ``` js
        xhr.onload = function() {
            alert(`Loaded: ${xhr.status} ${xhr.response}`);
        };

        xhr.onerror = function() { // 仅在根本无法发出请求时触发
            alert(`Network Error`);
        };

        xhr.onprogress = function(event) { // 定期触发
            // event.loaded —— 已经下载了多少字节
            // event.lengthComputable = true，当服务器发送了 Content-Length header 时
            // event.total —— 总字节数（如果 lengthComputable 为 true）
            alert(`Received ${event.loaded} of ${event.total}`);
        };
        ```
    ??? example "例子"

        从服务器加载某个 URL 并打印加载进度

        ``` js
        // 1. 创建一个 new XMLHttpRequest 对象
        let xhr = new XMLHttpRequest();

        // 2. 配置它：从 URL /article/.../load GET-request
        xhr.open('GET', '/article/xmlhttprequest/example/load');

        // 3. 通过网络发送请求
        xhr.send();

        // 4. 当接收到响应后，将调用此函数
        xhr.onload = function() {
            if (xhr.status != 200) { // 分析响应的 HTTP 状态
                alert(`Error ${xhr.status}: ${xhr.statusText}`); // 例如 404: Not Found
            } else { // 显示结果
                alert(`Done, got ${xhr.response.length} bytes`); // response 是服务器响应
            }
        };

        xhr.onprogress = function(event) {
        if (event.lengthComputable) {
            alert(`Received ${event.loaded} of ${event.total} bytes`);
        } else {
            alert(`Received ${event.loaded} bytes`); // 没有 Content-Length
        }

        };

        xhr.onerror = function() {
            alert("Request failed");
        };
        ```
- 相关属性
    - `status`：HTTP 状态码（数字），若出现非 HTTP 错误则为 `0`
    - `statusText`：HTTP 状态消息（字符串）（比如 `200` 对应为 `OK`，`404` 对应 `Not Found`、`403` 对应 `Forbidden`）
    - `response`：服务器响应体
    - `timeout`：指定最大超时时间，如果在给定时间内未执行成功，则取消请求并触发 `timeout` 事件
    - `responseType`：设置响应格式
        - `""`（默认）、`"text"`：字符串
        - `"arraybuffer"`：`ArrayBuffer`
        - `"blob"`：`Blob`
        - `"document"`：XML document 或 HTML document
        - `"json"`：JSON
        ??? example "例子"

            ``` js
            let xhr = new XMLHttpRequest();

            xhr.open('GET', '/article/xmlhttprequest/example/json');

            xhr.responseType = 'json';

            xhr.send();

            // 响应为 {"message": "Hello, world!"}
            xhr.onload = function() {
                let responseObj = xhr.response;
                alert(responseObj.message); // Hello, world!
            };
            ```

    - `readyState`：获取 `XMLHttpRequest` 的当前状态，有以下几种状态：
        ``` js
        UNSENT = 0;            // 初始状态
        OPENED = 1;            // 调用 open()
        HEADERS_RECEIVED = 2;  // 接收到响应头
        LOADING = 3;           // 加载响应（接收数据包）
        DONE = 4;              // 请求完成
        // 0 -> 1 -> 2 -> 3 -> ... -> 3 -> 4
        ```

        - 可以使用 `readystatechange` 事件来跟踪状态：
        ``` js
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 3) {
                // 加载中
            }
            if (xhr.readyState == 4) {
                // 请求完成
            }
        };
        ```

    - `upload`：跟踪数据上传进度，它会在上传时生成以下事件：
        - `loadstart`：上传开始
        - `progress`：上传期间定期触发
        - `abort`：上传中止
        - `error`：非 HTTP 错误
        - `load`：上传成功完成
        - `timeout`：上传超时（若设置了 `timeout` 属性）
        - `loadend`：上传完成（无论成功与否）
    ??? example "例子"

    ``` html
    <input type="file" onchange="upload(this.files[0])">

    <script>
        function upload(file) {
            let xhr = new XMLHttpRequest();

            // 跟踪上传进度
            xhr.upload.onprogress = function(event) {
                console.log(`Uploaded ${event.loaded} of ${event.total}`);
            };

            // 跟踪完成：无论成功与否
            xhr.onloadend = function() {
                if (xhr.status == 200) {
                console.log("success");
                } else {
                console.log("error " + this.status);
                }
            };

            xhr.open("POST", "/article/xmlhttprequest/post/upload");
            xhr.send(file);
        }
    </script>
    ```

    - `withCredentials`：若值为 `true`，则将 cookie 和 HTTP 授权发送到其他域（默认禁止），实现跨源请求
    

- 中止请求：`xhr.abort()`，触发 `abort` 事件，使 `xhr.status` 变为 `0`
- 关于 HTTP 头的方法
    - `setRequestHeader(name, value)`：设置请求头的某个字段，比如：
        ``` js
        xhr.setRequestHeader('Content-Type', 'application/json');
        ```

        - 一旦用该方法设置字段，该字段便无法被撤销，也不能被覆写
    - `getResponseHeader(name)`：获取指定的头字段
    - `getAllResponseHeaders`：获取所有响应头字段，返回形式如下，每行以 `"\r\n"` 结尾（不依赖于操作系统）
    ``` http
    Cache-Control: max-age=31536000
    Content-Length: 4260
    Content-Type: image/png
    Date: Sat, 08 Sep 2012 16:53:16 GMT
    ```

    >注：不包括 `Set-Cookie` 和 `Set-Cookie2` 头字段

- 关于 POST 请求：创建 FormData 对象（前面介绍过），在 `xhr.open()` 中使用 `'POST'` 参数，并用 `xhr.send(formData)` 发送表单到服务器

??? example "例子"

    ``` html
    <form name="person">
        <input name="name" value="John">
        <input name="surname" value="Smith">
    </form>

    <script>
        // 从表单预填充 FormData
        let formData = new FormData(document.forms.person);

        // 附加一个字段
        formData.append("middle", "Lee");

        // 将其发送出去
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/article/xmlhttprequest/post/user");
        xhr.send(formData);

        xhr.onload = () => alert(xhr.response);
    </script>
    ```