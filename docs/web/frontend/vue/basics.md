---
counter: true
---


# Vue 基础部分

## 简介

Vue的定义（摘自官方文档）：

>Vue (发音为 /vjuː/，类似 view) 是一款用于构建用户界面的 **JavaScript 框架**。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套**声明式的、组件化的编程模型**，帮助你高效地开发用户界面。无论是简单还是复杂的界面，Vue 都可以胜任。

核心功能：

- **声明式渲染**：Vue 基于标准 HTML 拓展了一套模板语法，使得我们可以声明式地描述最终输出的 HTML 和 JavaScript 状态之间的关系
- **响应性**：Vue 会自动跟踪 JavaScript 状态并在其发生变化时响应式地更新 DOM

**单文件组件**(single-file components, SFC)：将一个组件的逻辑(JavaScript)，模板(HTML)和样式(CSS)封装在同一个文件里。

??? code "代码示例"

    ```vue
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

    ```vue
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

## 响应式基础

!!! info "注"

    这是我第一次学习 Vue，虽然官方推荐新手先学选项式API，但从个人偏好上来说我还是更倾向于组合式API，因为选项式API那种面向对象的风格看起来略显臃肿，而组合式API做同样的工作只需几句话就搞定了。所以我目前先从**组合式API**开始学习，笔记呈现的代码都是组合式API风格，之后有时间的话会补充选项式API的内容。

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

        ```vue
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

## Class 与 Style 绑定

## 条件渲染

## 列表渲染

## 事件处理

## 表单输入绑定

## 生命周期

## 侦听器

## 模板引用

## 组件基础





