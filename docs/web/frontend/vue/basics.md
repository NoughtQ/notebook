---
counter: true
---


# Vue 基础部分

!!! info "注"

    这是我第一次学习 Vue，虽然官方推荐新手先学选项式API，但从个人偏好上来说我还是更倾向于组合式API，因为选项式API那种面向对象的风格看起来略显臃肿，而组合式API做同样的工作只需几句话就搞定了。所以我目前先从**组合式API**开始学习，笔记呈现的代码都是组合式API风格，之后有时间的话会补充选项式API的内容。

## 简介

Vue的定义（摘自官方文档）：

>Vue (发音为 /vjuː/，类似 view) 是一款用于构建用户界面的 **JavaScript 框架**。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套**声明式的、组件化的编程模型**，帮助你高效地开发用户界面。无论是简单还是复杂的界面，Vue 都可以胜任。

核心功能：

- **声明式渲染**：Vue 基于标准 HTML 拓展了一套模板语法，使得我们可以声明式地描述最终输出的 HTML 和 JavaScript 状态之间的关系
- **响应性**：Vue 会自动跟踪 JavaScript 状态并在其发生变化时响应式地更新 DOM

**单文件组件**(single-file components, SFC)：将一个组件的逻辑(JavaScript)，模板(HTML)和样式(CSS)封装在同一个文件里。

??? code "代码示例"

    ```html
    <script setup>
        import { ref } from 'vue'
        const count = ref(0)
    </script>

    <template>
        <button @click="count++">Count is: {{ count }}</button>
    </template>

    <style scoped>
        button {
            font-weight: bold;
        }
    </style>
    ```

API风格：

- **选项式API**(options API)：用包含多个选项的**对象**来描述组件的逻辑，例如`data`、`methods`和`mounted`。选项所定义的属性都会暴露在函数内部的`this`上，它会指向当前的组件实例。
    - 核心思想：**组件实例**(即上述例子中的 this)。对于有**面向对象语言**背景的用户来说，这通常与基于类的模型更为一致。同时，它将**响应性**相关的细节抽象出来，并强制按照选项来组织代码，从而对初学者而言更为友好。
    - 适用场合：不需要使用构建工具，或者打算主要在低复杂度的场景中使用 Vue，例如渐进增强的应用场景。

- **组合式API**(composition API)：使用导入的 **API 函数**来描述组件逻辑。
    - 在单文件组件中，组合式 API 通常会与`<script setup>`搭配使用。这个`setup`属性是一个标识，告诉 Vue 需要在编译时进行一些处理，让我们可以更简洁地使用组合式 API。比如`<script setup>`中的导入和顶层变量/函数都能够在模板中直接使用。
    - 核心思想：直接在**函数**作用域内定义响应式状态变量，并将从多个函数中得到的状态组合起来处理复杂问题。这种形式更加自由，也需要你对 Vue 的响应式系统有更深的理解才能高效使用。相应的，它的**灵活性**也使得组织和重用逻辑的模式变得更加强大。
    - 适用场合：用 Vue 构建完整的单页应用（同时配合单文件组件）

## 创建 Vue 应用

### 操作步骤

>默认使用`npm`安装 Vue。

1. 在项目目录下执行以下命令：

    ```sh
    $ npm create vue@latest

    ...
    ✔ Project name: … <your-project-name>
    ✔ Add TypeScript? … No / Yes
    ✔ Add JSX Support? … No / Yes
    ✔ Add Vue Router for Single Page Application development? … No / Yes
    ✔ Add Pinia for state management? … No / Yes
    ✔ Add Vitest for Unit testing? … No / Yes
    ✔ Add an End-to-End Testing Solution? … No / Cypress / Nightwatch / Playwright
    ✔ Add ESLint for code quality? … No / Yes
    ✔ Add Prettier for code formatting? … No / Yes
    ✔ Add Vue DevTools 7 extension for debugging? (experimental) … No / Yes

    Scaffolding project in ./<your-project-name>...
    Done.
    ```

    执行指令后会跳出一系列的可选功能提示，如果不确定是否要开启某个功能，可以直接敲回车（默认为 No）。

2. 执行以下命令来安装依赖并启动开发服务器：

    ```sh
    $ cd <your-project-name>
    $ npm install
    $ npm run dev

    > vue-project@0.0.0 dev
    > vite

    ➜  Local: http://localhost:5173/
    __devtools__/ as a separate window
    ➜  Vue DevTools: Press Alt(⌥)+Shift(⇧)+D in App to toggle the Vue DevTools

    ➜  press h + enter to show help
    ```

    现在这个Vue项目已经运行起来了。

3. 执行以下命令将应用发布到生产环境：

    ```sh
    $ npm run build
    ```

    此命令会在`./dist`目录中为Vue应用创建一个生产环境的构建版本。

### 应用实例

每个 Vue 应用都是通过`createApp()`函数创建一个新的**应用实例**：

```js
import { createApp } from 'vue'

const app = createApp({
  /* 根组件选项 */
})
```

- 传入`createApp()`的对象实际上是一个**组件**，每个应用都需要一个“**根组件**”，其他组件将作为其子组件。
- 从其他文件导入根组件：

    ```js
    import { createApp } from 'vue'
    // 从一个单文件组件中导入根组件
    import App from './App.vue'
    const app = createApp(App)
    ```

- 大多数真实的应用都是由一棵嵌套的、可重用的**组件树**组成的（个人看法是：每个组件代表的是一个子功能，最底层的组件应当完成的是最基本的、不可分割的功能）

- **挂载应用**：应用实例必须在调用了`.mount()`方法后才会渲染出来
- 该方法应始终在整个应用配置和资源注册完成后被调用
- 它接收一个**“容器”参数**，可以是一个实际的 **DOM 元素**或是一个 **CSS 选择器字符串**
- 返回值是**根组件实例**而非应用实例
- 应用根组件的内容将会被渲染在容器元素里面，但**容器元素**自己将**不会**被视为应用的一部分
- **根组件的模板**通常是组件本身的一部分，但也可以直接通过在挂载容器内编写模板来单独提供
    - 当根组件没有设置 template 选项时，Vue 将自动使用容器的 innerHTML 作为模板

- **应用配置**：
    - 应用实例通过`.config`对象允许我们配置一些**应用级**的选项
        - 例子：应用级的错误处理器，用来捕获所有子组件上的错误

        ```js
        app.config.errorHandler = (err) => {
        /* 处理错误 */
        }
        ```

    - 应用实例还提供了一些用于注册（个人理解为“创建”）应用范围内（个人理解为“全局范围”）可用的资源的方法
        - 例子：注册组件

        ```js
        app.component('TodoDeleteButton', TodoDeleteButton)
        ```

- 同一个页面可以创建多个共存的Vue应用，而且每个应用都拥有自己的用于配置和全局资源的作用域

    ```js
    const app1 = createApp({
    /* ... */
    })
    app1.mount('#container-1')

    const app2 = createApp({
    /* ... */
    })
    app2.mount('#container-2')
    ```

    - 如果正在使用 Vue 来增强服务端渲染 HTML，并且只想要 Vue 去控制一个大型页面中特殊的一小部分，应避免将一个单独的 Vue 应用实例挂载到整个页面上，而是应该创建多个小的应用实例，将它们分别挂载到所需的元素上去。

## 模板语法

- Vue 使用一种**基于 HTML 的模板语法**，能够声明式地将组件实例的**数据绑定**到 DOM 上。所有的 Vue 模板都是语法层面合法的 HTML，可以被符合规范的浏览器和 HTML 解析器解析。
- 在底层机制中，Vue 会将模板**编译成高度优化的 JS 代码**。结合响应式系统，当应用状态变更时，Vue 能够智能地推导出需要重新渲染的组件的最少数量，并应用最少的 DOM 操作。

### 数据绑定

下面介绍各种数据绑定的形式：

- 文本插值：使用的是“Mustache”语法 (即**双大括号**)

    ```html
    <span>Message: {{ msg }}</span>
    <!-- 双大括号标签会被替换为相应组件实例中 msg 属性的值。 -->
    <!-- 同时每次 msg 属性更改时它也会同步更新。 -->
    ```

    - 此时双大括号会将数据解释为纯文本，而不是 HTML

- 插入原始 HTML：使用 `v-html` 指令（由 Vue 提供的一种特殊的 HTML 属性），在当前组件实例上，将此元素的 innerHTML 与指定的属性（这里指 `v-html` 的值）对应保持同步。

    ???+ example "例子"

        ```html
        <p>Using text interpolation: {{ rawHtml }}</p>
        <p>Using v-html directive: <span v-html="rawHtml"></span></p>
        ```

        结果：

        <figure style=" width: 60%" markdown="span">
            ![](../images/vue/1_dark.png#only-dark)
            ![](../images/vue/1_light.png#only-light)
            <figcaption></figcaption>
        </figure>

    - 此时插入的内容为纯HTML，因此数据绑定将会被忽略
    - 不能用`v-html`来拼接组合模板
    
    !!! warning "安全警告"
    
        在网站上动态渲染任意 HTML 是非常危险的，因为这非常容易造成[XSS 漏洞](https://en.wikipedia.org/wiki/Cross-site_scripting)。请仅在内容安全可信时再使用 v-html，并且永远不要使用用户提供的 HTML 内容。

- HTML 属性(attributes)绑定：使用 `v-bind` 指令实现响应式地绑定 HTML 属性

    ```html
    <div v-bind:attr="dynamicAttr"></div>
    ```
    `v-bind` 指令指示 Vue 将 HTML 元素的 `attr` 属性与组件的 `dynamicAttr` 属性保持一致。

    - 如果绑定的值是 `null` 或者 `undefined`，那么该属性将会从渲染的元素上移除
    - 简写：`v-bind:attr` 可以简记为 `:attr`，所有支持 Vue 的浏览器都能正确解析它，此外，它们不会出现在最终渲染的 DOM 中
    - 同名简写：如果 HTML 属性名称与绑定的 JS 值的名称相同，那么可以进一步简化语法，省略 HTML 属性值，即：

    ```html
    <div v-bind:attr></div>
    <!-- 等价于 <div v-bind:attr="attr"></div> -->
    ```

    - 绑定多个值：利用JS对象可以同时为一个HTML元素的多个HTML属性绑定对应的JS值，此时 `v-bind` 无需带参数

    ???+ example "例子"

        ```js
        const objectOfAttrs = {
            id: 'container',
            class: 'wrapper',
            style: 'background-color:green'
        }
        ```

        ```html
        <div v-bind="objectOfAttrs"></div>
        ```


- JS 表达式：可用于文本插值（双大括号）中以及任何以`v-`开头的 HTML 属性（即 Vue 指令）中

    ```html
    {{ number + 1 }}

    {{ ok ? 'YES' : 'NO' }}

    {{ message.split('').reverse().join('') }}

    <div :id="`list-${id}`"></div>
    ```

    - 需要注意的是，每个绑定仅支持**单一的表达式**，不支持完整的一条 JS 语句
    - **函数/方法调用**也算一种表达式，但需要注意的是：绑定在表达式中的函数/方法在组件每次更新时都会被重新调用，因此**不应该产生任何副作用**，比如改变数据或触发异步操作。
    - 模板中的表达式只能进行受限的全局访问，即仅能够访问[有限的全局对象列表](https://github.com/vuejs/core/blob/main/packages/shared/src/globalsAllowList.ts#L3)中的对象
    - **计算属性**：如果 JS 表达式过于复杂臃肿，此时推荐使用计算属性来描述依赖响应式状态的复杂逻辑。
        - 它的值是一个方法，接收一个 getter 函数，返回值为一个计算属性 [ref](#ref())。可以用 `.value` 访问计算结果，在模板中它也会自动解包。
            - getter 不应有副作用（包括改变其他状态、在 getter 中做异步请求或者更改 DOM）

        ??? example "例子"

            ```html
            <script setup>
                import { reactive, computed } from 'vue'

                const author = reactive({
                    name: 'John Doe',
                    books: [
                        'Vue 2 - Advanced Guide',
                        'Vue 3 - Basic Guide',
                        'Vue 4 - The Mystery'
                    ]
                })

                // 一个计算属性 ref
                const publishedBooksMessage = computed(() => {
                    return author.books.length > 0 ? 'Yes' : 'No'
                })
            </script>

            <template>
                <p>Has published books:</p>
                <span>{{ publishedBooksMessage }}</span>
            </template>
            ```

    - 计算属性会自动追踪响应式依赖，因此可以做到同步更新。
    - 直接调用函数也可以呈现出同样的效果，但不同之处在于**计算属性值会基于其响应式依赖被缓存**，这意味着只要依赖值不改变，无论多少次访问计算属性都会立即返回先前的计算结果，无需重复计算。
    - 计算属性默认**只读**，因此避免直接修改计算属性值。要想修改计算属性，需要在创建时同时提供 getter 和 setter。

### 指令

**指令**(directives)是带有 `v-` 前缀的特殊 HTML 属性，它们一般接收的值为一个 **JS 表达式**。一个指令的任务是在其表达式的值变化时响应式地更新 DOM。

- 参数(arguments)：指令名与参数之间用冒号隔开
    - 前面提到的“简写”：可以仅保留冒号和参数，省略指令名；有些指令还有特殊的简写规则，比如 `v-on` 可以简写为 `@`
    - 参数可以是 HTML 属性、DOM 事件等
    - 参数可以是**动态**的——使用 JS 表达式作为参数，但需要额外用方括号包起来

        ```html
        <a v-bind:[attributeName]="url"> ... </a>
        <a v-on:[eventName]="doSomething"> ... </a>
        ```

        - 限制：
            - 动态参数中表达式的值应当是一个字符串，或者是`null`（用于显式移除该绑定）
            - 且字符串内不应出现空格、引号等非法的 HTML 属性名字符
            - 避免使用大写字母，因为浏览器会强制将其转化为小写


- 修饰符(modifiers)：以点开头的特殊后缀，表明指令需要以一些特殊的方式被绑定


!!! note "总结"

    <div style="text-align: center">
        <image src="../images/vue/2.png" width=80%>
    </div>


相关资料：所有 Vue 的[内置指令](https://cn.vuejs.org/api/built-in-directives)

### 类与样式绑定


- 类(class)
    - 对象
        - 使用`:class`(`v-bind:class`的缩写)传递 ref 值以改变 HTML 的 `class` 属性，可以在对象中写多个字段来操作多个类
        - `:class` 与 `class` 可以共存

        ??? example "例子"

            ```js
            const isActive = ref(true)
            const hasError = ref(false)
            ```

            ```html
            <div
                class="static"
                :class="{ active: isActive, 'text-danger': hasError }"
            ></div>
            ```

            渲染结果：

            ```html
            <div class="static active"></div>
            ```


        - 也可以绑定 reactive 对象、或者返回对象的**计算属性**

        ??? example "例子"

            ```js
            const isActive = ref(true)
            const error = ref(null)

            const classObject = computed(() => ({
                active: isActive.value && !error.value,
                'text-danger': error.value && error.value.type === 'fatal'
            }))
            ```

            ```html
            <div :class="classObject"></div>
            ```


    - 数组：每个元素对应一个类，用于同时渲染多个CSS类

    ```js
    const activeClass = ref('active')
    const errorClass = ref('text-danger')
    ```

    ```html
    <div :class="[activeClass, errorClass]"></div>
    ```

    - 在组件上使用（由于还没学到组件，暂时跳过）

- 样式(style)
    - 对象：使用 `:style` 绑定 JS 对象值（ref 值或 reactive 对象），对应 HTML 的 `style` 属性

    === "ref 值"

        ```js
        const activeColor = ref('red')
        const fontSize = ref(30)
        ```

        ```html
        <div :style="{ color: activeColor, fontSize: fontSize + 'px' }"></div>
        ```

    === "reactive 对象"

        ```js
        const styleObject = reactive({
            color: 'red',
            fontSize: '30px'
        })
        ```

        ```html
        <div :style="styleObject"></div>
        ```

    - 数组：包含多个样式对象，这些对象被合并起来，并渲染到同一元素上

    ```html
    <div :style="[baseStyles, overridingStyles]"></div>
    ```

    - 样式多值：可以对一个样式属性提供多个 (不同前缀的) 值，数组仅会渲染浏览器支持的最后一个值

### 条件渲染

基本指令有：

- `v-if`
- `v-else-if`
- `v-else`

除`v-else`外，其余两个指令的后面跟一个字符串作为判断条件。它们的作用同一般编程语言中的`if-else`语句，看完下面的例子就知道怎么用了：

```html
<div v-if="type === 'A'">
  A
</div>
<div v-else-if="type === 'B'">
  B
</div>
<div v-else-if="type === 'C'">
  C
</div>
<div v-else>
  Not A/B/C
</div>
```

如果希望某个分支内包含多个元素（由于上面的指令依附于某个元素，因此只能控制单个元素的内容），那么就需要在`<template>`元素上使用上述的几个指令，注意最后的渲染结果并不会包含这个`<template>`元素。

```html
<template v-if="ok">
  <h1>Title</h1>
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
</template>
```

`v-show`是另一种按条件显示元素的指令，格式与`v-if`相同，不同之处在于：

- `v-show`会在 DOM 渲染中保留该元素，它仅切换了该元素上名为 `display` 的 CSS 属性
- `v-show` 不支持在 `<template>` 元素上使用，也不能和 `v-else` 搭配使用
- 使用`v-show`时，元素无论初始条件如何，始终会被渲染，因此有更高的初始渲染开销；而`v-if`是惰性的，只有当条件首次变为`true`时才能渲染元素，因此具备更高的切换开销
    - 因此，如果需要频繁切换，则使用`v-show`较好；如果在运行时绑定条件很少改变，则`v-if`会更合适


### 列表渲染

列表渲染用到的指令为`v-for`

- 语法：`v-for="(item, index) in items"`
    - `item`：迭代项的别名
    - `items`：定义在JS脚本中的
        - **数组**：此时遍历的是数组的每个元素
            - `index`：（可选的第二个参数）对应的索引
        - **对象**：此时遍历的是对象的每个属性值
            - `key`：（可选的第二个参数）对应的属性名
            - `index`：（可选的第三个参数）对应的索引         
        - **数值**：若数值为n，则遍历1~n之间的正数

    - `in`可以被`of`替代

- `v-for`块中可以完整地访问父作用域内的属性和变量

??? example "例子"

    ```js
    const parentMessage = ref('Parent')
    const items = ref([{ message: 'Foo' }, { message: 'Bar' }])
    ```

    ```html
    <li v-for="(item, index) in items">
        {{ parentMessage }} - {{ index }} - {{ item.message }}
    </li>
    ```

    结果：

    - Parent - 0 - Foo
    - Parent - 1 - Bar

- 可嵌套，每个`v-for`作用域都可以访问到父级作用域
- 与`v-if`类似，可以在`<template>`上使用`v-for`指令来宣汉一个包含多个元素的块

```html
<ul>
  <template v-for="item in items">
    <li>{{ item.msg }}</li>
    <li class="divider" role="presentation"></li>
  </template>
</ul>
```

- 当`v-if`和`v-for`同时作用于一个元素上的时候，`v-if`会首先被执行

    ??? example "例子"

        ```html
        <!--
        这会抛出一个错误，因为属性 todo 此时
        没有在该实例上定义
        -->
        <li v-for="todo in todos" v-if="!todo.isComplete">
        {{ todo.name }}
        </li>
        ```

        在外先包装一层`<template>`再在其上使用`v-for`可以解决这个问题 (这也更加明显易读)：

        ```html
        <template v-for="todo in todos">
        <li v-if="!todo.isComplete">
            {{ todo.name }}
        </li>
        </template>
        ```

    !!! warning "警告"

        因为`v-if`和`v-for`的优先级不明显，所以不推荐同时使用这两者。

- 默认情况下，当数据项的顺序改变时，Vue 不会随之移动 DOM 元素的顺序，而是**就地更新**每个元素，确保它们在原本指定的索引位置上渲染
    - 要想实现对元素的重新排序，需要使用一个名为`:key`的HTML属性，它的值为应当是能够唯一表示某个数据项的属性（字符串或数值类型）

    ```html
    <div v-for="item in items" :key="item.id">
    <!-- 内容 -->
    </div>
    ```

- Vue 能够侦听响应式数组的[变更方法](../js/basic.md#数组)，并在它们被调用时触发相关的更新
    - 有些方法不会更改原数组，而是返回一个新数组，这时需要将旧数组替换为新数组


### 表单输入绑定

`v-model`指令：用于绑定表单的输入值，分为以下几类情况：

- `<input>`和`<textarea>`（文本类型）：`v-model`绑定`value`属性，且侦听`input`事件
- `<input type="checkbox">`和`<input type="radio">`：`v-model`绑定`checked`属性，且侦听`change`事件
- `<select>`：`v-model`绑定`value`属性，且侦听`change`事件

注意：

- 默认情况下，`v-model`绑定的值是静态的字符串/布尔值（复选框）
- `v-model`会忽略任何表单元素上初始的`value`、`checked`或`selected`属性，它将始终将当前绑定的JS状态视为数据的正确来源

??? example "例子"

    === "文本"

        ```html
        <p>Message is: {{ message }}</p>
        <input v-model="message" placeholder="edit me" />
        ```

    === "多行文本"

        ```html
        <span>Multiline message is:</span>
        <p style="white-space: pre-line;">{{ message }}</p>
        <textarea v-model="message" placeholder="add multiple lines"></textarea>
        ```

        注意：`<textarea>`不支持插值表达式（即用双大括号引用JS变量），需要用`v-model`替代

        ```html
        <!-- 错误 -->
        <textarea>{{ text }}</textarea>

        <!-- 正确 -->
        <textarea v-model="text"></textarea>
        ```


    === "复选框"

        ```js
        const checkedNames = ref([])
        ```

        ```html
        <div>Checked names: {{ checkedNames }}</div>

        <input type="checkbox" id="jack" value="Jack" v-model="checkedNames" />
        <label for="jack">Jack</label>

        <input type="checkbox" id="john" value="John" v-model="checkedNames" />
        <label for="john">John</label>

        <input type="checkbox" id="mike" value="Mike" v-model="checkedNames" />
        <label for="mike">Mike</label>
        ```

    === "单选按钮"

        ```html
        <div>Picked: {{ picked }}</div>

        <input type="radio" id="one" value="One" v-model="picked" />
        <label for="one">One</label>

        <input type="radio" id="two" value="Two" v-model="picked" />
        <label for="two">Two</label>
        ```

    === "选择器"

        - 单选：

            ```html
            <div>Selected: {{ selected }}</div>

            <select v-model="selected">
                <option disabled value="">Please select one</option>
                <option>A</option>
                <option>B</option>
                <option>C</option>
            </select>
            ```

        - 多选：

            ```html
            <div>Selected: {{ selected }}</div>

            <select v-model="selected" multiple>
                <option>A</option>
                <option>B</option>
                <option>C</option>
            </select>
            ```
---
我们可以使用`v-bind`将设定值绑定到当前组件实例上的动态数据，且该数据可以是非字符串类型的。

- 复选框：使用`:true-value`和`:false-value`属性设置动态值，当选中时会绑定`:true-value`上的值，否则绑定`:false-value`上的值

    ```html
    <input
        type="checkbox"
        v-model="toggle"
        :true-value="dynamicTrueValue"
        :false-value="dynamicFalseValue" />
    ```

- 单选按钮：使用`:value`属性设置动态值（被选中时绑定该值）

    ```html
    <input type="radio" v-model="pick" :value="first" />
    <input type="radio" v-model="pick" :value="second" />
    ```

- 选择器选项：使用`:value`属性设置动态值（被选中时绑定该值）

    ```html
    <select v-model="selected">
        <!-- 内联对象字面量 -->
        <option :value="{ number: 123 }">123</option>
    </select>
    ```

---
`v-model`的修饰符：

- `.lazy`：使`v-model`在每次发生`change`事件后更新数据（默认为在发生`input`事件后更新数据）
- `.number`：将输入内容自动转化为数字
    - 此时`<input>`元素的`type="number"`自动启用
- `.trim`：自动去除输入内容中两端的空格

## 响应式基础

### 声明响应式状态

#### ref()

使用`ref()`函数声明响应式状态，它接收参数，返回一个带有 `.value` 属性的 ref 对象，其值为传入的参数值：

```js
import { ref } from 'vue'

const count = ref(0)

console.log(count) // { value: 0 }
console.log(count.value) // 0

count.value++
console.log(count.value) // 1
```

- 在**组件模板**中访问 ref：在 `setup()` 函数中声明并返回它们：

    ```js hl_lines="5 9-11"
    import { ref } from 'vue'

    export default {
    // `setup` 是一个特殊的钩子，专门用于组合式 API。
        setup() {
            const count = ref(0)

            // 将 ref 暴露给模板
            return {
                count
            }
        }
    }
    ```

    ```html
    <div>{{ count }}</div>
    ```

    - 注意：在模板中使用 ref 时，由于 ref 会自动解包，因此**不需要**附加 `.value`
    - 可以直接在事件监听器中改变 ref 值

    ```html
    <button @click="count++">
        {{ count }}
    </button>
    ```

    - 对于更复杂的逻辑，可以在同一作用域内声明**更改 ref 的函数**，并将它们作为方法与状态一起公开，然后将该方法作为事件监听器

    ??? example "例子"

        ```js
        import { ref } from 'vue'

        export default {
            setup() {
                const count = ref(0)

                function increment() {
                    // 在 JavaScript 中需要 .value
                    count.value++
                }

                // 不要忘记同时暴露 increment 函数
                return {
                    count,
                    increment
                }
            }
        }
        ```


        ```html
        <button @click="increment">
            {{ count }}
        </button>
        ```

- 在 `setup()` 函数中手动暴露大量的状态和方法非常繁琐，但可以通过使用**单文件组件**(SFC)来避免这种情况——使用 `<script setup>` 来大幅度地简化代码

    ??? example "例子"

        ```html
        <script setup>
            import { ref } from 'vue'

            const count = ref(0)

            function increment() {
                count.value++
            }
        </script>

        <template>
            <button @click="increment">
                {{ count }}
            </button>
        </template>
        ```

    - `<script setup>` 中的顶层的导入、声明的变量和函数可在同一组件的模板中直接使用

- 使用 ref 的原因：
    - 在标准的 JS 中，检测普通变量的访问或修改是行不通的；
    - 而 ref 的 `.value` 属性提供了检测 ref 何时被访问或修改的机会。当一个组件首次渲染时，Vue 会**追踪**(track)在渲染过程中使用的每一个 ref。然后，当一个 ref 被修改时，它会**触发**(trigger)追踪它的组件的一次重新渲染。
    - 另一个好处是，与普通变量不同， ref 可以在被传递给函数的同时保留对最新值和响应式连接的访问。

- ref 具有**深层响应性**，即使改变嵌套对象或数组（它们作为 ref 的值）时，变化也会被检测到。
    - 也可以通过 `shallowRef()` 来放弃深层响应性

- DOM 更新时机：响应式状态被修改时，DOM 会被自动更新。但更新不是同步的，Vue 会在“next tick”更新周期中缓冲所有状态的修改，以确保不管进行了多少次状态修改，每个组件都只会被更新一次。

#### reactive()

`reactive()` 是另一种声明响应式状态的方式，与 `ref()` 不同的是，将使**对象**本身具有响应性：

```js
import { reactive } from 'vue'

const state = reactive({ count: 0 })
```

```html
<button @click="state.count++">
    {{ state.count }}
</button>
```

- Vue 能够拦截对响应式对象所有属性的访问和修改，以便进行依赖追踪和触发更新
- `reactive()` 也具备深层响应性：当访问嵌套对象时，它们也会被 `reactive()` 包装
    - 可以使用 `shallowReactive()` API 可以选择退出深层响应性

- 局限性：
    - 有限的值类型：它只能用于**对象类型** (对象、数组和如 `Map`、`Set` 这样的集合类型)。它不能持有如 `string`、`number` 或 `boolean` 这样的原始类型
    - 不能替换整个对象，否则会丢失对原对象引用的响应式连接
    - 对解构操作不友好：当响应式对象的原始类型属性被解构为本地变量时，或者该属性被传递给函数时，将会丢失响应性连接

!!! warning "注意"

    因此，建议使用 `ref()` 作为声明响应式状态的主要 API。

???+ info "额外的 ref 解包细节"

    **解包**：我们可以直接访问 ref 值，而无需附加 `.value` 。

- ref 作为 reactive 对象的属性时，当被访问或修改时会自动解包
    - 如果将一个新的 ref 赋值给一个关联了已有 ref 的属性，那么它会替换掉旧的 ref
    - 只有当嵌套在一个深层响应式对象内时，才会发生 ref 解包

- 当 ref 作为响应式**数组**或原生**集合**类型 (如 `Map`) 中的元素被访问时，它**不会**被解包
- 在模板渲染上下文中，只有**顶级**的 ref 属性才会被解包
- 如果 ref 是文本插值的最终计算值 (即 `{{ }}` 标签)，那么它将被解包


## 事件处理

`v-on`指令（可简记为`@`）用于监听DOM事件，并在事件触发时执行对应的JS脚本。格式为：

- `v-on:click="handler"`
- 或`@click="handler"`

**事件处理器**(handler)的值可以是：

- **内联**事件处理器：事件被触发时执行的内联JS语句(与`onclick`类似)，通常用于简单场景

    - 数据绑定

    ??? example "例子"

        ```js
        const count = ref(0)
        ```

        ```html
        <button @click="count++">Add 1</button>
        <p>Count is: {{ count }}</p>
        ```

    - 调用方法

    ??? example "例子"

        ```js
        function say(message) {
            alert(message)
        }
        ```

        ```html
        <button @click="say('hello')">Say hello</button>
        <button @click="say('bye')">Say bye</button>
        ```

    - 也可以在调用方法时传入特殊的`$event`变量，或使用内联箭头函数，以访问原生DOM事件

    ??? example "例子"

        ```html
        <!-- 使用特殊的 $event 变量 -->
        <button @click="warn('Form cannot be submitted yet.', $event)">
            Submit
        </button>

        <!-- 使用内联箭头函数 -->
        <button @click="(event) => warn('Form cannot be submitted yet.', event)">
            Submit
        </button>
        ```

        ```js
        function warn(message, event) {
            // 这里可以访问原生事件
            if (event) {
                event.preventDefault()
            }
            alert(message)
        }
        ```

- **方法**事件处理器：一个指向组件上定义的方法的属性名或是路径

    ??? example "例子"

        ```js
        const name = ref('Vue.js')

        function greet(event) {
            alert(`Hello ${name.value}!`)
            // `event` 是 DOM 原生事件
            if (event) {
                alert(event.target.tagName)
            }
        }
        ```

        ```html
        <!-- `greet` 是上面定义过的方法名 -->
        <button @click="greet">Greet</button>
        ```

- 判断方法：
    - 内联事件处理器：形如`foo`、`foo.bar`和`foo['bar']`
    - 方法事件处理器：形如`foo()`和`count++`

### 修饰符

修饰符：用`.`表示的指令后缀

- 事件修饰符：用于阻止事件的默认行为或进一步传播（对应JS的`event.preventDefault()`和`event.stopPropagation()`方法），使我们更专注于数据逻辑而不用去处理DOM事件的细节
    - 包括了：
        - `.stop`：停止事件的传递
        - `.prevent`：阻止重新加载页面
        - `.self`：仅当`event.target`是元素本身时才会触发事件处理器
        - `.capture`：指向内部元素的事件，在被内部元素处理前，先被外部处理
        - `.once`：事件最多被触发一次
        - `.passive`：事件的默认行为将立即发生而非等待事件完成
            - 一般用于触摸事件的监听器，可以用来改善移动端设备的滚屏性能
            - 请勿同时使用`.prevent`和`.passive`

        ```html
        <a @click.stop="doThis"></a>
        ```

    - 修饰符可以使用链式书写，即同一个事件可以连续使用多个修饰符

- 按键修饰符
    - 常规按键：
        - `.enter`
        - `.tab`
        - `.delete` (捕获+Delete+和+Backspace+两个按键)
        - `.esc`
        - `.space`
        - `.up`
        - `.down`
        - `.left`
        - `.right`
    - 系统按键：在事件发出时必须处于按下状态，单独按下松开系统按键不会触发任何事件
        - `.ctrl`
        - `.alt`
        - `.shift`
        - `.meta`（在Windows上指的是Windows键，在Mac上指的是Command键）

        ```html
        <!-- Alt + Enter -->
        <input @keyup.alt.enter="clear" />

        <!-- Ctrl + 点击 -->
        <div @click.ctrl="doSomething">Do something</div>
        ```

    - `.exact`：符允许精确控制触发事件所需的系统修饰符的组合

    ```html
    <!-- 当按下 Ctrl 时，即使同时按下 Alt 或 Shift 也会触发 -->
    <button @click.ctrl="onClick">A</button>

    <!-- 仅当按下 Ctrl 且未按任何其他键时才会触发 -->
    <button @click.ctrl.exact="onCtrlClick">A</button>

    <!-- 仅当没有按下任何系统按键时触发 -->
    <button @click.exact="onClick">A</button>
    ```

- 鼠标按键修饰符
    - `.left`
    - `.right`
    - `.middle`

## 生命周期

**生命周期钩子**(hook)（本质上是函数）在组件实例的生命周期的不同阶段中被自动调用，用于完成一系列的初始化步骤。钩子应当在组件初始化时被**同步**注册。

常用的生命周期钩子有：

- `onMounted`：在组件完成初始渲染并创建 DOM 节点后运行代码（类似构造函数）
- `onUpdated`：在组件因为响应式状态变更而更新其 DOM 树之后调用
- `onUnmounted`：在组件实例被卸载之后调用（类似析构函数）

生命周期图示：

<div style="text-align: center">
    <image src="../images/vue/3.png" width=80%>
</div>

相关资料：[生命周期钩子API索引](https://cn.vuejs.org/api/composition-api-lifecycle)

## 侦听器

- `watch()`函数：在每次响应式状态发生变化时触发回调函数
    - 前面的参数可以是不同形式的“**数据源**”，`watch()`函数只追踪这些指定的数据源，也就是说只有这些数据源改变时才会触发回调函数。数据源包括：
        - ref (包括计算属性)
        - 响应式对象，此时会隐式地创建一个**深层侦听器**，该回调函数在所有嵌套的变更时都会被触发
        - getter 函数
            - 一个返回响应式对象的 getter 函数，只有在返回不同的对象时，才会触发回调
            - 可以在`watch()`函数的最后加上`deep`选项，使其强制转化为深层监听器

        - 多个数据源组成的数组

    - 不能直接侦听响应式对象的属性值

    ??? example "例子"

        ```js
        const x = ref(0)
        const y = ref(0)

        // 单个 ref
        watch(x, (newX) => {
            console.log(`x is ${newX}`)
        })

        // getter 函数
        watch(
            () => x.value + y.value,
            (sum) => {
                console.log(`sum of x + y is: ${sum}`)
            }
        )

        // 多个来源组成的数组
        watch([x, () => y.value], ([newX, newY]) => {
            console.log(`x is ${newX} and y is ${newY}`)
        })
        ```

    - 深层侦听器：`deep`选项
        - 其值可以是布尔值，也可以是数字（表示最大遍历深度）
        - 谨慎使用：深度侦听需要遍历被侦听对象中的所有嵌套的属性，当用于大型数据结构时，开销很大。因此请只在必要时才使用它，并且要留意性能    

        ```js hl_lines="7"
        watch(
            () => state.someObject,
            (newValue, oldValue) => {
                // 注意：`newValue` 此处和 `oldValue` 是相等的
                // *除非* state.someObject 被整个替换了
            },
            { deep: true }
        )
        ```

    - 即时回调的侦听器：`immediate`选项
        - `watch()`默认是懒执行的，仅当数据源变化时，才会执行回调
        - 但在某些场景中，我们希望在创建侦听器时，立即执行一遍回调，此时可以通过`{ immediate:true }`来强制侦听器的回调立即执行

    - 一次性侦听器：`once`选项
        - 默认情况下，每当被侦听源发生变化时，侦听器的回调就会执行
        - `{ once: true }`可以使回调只在源变化时触发一次

- `watchEffect()`函数：允许自动跟踪回调的响应式依赖
    - 回调函数会立即执行，因此无需指定`immediate: true`
    - 若回调函数内任一响应式属性发生改变，回调函数会再次执行
    - 相比`watch()`函数，由于它会自动追踪所有能访问到的响应式属性，因此我们无需显式传递数据源。对于有多个依赖项的侦听器来说，可以显著减少手动维护依赖列表的负担
    - 该函数也可用于侦听一个嵌套数据结构中的几个属性，可能比深度侦测器更有效，因为它将只跟踪回调中被使用到的属性，而不是递归地跟踪所有的属性

    ```js
    watchEffect(async () => {
        const response = await fetch(
            `https://jsonplaceholder.typicode.com/todos/${todoId.value}`
        )
        data.value = await response.json()
    })
    ```

- `onWatcherCleanup()`：一个用于清理副作用的函数，当侦听器失效并准备重新运行时会被调用
    - 它必须在`watchEffect()`函数或`watch()`回调函数的同步执行期间调用，而不能在异步函数的`await`语句之后调用它
    - 在Vue 3.5以前的版本，使用的是`onCleanup`函数，它作为第三个参数传递给侦听器回调，因此不受`onWatcherCleanup`的同步限制

- 回调函数的触发时机：侦听器回调函数会在父组件更新 （如有）**之后**、所属组件的 DOM 更新**之前**被调用
    - 若想在侦听器回调中能访问被 Vue 更新**之后**的所属组件的 DOM
        - `watch()`函数：增加`{ flush: 'post' }`选项
        - `watchEffect()`函数：使用别名`watchPostEffect()`
    - 同步侦听器：在 Vue 进行任何更新之前触发；可以使用它来监视简单的布尔值，但应避免在可能多次同步修改的数据源 (如数组) 上使用
        - `watch()`函数：增加`{ flush: 'sync' }`选项
        - `watchEffect()`函数：使用别名`watchSyncEffect()`

- 停止侦听器：
    - 在`setup()`或`<script setup>`中用同步语句创建的侦听器，会自动绑定到宿主组件实例上，并且会在宿主组件卸载时自动停止。因此，在大多数情况下，我们无需关心怎么停止一个侦听器
    - 侦听器必须用同步语句创建，如果用异步回调创建一个侦听器，那么它不会绑定到当前组件上，此时必须手动停止它，以防内存泄漏。
        - 具体做法：调用`watch`或`watchEffect`返回的函数

        ```js
        const unwatch = watchEffect(() => {})

        // ...当该侦听器不再需要时
        unwatch()
        ```

## 模板引用

`ref`属性：用于直接访问底层的DOM元素，即允许在一个特定的 DOM 元素或子组件实例被挂载后，获得对它的直接引用。

```html
<script setup>
import { useTemplateRef, onMounted } from 'vue'

// 第一个参数必须与模板中的 ref 值匹配
const input = useTemplateRef('my-input')

onMounted(() => {
  input.value.focus()
})
</script>

<template>
  <input ref="my-input" />
</template>
```

- 访问模板引用：使用辅助函数`useTemplateRef()`
    - 只能在组件挂载后才能访问模板引用，因为在初次渲染前这个元素还不存在，因此其值为`null`

- `v-for`中的模板引用：对应的 ref 中包含的值是一个数组，它将在元素被挂载后包含对应整个列表的所有元素
    - ref 数组并不保证与源数组相同的顺序

    ??? example "例子"

        ```html
        <script setup>
        import { ref, useTemplateRef, onMounted } from 'vue'

        const list = ref([
        /* ... */
        ])

        const itemRefs = useTemplateRef('items')

        onMounted(() => console.log(itemRefs.value))
        </script>

        <template>
            <ul>
                <li v-for="item in list" ref="items">
                {{ item }}
                </li>
            </ul>
        </template>
        ```

- 函数模板引用：`:ref`属性可以绑定一个函数，会在每次组件更新时都被调用。该函数会收到元素引用作为其第一个参数
    - 当绑定的元素被卸载时，函数也会被调用一次，此时参数值为`null`

    ```html
    <input :ref="(el) => { /* 将 el 赋值给一个数据属性或 ref 变量 */ }">
    ```

