---
counter: true
---

# JavaScript 基础部分

## 基础知识

- 引入 JavaScript 脚本的方式：
    - 内部嵌入：使用 `<script>` 标签，里面直接写 JS 代码（仅适用于代码量少的情况，不推荐）
    - 外部导入：在 `<script>` 元素中使用 `src` 属性，它的值为 JS 外部文件的地址（本地或 URL 均可），此时会忽略标签内的任何内容。推荐用这种方法，因为浏览器会下载 JS 文件并保存到缓存中，下次打开网页无需再次下载，使页面加载更快
- 注释：同 C 语言
- 在 JS 代码开头添上 `"use strict";`，JS 将启用严格模式，使用新版本的特性，推荐使用
- 好的书写习惯
    - 花括号：

    ``` js 
    if (condition) {
        // body
    }
    ```
    
    - 每行长度不超过 80 个字符
    - 缩进，额外的空行，分号
    - 尽可能减少嵌套语句的出现
    - 函数名能够精确表示函数的功能（动词）
    - 一个函数只做一件事
    - 令 函数 == 注释
    - 函数位置在主程序下面，便于阅读    
    - [反面教材：忍者代码](https://zh.javascript.info/ninja-code)

### 变量

- `let` 关键字用于声明各种类型的变量
    - 推荐一行声明一个变量，方便阅读
    - 同一个变量声明两次会报错
    - 变量命名：类似 C 语言，但它还允许符号 `$`，且 `$` 和 `_` 在命名时被视为字母（~~甚至可以用中文，但别这么做~~）（[保留字列表](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#keywords)）
    - 推荐的做法：使用易读的名称，避免使用缩写，名称能够准确描述变量功能，为不同的值使用不同的变量
- ~~`var` 不要用~~，它与 `let` 和 `const` 有以下区别：
    - `var` 声明的变量没有块级作用域，即它们要么在当前函数可见，要么全局可见
    - `var` 变量申明在函数开头就会被处理
- `const` 关键字用于声明常量变量，这类变量无法被修改
    - 推荐的命名法：使用大写字母和下划线来命名，用于存储一些难以记住且确保不变的值

### 数据类型

可以使用 `typeof x` 运算符返回变量 `x` 的类型。

- number：整数、浮点数，以及一些「特殊数值」：`Infinity`、`-Infinity`、`NaN`（计算错误），安全范围为 $-(2^{53} - 1) \sim (2^{53} - 1)$
    - 如果数字特别长，可以用下划线 `_` 间隔，JS 会忽略数字之间的 `_`，这是一种语法糖
    - 科学计数法 `e`（同 C 语言）
    - 十六进制（前缀 `0x`）、八进制（前缀 `0o`）、二进制（前缀 `0b`）
    - 使用 `num.toString(base)` 方法可以返回数字在 base 进制下的字符串表现形式（`base` 最大为 36）。如果 `num` 是数字字面量而非变量，需要用两个点（即 `..toString(base)`）或者用括号将数字包起来
    - 关于舍入的数学函数
        - `Math.ceil(num)`：向上取整
        - `Math.floor(num)`：向下取整
        - `Math.round(num)`：四舍五入
        - `Math.trunc(num)`：截断（小数部分）取整
        - 四舍五入至第 n 位：
            - `Math.round(num * 1en) / 1en`，请将 `n` 替换为数字
            - `Number(num.toFixed(n))`（`.toFixed()` 返回的是字符串） 
    - 同 C 语言，JS 也无法精确存储小数，使用 `.toFixed()` 方法对结果进行舍入可以缓解这种情况
    - `isNaN(value)` 函数：先将 `value` 转化为数字型，然后判断它是否为 `NaN`，若是则返回 `true`，否则返回 `false`
    - `isFinite(value)` 函数：先将 `value` 转化为数字型，然后判断它是否为常规数字（不是 `NaN/Infinity/-Infinity`），若是则返回 `true`，否则返回 `false`（注意空字符串或仅包含空白字符的字符串转化为数字后都是 0）
    - `parseInt(str[, base])` 函数：从字符串中提取（`base` 进制，可选参数）整数，直到无法提取为止，返回已提取的数字
    - `parseFloat(str)` 函数：类似上面的函数，但返回的是浮点数
    - 其他内建函数（来自 Math 对象）
        - `Math.random()` 返回 $[0, 1)$ 之间的随机数
        - `Math.max(a, b, c...)` 和 `Math.min(a, b, c...)`：分别返回参数中的最大值和最小值
        - `Math.pow(n, power)`：返回 `n^{power}`
 
- bigint：任意长度的整数
- string：可用单引号、双引号或反引号表示字符串
    - 但是反引号的字符串允许将变量或表达式传进去（还需使用 `${}` 包装，类似 Python） ，还允许字符串跨行
    
    ``` js
    let guestList = `Guests:
        * John
        * Pete
        * Mary
        `;
    ```

    - 转义字符（同 C 语言）
        - `\uXXXX` 使用 Unicode 编码的字符
    - `.length`：字符串长度
    - 访问字符串指定字符
        - `str[pos]`
        - `str.charAt(pos)`
        >两者的区别是若没有找到字符，前者返回 `undefined`，后者返回空字符串
    - 遍历字符串的字符 `for (let char of str)`（注意是 `of`）
    - 不可以直接修改字符串的内容
    - `.toLowerCase()` 和 `.toUpperCase()` 方法分别使字符串的字母全变成小写字母和大写字母
    - 查找子字符串
        - `str.indexOf(substr, pos)`：从给定位置 `pos` 开始查找 `str` 的子字符串 `substr`，若找到返回子字符串首次出现的位置，否则返回 -1
        - `str.lastIndexOf(substr, pos)`：类似上面的方法，但它是从字符串末尾开始逆向遍历
        - `str.includes(substr[, pos])`：也类似第一种方法，但 `pos` 位置可选，且返回的是 `true` 或 `false`
        - `str.startsWith(substr)`：检查字符串是否以 `substr` 开头，若是则返回 `true`，否则返回 `false`
        - `str.endsWith(substr)`：检查字符串是否以 `substr` 结尾，若是则返回 `true`，否则返回 `false`
    - 获取子字符串
        - `str.slice(start[, end])` :star:：返回 `str` 从 `start` 位置开始到 `end` 位置为止（不包括 `end`）的子字符串，若只有一个参数则返回从 `start` 开始剩余部分的子字符串。注意 `start` 和 `end` 可以是负数（`-1` 是最右边的字符索引，负数索引是从右往左数的，同 Python）
        - `str.substring(start[, end])`：与前一种方法的唯一区别在于不支持负参数（会被视为 0）
        - `str.substr(start[, length])`：与第一种方法的区别是第二个参数指定的是子字符串的长度而非结束位置（因此必须是非负值）
    - 比较字符串
        - `str.codePointAt(pos)`：返回字符串 `str` 在 `pos` 位置的字符的 ASCII 码
        - `String.fromCodePoint(code)`：返回 ASCII 码为 `code` 的字符

- boolean：`true`、`false`
- null：未知值
- undefined：未定义的值（未被赋值...）
- symbol：对象的唯一标识符（见“对象 symbol 类型”一节）
- object：（见“对象”一章）

---
**类型转换**

- `String(value)` 将 `value` 转为字符串型
- 数字型
    - 自动转换：算术运算
    - 显示转换：`Number(value)`，一些特殊规则：
        - `Number(undefined) -> NaN`
        - `Number(null) -> 0`
        - `Number(true) -> 1  Number(false) -> 0`
        - 字符串转数字会先去掉空白字符，若剩余部分为空返回0，若无法转为数字返回 `NaN`
- 布尔型：`Boolean(value)`，除了 `0`、空字符串、`null`、`undefined`、`NaN` 返回 `false`，其余值都返回 `true` 

---
**数组**

- 数组本质上是一种特殊的对象（特殊之处在于数组存储的是**有序数据**），数组的元素可以是任意类型（对象、函数等均可）
- 创建空数组（2 种方法）

``` js 
let arr = new Array();
let arr = [];          // 用的更多
```

- 初始化数组：`let fruits = ["Apple", "Banana", "Orange"];`
- 访问并修改元素：
    - `fruits[2] = 'Pear'`，注意无法使用负索引
    - `.at(i)` 方法可以访问索引为 `i` 的数组元素，`i` 可以是负数
    - `.pop()`：取出数组末端的元素
    - `.shift`：取出数组开头的元素
- 新增元素
    - 若访问不存在的元素，则会往数组添加元素，比如 `fruits[3] = 'Lemon'`
    - `.push(elem)`：在数组末尾添加元素 `elem`
    - `.unshift(elem)`：在数组开头添加元素 `elem`
>注：`pop()` 和 `push()` 的速度快于 `unshift()` 和 `shift()`（字面意思，后两种方法还多了一步 O(n) 的移位操作）
- `.length`：数组元素个数
    - 我们可以手动修改 `.length` 的值：增加不会发生变化，减小则会截断数组（不可逆）
    - 清空数组：`arr.length = 0;`
- 引用复制：`let arr = fruits;`
- 数组的错误使用方法
    - 添加非数字的属性，比如 `arr.test = 5;`
    - 制造空洞，比如添加 `arr[0]` 后就添加 `arr[1000]`，中间没有元素
    - 倒序填充数组
- 遍历数组：使用 `for...of` 循环（~~不要用 `for...in` 循环~~）
- 多维数组
- `String(arr)`：数组 -> 字符串，该字符串是一个用逗号间隔的元素列表
- 不要使用 `==` 比较数组
- `.splice()` 方法：
    - 语法：`arr.splice(start[, deleteCount, elem1, ..., elemN])`，其中只有 `start` 是必写参数，它可以是负数（使用负索引）
    - 功能：从索引 `start` 开始修改 `arr`，删除 `deleteCount` 个元素后，在当前位置插入新的元素 `elem1, ..., elemN`，最后返回修改后的数组
    - 实际运用：

    ``` js
    let arr = ["I", "study", "JavaScript", "right", "now"];
    arr.splice(0, 3, "Let's", "dance");
    // arr == ["Let's", "dance", "right", "now"]

    // 增加元素
    let arr = ["I", "study", "JavaScript"];
    arr.splice(2, 0, "complex", "language");
    // arr == ["I", "study", "complex", "language", "JavaScript"]
    ```

- `arr.slice([start], [end])` 方法：获取 `start` 到 `end`（不包括 `end`）之间所有的数组元素，返回由这些元素构成的数组。两个参数可以是负数，且都是可选参数（参数表为空则复制整个数组）
- `arr.concat(arg1, arg2...)` 方法：返回由原数组与传入参数（可以是任何值（对象也行）和数组（只会复制数组的元素，不复制完整实体））拼接而成的新数组
>如果对象有 `Symbol.isConcatSpreadable` 属性，将对象视作数组拼接

- `.forEach()` 方法：为数组的每个元素都运行一个函数
    - 语法（其中三个参数分别为数组元素、索引、数组）：

    ``` js
    arr.forEach(function(item, index, array) {
        // ...
    });
    ```

    - 括号里面的函数既可以是内建函数、箭头函数等
    - 变体：`.map()` 方法，语法类似，但注意函数返回值是新的值而不是当前元素，且调用该方法返回的是数组元素经过函数修改后的新数组
- `arr.indexOf(item, from)`：从索引 `from` 开始搜索 `item`，若找到则返回索引，否则返回 -1
- `arr.lastIndexOf(item, from)`：从索引 `from` 开始**逆向**（从右往左）搜索 `item`，若找到则返回索引，否则返回 -1
- `arr.includes(item, from)`：类似上一种方法，但返回的是 `true` 或 `false`
- `.find()` 方法：用于对象数组，寻找具有特定条件的对象
    - 语法同`.forEach()` 方法
    - 但是函数体的内容有讲究：如果找到符合条件的对象则返回 `item` 并停止迭代；如果遍历完后都找不到则返回 `undefined`
    - 变体：
        - `.findeIndex()` 返回的是索引
        - `.findLastIndex()` 逆向搜索，返回索引
        - `.filter` 返回的是所有匹配条件的元素构成的数组，而不是第一个符合条件的元素
- `.sort([cmp_func])` 方法：对数组进行排序（注意这个操作修改的是**原数组**的内容，而非数组的副本）
    - 如果括号内没有参数，则会将所有元素视为字符串，按照字符串比较规则升序排序
    - 括号内可以指定比较函数，用来确定排序规则，比如：

    ``` js
    function compareNumeric(a, b) {
        if (a > b) return 1;
        if (a == b) return 0;
        if (a < b) return -1;
    }

    // 调用，现在该方法是按照数字大小排序的了
    arr.sort(compareNumeric);
    ```

    事实上，比较函数返回正值表示“大于”，返回负值表示“小于”，所以有以下的精简版：

    ``` js
    arr.sort( (a, b) => a - b );
    ```

- `arr.reverse()`：逆转数组的顺序
- `str.split(delim[, length])`：将字符串 `str` 按照分隔字符 `delim` 划分元素并形成一个数组
    - 第二个参数 `length` 控制划分元素的个数，很少用
    - 如果 `delim = ''`，该方法将每个字符作为单独的数组元素
- `arr.join(glue)`：将数组元素连接成一个字符串，元素之间用 `glue` 分隔
- `.reduce()` 方法：让每个数组元素运行指定函数，返回运行函数后的结果
    - 语法：

    ``` js
    let value = arr.reduce(function(accumulator, item, index, array) {
        // ...
    }, [initial]);
    // accumulator：累加器，保存上一次调用函数的结果
    // item：数组元素
    // index：索引
    // arr：数组
    // initial：accumulator 的初始值
    // 函数返回值为最后一次调用函数后 accumulator 的值
    ```

    - 应用：

    ``` js
    let arr = [1, 2, 3, 4, 5];

    let result = arr.reduce((sum, current) => sum + current, 0);
    
    // result == 15
    ```

- `Array.isArray()` 方法：判断变量是否为数组，返回布尔值
- 除了 `.sort()` 方法外，上述大多数调用函数的方法都有第二个参数 `thisArg`。当第一个参数 `func` 函数出现 `this` 时，如果没有第二个参数指定 `this` 对应的对象就会报错，所以需要 `thisArg` 显式指出对象
        

### 运算符

与 C 语言相同的部分就不再赘述，这里着重介绍 JS 特有的部分。

- 求幂 `**` （同 Python）
- `+` 可拼接字符串，而且如果 `+` 两边有一边是字符串，那么另一边会被转化为字符串然后被拼接起来（比如 `'1' + 2 + 2 == '122'`）。而其他运算符都是将两边的变量转为数字型
- `+` 作为一元运算符，用于非数字变量前的作用与 `Number()` 一致，将其转为数字型（比如 `+"2" + +"3" == 5`）
- 链式赋值：多个变量用赋值号 `=` 连接，赋值顺序从右向左（同 Python）
- 也有自增（`++`）/自减（`--`）运算符
- 位运算符多了一个无符号右移（`>>>`）
- [运算符优先级表](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Operator_precedence#%E6%B1%87%E6%80%BB%E8%A1%A8)
- 值的比较
    - 注意字符串比较规则（同 C 语言）
    - 不同类型的比较：先全部转为数字型再比较大小
    - 比较运算符几乎同 C 语言，但它多了个严格相等运算符 `===`，它就不会先将两侧的值转化为数字，而是直接比较（符合我们的直觉）。同样也多了对应的严格不相等 `!==`
    - `Object.is(val1, val2)` 类似 `===`，但有以下区别：
        - `Object.is(NaN, NaN)` 的值为 `true`，`NaN === NaN` 返回 `false`
        - `Object.is(0, -0)` 的值为 `false`，`0 === -0` 返回 `true`


### 条件分支

- `if`、`else`、`else if`
- 条件（三目）运算符 `?`
- 逻辑运算符：`||`、`&&`、`!`
    - 注意“短路求值”的概念
    - 空值合并运算符 `??`
        - 用法：`a ?? b`，当 `a` 不是 `null` 或 `undefined` 时返回 `a`，否则返回 `b`
        - 可以连续使用多个 `??` 从一系列的值中返回第一个非 `null` 或 `undefined` 的值
        - 不可以与 `&&` 和 `||` 一起用，除非用括号隔开
- `switch` 语法类似 C 语言，但要注意以下几点：
    - `case value:` 中的 `value` 可以为任意表达式
    - 采用的是**严格相等**的比较方式

### 循环

- `for`
- `while`
- `do...while`
- `break`、`continue`
    - 它们不能与条件运算符一起使用
    - 它们还有一种与 C 语言 `goto` 类似的用法

    ```js
    label: {
        // ...
        break label;
        // ...
    }
    ```

### 交互

- `alert(msg)` 函数：运行该函数后会显示一个名为模态窗(modal window)的东西，内容为 msg（字符串），直到点击“确定”按钮后用户才能与页面交互
- `prompt(title, [default])`：显示内容为 `title` 的模态框，还有一个输入框和确认/取消按钮。它会将我们输入的内容作为函数返回值，如果点击取消或直接退出（`Esc`），返回值为 `null`
    - 第二个参数 `default` 可选，作为默认的输入内容出现在输入框上，推荐使用
- `confirm(question)`：显示内容为 `question` 的模态框，带确认/取消按钮，点击确认返回 `true`，点击取消或直接退出返回 `false`

## 函数

### 基础部分

- 函数声明：

``` js
function name(param1[ = exp1], param2[ = exp2], ... paramN[ = expN]) {
    ...body...
}
```

- 函数表达式：在任何表达式的中间声明函数，这时函数可以省略函数名（匿名函数，我们无法直接访问这类函数）

``` js
let sayHi = function() {
    alert("Hello");
};
```

!!! note "函数声明 vs 函数表达式"

    一些区别：

    - 函数表达式是在代码执行到达时被创建，在这之后我们才可以调用它；而函数声明可以在它声明之前就可以被调用，只要调用语句与函数声明位于同一代码块内
    - 然而，如果调用语句在函数声明所处的代码块外，那么就会报错。解决方法是在代码块外声明变量，在代码块内对该变量使用函数表达式，这样在代码块外通过调用这个变量（实际上成为函数了）来调用函数

- 局部变量、外部变量（全局变量尽量少用）
- 形参(parameter)：函数声明中括号内列出的变量，实参(argument)：函数调用时传给函数的值，可以为形参设置默认值（可以是复杂的表达式，甚至是函数）
- 如果某个参数没有传入值，该参数为 `undefined`
- `return` 返回值
    - `return;` 和不写 `return` 一样，最终返回的是 `undefined`
    - 不要在 `return` 和返回值之间添加新行，因为在同一行上，若 `return` 后面没有内容，JS 自动会加上分号


- 函数是一个值
    - 可以将一个函数赋给变量，那么该变量就成为与该函数一样的函数（比如 `let func = sayHi`后，`func() == sayHi()`）
    - `alert(func)` 的结果是显示 `func()` 函数的源码
- 回调函数：简单理解为作为参数值的函数

??? example "例子"

    下面代码中，`showOk()` 和 `showCancel()` 都是回调函数：

    ``` js
    function ask(question, yes, no) {
        if (confirm(question)) yes();
        else no;
    }

    function showOk() {
        alert("You agreed.");
    }

    function showCancel() {
        alert("You canceled the execution.");
    }

    ask("Do you agree?", showOk, showCancel);
    ```

    我们可以使用匿名函数简写上面的回调函数：

    ``` js
    function ask(question, yes, no) {
        if (confirm(question)) yes();
        else no;
    }

    ask(
        "Do you agree?",
        function() { alert("You agreed."); },
        function() { alert("You canceled the execution."); }
    );
    ```
- 箭头函数
    - 格式：`let func = (arg1, arg2, ..., argN) => expression`，等价于下面的函数表达式：
    ``` js
    let func = function(arg1, arg2, ..., argN) {
        return expression;
    };
    ```

    - 如果只有一个参数，可以省略圆括号
    - 如果没有参数，必须留下空括号
    - 多行的箭头函数：使用花括号，最后要用 `return` 语句返回值，比如：

    ``` js
    let sum = (a, b) => {
        let result = a + b;
        return result;
    };
    ```
    - 箭头函数没有 `this`，所以若访问 `this`，函数会尝试从外部获取对象
    - 不能将箭头函数作为构造函数，即不能使用 `new` 操作符
    - 箭头函数没有 `arguments` 变量

### 变量作用域、闭包

- 代码块：在代码块 `{...}` 内（包括 `if`、`for`、`while` 等）声明的变量只有在该代码块内可见
- 嵌套函数：一个函数创建于另一个函数内
    - 函数还可以返回一个嵌套函数
- 词法环境：由**环境记录**(environment record)（一个存储所有局部变量作为其属性的对象）和对**外部词法环境**的引用构成
    - **全局**词法环境：没有外部引用的词法环境

    ??? example "例子"

        这个例子展示了代码执行过程中全局词法环境的变化：

        <figure style=" width: 50%" markdown="span">
            ![](../images/js/4_dark.png#only-dark)
            ![](../images/js/4_light.png#only-light)
            <figcaption></figcaption>
        </figure>

    - 函数声明：虽然函数和变量一样也是一个值，但不同于变量的是只要有函数声明，函数就已经创建完毕，不像变量要到执行到声明语句后才会被创建。下面这张图体现了函数和变量的这点区别：

    <figure style=" width: 50%" markdown="span">
        ![](../images/js/5_dark.png#only-dark)
        ![](../images/js/5_light.png#only-light)
        <figcaption></figcaption>
    </figure>

    - 多个词法环境：当函数开始被调用时，JS 会自动创建一个新的词法环境，用于存储该函数的局部变量和参数。此时程序分为内部词法环境和外部词法环境
    - 程序访问变量的顺序：内部词法环境 -> 外部词法环境 -> ...（更外部的词法环境）-> 全局词法环境

    ??? example "例子"

        该例子展示了程序如何找到变量对应的值

        <figure style=" width: 50%" markdown="span">
            ![](../images/js/6_dark.png#only-dark)
            ![](../images/js/6_light.png#only-light)
            <figcaption></figcaption>
        </figure>

    - 所有函数都有名为 `[[Environment]]` 的隐藏属性，该属性保存了对创建该函数的词法环境的引用

- **闭包(closure)**：一个函数可以记住其外部变量并且可以访问这些变量。JS 中所有函数都是闭包的，它们自动通过隐藏的 `[[Environment]]` 属性记住创建它们的位置，所以它们都可以访问外部变量。

### setTimeout 和 setInterval

- `setTimeout()` 函数：延迟执行指定函数
    - 语法：`setTImeout(func|code[, delay, arg1, arg2,...])`
        - `func`：想要执行的函数或代码块
        - `delay`：执行前的延迟时间（单位：ms）
        - `arg1, arg2...`：`func` 的参数列表
    - 返回值是一个定时器标识符(timer identifier)，可以用它来取消该函数的执行——执行 `clearTimeout(timerId)` 即可（`timerId` 为该函数的返回值）
    - 零延时调用 `setTimeout(func, 0)` 或 `setTimeout(func)`，使该函数在当前脚本执行完时调用（事实上至少还有 4ms 延迟）
- `setInterval()` 函数：间隔指定时间，周期性执行指定函数
    - 语法同上面的函数
    - 同样也可以阻止该函数的调用——执行 `clearInterval(timerId)`

可以使用嵌套的 `setTImeout`。这种嵌套方法相比 `setInterval()`，在两次执行之间的延时的设置上更加灵活精确。

``` js
setInterval(func, delay);

// 等价于
setTimeout(function run() {
    // func 函数体
    setTimeout(run, delay);
}, delay);
```

下面两张图分别展示它们在时间间隔上的微妙差异（上图为 `setInterval()`，下图为嵌套的 `setTimeout()`，且 `delay = 100`）：


<figure style="width: 70%" markdown="span">
    ![](../images/js/10_dark.png#only-dark)
    ![](../images/js/10_light.png#only-light)
    <figcaption></figcaption>
</figure>

<figure style="width: 70%" markdown="span">
    ![](../images/js/11_dark.png#only-dark)
    ![](../images/js/11_light.png#only-light)
    <figcaption></figcaption>
</figure>

!!! warning "关于垃圾回收"

    - 当一个函数传入 `setInterval()` 或 `setTimeout()` 时，JS 会为该函数创建一个内部引用，这样该函数就无法被垃圾收集器回收，直到 `clearInterval()` 或 `clearTimeout()` 被调用为止
    - 如果该函数还引用了外部变量（形成一个闭包），那么只要该函数存在，外部变量就一直存在，可能比该函数占用更多的内存

    因此建议在程序最后使用 `clearInterval()` 或 `clearTimeout()`


## 对象

对象用于存储键值对或更复杂的实体。它是一个由花括号包起来的属性列表，一个属性就是一个键值对（`key:value`），键(key，又称属性名)是一个字符串或者 `symbol` 值（后面会讲到），值(value)可以是任何值

- 创建空对象：

    ``` js
    let user = new Object(); // 法1：构造函数
    let user = {};           // 法2：字面量
    ```

- 创建带键值对的对象：

    ``` js
    let user = {
        name: "NoughtQ",
        age: 20,
        // 最后一个属性的末尾可以不加逗号，
        // 但是为了修改属性的方便，强烈建议加上逗号        
    };
    ```

    我们可以进行以下操作：

    - 访问属性值：`user.name`、`user.age`
    - 加入新的属性：`user.isAdmin = true;`
    - 移除属性：`delete user.age;`

- 方括号访问法（`obj["property"]`） vs `.` 访问法（`obj.property`）：

    - 属性名可以由多个单词构成，但需要用引号括起来，比如 `"likes birds": true;`。如果要访问这样的多词属性，需要用方括号替代 `.`，比如 `user["likes birds"]`。

    - 方括号访问元素比用 `.` 访问元素更加灵活，因为只要方括号内的表达式的值为键名（字符串），那么就可以成功访问该属性，而 `.`访问法就不能这样，比如：

    ``` js
    let key = prompt("What do you want to know about the user?", "name");

    alert( user[key] );   // output the inputted name
    alert( user.key );    // undefined
    ```

    - 在对象字面量内使用方括号，这样的属性称为计算属性。看下面的例子，`[fruit]` 属性名（键）应该从 `fruit` 变量获取。方括号内还可以是一个复杂的表达式

    ``` js
    let fruit = prompt("Which fruit to buy?", "apple");

    let bag = {
    [fruit]: 5, // 属性名是从 fruit 变量中得到的
    };

    alert( bag.apple ); // 5 如果 fruit="apple"
    ```

    - 总结：`[]` 虽然强大但很麻烦，能够用 `.` 访问法就用它，实在不行用 `[]`

- 属性名的命名更加自由：只要不是保留字的字符都会被接受（~~甚至可以是一串数字~~），JS 会自动将名称转化为字符串
- 如果属性名和作为它对应值的变量的名称相同，则可以进行属性值简写，比如一个键值对 `name: name` 等价于 `name`
- `in` 操作符：判断属性是否存在，语法：`"key" in object`，其中 `key` 为属性名，`object` 为被检测的对象
- `for` 循环：`for (key in object) { ... }`，这样会遍历对象所有的键
- 属性的顺序问题：如果属性名是一个整数（只有数字字符），JS 会自动根据整数值进行升序排序，否则就按照创建时的顺序排序（对对象进行遍历的时候就会发现这个顺序）

### 对象引用和复制

对象引用：实际上，一个赋值了对象的变量并不是一个对象，它仅保存了该对象**在内存中的地址**，也就是该对象的**引用**。因此对于下列语句：

``` js
let user = { name: "NoughtQ" };

let admin = user;
```

`admin` 和 `user` 是同一个对象的引用。如果用 `admin` 修改这个对象的属性，那么用 `user` 也可以访问该对象修改后的属性。

`Object.assign`

- 语法为 `Object.assign(dest, [src1, src2, src3...])`，其中 `dest` 是目标对象，后面的可选参数为源对象，该方法会将所有源对象的属性拷贝到目标对象内，最后返回 `dest`
- 如果 `dest` 存在与源对象名称相同的属性，则该属性会被源对象的属性覆盖
- 使用该方法实现浅拷贝：`let clone = Object.assign({}, obj)`
>要实现深拷贝，需要用到 `.cloneDeep(obj)` 函数

### 方法

方法：作为对象属性的函数
 
``` js
let obj = {
    // ...
};

/* 方法声明 */
// 法1：函数表达式
obj.method = function() {
    // ...
}
// 法2：函数声明 + 变量赋值（略）
// 法3：
obj = {
    method: function() {
        // ...
    }
};
// 法4：
obj = {
    method() {
        // ...
    }
};

/* 方法调用 */
obj.method()

/* 复制函数 */
function func() {
    // ...
}

obj.method = func;
```

`this` 关键字：使对象方法能够访问对象中存储的信息，通过 `this.property` 可以访问对象的属性。

- JS 的 `this` 可用于任何函数中（即使不是对象的方法），JS 会根据代码上下文来计算 `this` 的值，也就是说 `this` 的值是在程序运行时获得的
- 如果 `this` 没有表示任何对象的话，它的值为 `undefined`（严格模式下）
- 箭头函数没有自己的 `this`，所以若在箭头函数内使用 `this`，`this` 的值取决于外部正常的函数


### 垃圾回收

JS 主要的内存管理概念是「可达性」，即被存储在内存中的可访问或可用的值，包括：

- 根(roots)：
    - 当前执行函数的变量和参数
    - 嵌套调用链上的其他函数及其变量和参数
    - 全局变量
    - ...
- 来自对根的引用或引用链 

如果值不具备可达性，那么 JS 的垃圾回收器就会自动删除这些值

??? example "一个复杂的例子"

    我们构建了一组相互关联的对象：

    ``` js
    function marry(man, woman) {
    woman.husband = man;
    man.wife = woman;

    return {
        father: man,
        mother: woman
    }
    }

    let family = marry({
        name: "John"
        }, {
        name: "Ann"
    });
    ```

    此时的内存结构图：

    <figure style=" width: 50%" markdown="span">
        ![](../images/js/1_dark.png#only-dark)
        ![](../images/js/1_light.png#only-light)
        <figcaption></figcaption>
    </figure>

    若我们移除两个引用：

    ``` js
    delete family.father;
    delete family.mother.husband;
    ```

    <figure style=" width: 50%" markdown="span">
        ![](../images/js/2_dark.png#only-dark)
        ![](../images/js/2_light.png#only-light)
        <figcaption></figcaption>
    </figure>

    现在没有对 `John` 的引用了，所以它变得不可达，那么 JS 就会自动将它从内存中删掉，实现垃圾回收。

    <figure style=" width: 50%" markdown="span">
        ![](../images/js/3_dark.png#only-dark)
        ![](../images/js/3_light.png#only-light)
        <figcaption></figcaption>
    </figure>

### 构造函数

若要创建多个类似的对象，较好的方法是使用**构造函数**来做，它能够实现可重用的对象创建代码，做到“一劳永逸”，无需一遍遍地使用字面量创建。这类函数与常规函数的区别有：

- 函数名以大写字母开头（约定）
- 只能由操作符 `new` 来执行


``` js
// 构造函数声明
function User(name) {
    // this = {};

    this.name = name;
    this.isAdmin = false;
    this.sayHi = function() {
        alert("My name is: " + this.name);
    };

    // return this;
}

// 调用构造函数
let user = new User("Jack");
// 可以像这样创建多个类似的对象
```

作为构造函数的函数无需 `return` 语句，因为默认有 `return this;`。但我们也可以手动加上 `return` 语句，JS 处理规则如下：

- 如果返回的是一个对象，则返回该对象而不是 `this` 
- 如果返回其他类型的值，则忽略该 `return` 语句，返回 `this`

???+ info "特殊用法：`new function() {...}`"

    在调用构造函数的位置创建函数，这样的函数是匿名函数，因此无法在后面被调用，这样的作用是处理构造单个对象时的复杂操作（而且后面也用不到了）。

`new.target` 可以检查该函数是否用 `new` 来调用过（也就是有没有成为构造函数），如果是常规调用则返回 `undefined`，如果是 `new` 调用则返回函数源码（从 `function` 到 `}` 的字符串）

### 可选链 ?.

对象属性的 `.` 访问法有一个问题：如果 `.` 两边的值有一个不存在（`null` 或 `undefined`），JS 就会报错，程序无法正常运行。但我们希望不要报错，这时就要用可选链 `?.` 来替代 `.`（`value?.prop`）：

- 只要 `?.` **前面**的值为 `null` 或 `undefined`，它就会停止运算并返回 `undefined`（这里就出现了「短路效应」，类似逻辑运算符）
- 否则就会返回 `value.prop`，即使不存在 `prop` 属性也不会报错，而是返回 `undefined`

在使用 `?.` 要注意以下几点：

- `?.` 可以安全地读取和删除对象的数据，但不能写入（否则会报错）：

``` js
obj?.prop = 114514; // Error
```

- 不要过度使用可选链，只有当某个属性是可选的（即它可能在对象内，也可以不在对象内）时候，使用 `?.` 是合理的。能不用 `?.` 尽量不用，还是用 `.`
- `?.` 前的变量必须已声明，否则会报错

可选链的其他变体：

- `?.()`：调用可能不存在的函数
- `?.[]`：类似 `?.`，读取可能不存在的属性（成功读取等价于 `[]` 访问法）

### Symbol 类型

`symbol` 值表示对象唯一的标识符（symbol 名相同的两个 `symbol` 值是不相等）

- 创建
    - `let id = Symbol("name")`
    - 在对象字面量内创建，需要用方括号将 symbol 名包起来：

    ``` js
    let user = {
        name: "NoughtQ",
        [id]: 123;
    };
    ```

- `symbol` 值无法被自动转化为字符串
    - `.toString()` 方法可以将 `symbol` 转为字符串显示
    - 访问 `.description` 属性可以显示 symbol 名的字符串
- `symbol` 值可以作为对象的“隐藏”属性，这种属性无法被意外访问或重写
- `symbol` 属性不参与 `for...in` 循环
- `Object.key(obj)` 会忽略 `symbol` 属性，而 `Object.assign()` 会同时复制字符串和 `symbol` 属性 
- 全局 symbol 注册表：每次访问该表内相同名字的 symbol 时都会返回相同的 symbol，做到同名的 symbol 是相同的 symbol
    - `Symbol.for("name")`：访问全局注册表内名为 `name` 的 `symbol` 值，如果存在则读取出来，否则在注册表内创建该 `symbol`
    - `Symbol.keyfor(sym)`：在全局注册表中查找 `symbol` 变量的 symbold 名（键），对于非全局 symbool 则返回 `undefined`

``` js
// Symbol.for() 用法
let id = Symbol.for("id");
let idAgain = Symbol.for("id");
alert (id === idAgain)  // ture

// Symbol.keyfor() 用法
let globalSymbol = Symbol.for("name");
let localSymbol = Symbol("name");

alert(Symbol.keyFor(globalSymbol)); // name
alert(Symbol.keyFor(localSymbol));  // undefined
```

- 系统 symbol，例如 `Symbol.hasInstance`、`Symbol.toPrimitive` 等等，具体见这个[规范](https://tc39.es/ecma262/#sec-well-known-symbols)，后面的章节也会介绍一些常用的系统 symbol
 
### 对象 -> 原始值转换

对象 -> 原始值转换的几种情况（后面三种转换被称为 hint）：

- 所有对象在**布尔**表达式中均被视为 `true`
- **数字**转换
    - 显示转换：`Number(obj)`
    - 数学运算：比如 `Date` 对象之间做减法，比较运算等
    - 使用内建的数学函数
- **字符串**转换
    - 使用 `alert(obj)` 输出对象内容
    - 将对象作为属性键：`anotherObj[obj] = 123`
- `default` 转换，当 JS 无法确定进行哪一类转换时采用这种转换，往往是运算符不适合用于对象的情况（比如两个对象相加，或者将对象与其他类型做 `==` 比较等）

JS 的转换流程：

1. 如果 `obj[Symbol.toPrimitive](hint)` 方法存在的话（需要我们自己声明）则调用它
    - `Symbol.toPrimitive` 是一种内建 symbol，它的作用是给转换方法命名，格式为：

    ``` js
    obj[Symbol.toPrimitive] = function(hint) {
        // hint = "stirng" | "number" | "default" 三者之一
        // 这里是将对象转换为原始值的代码
        // 必须返回一个原始值
    }
    ```

    ??? example "例子"

        ``` js
        let user = {
            name: "John",
            money: 1000,

            [Symbol.toPrimitive](hint) {
                alert(`hint: ${hint}`);
                return hint == "string" ? `{name: "${this.name}"}` : this.money;
            }
        };

        // 转换演示：
        alert(user);       // hint: string  -> {name: "John"}
        alert(+user);      // hint: number  -> 1000
        alert(user + 500); // hint: default -> 1500
        ```

2. 否则若 hint 是 `string`，则先尝试调用 `obj.toString()`，后尝试调用 `obj.valueOf()`
3. 否则若 hint 是 `number` 或 `default`，则先尝试调用 `obj.valueOf()`，后尝试调用 `obj.toString()`
    - `.toString()` 方法返回一个字符串 `"[object Object]"`
    - `.valueOf()` 方法返回对象自身
    - 这两个方法可以进行自定义

    ``` js
    let user = {
        name: "John",
        money: 1000,

        // 对于 hint="string"
        toString() {
            return `{name: "${this.name}"}`;
        },

        // 对于 hint="number" 或 "default"
        valueOf() {
            return this.money;
        }
    };
    ```


### JSON

JSON（JS 对象表示法）是基于 JS 对象语法的数据格式，但它独立于 JS 存在（因此在很多别的语言也可以读取和生成 JSON）。它是一个字符串，其格式非常类似 JS 对象字面量的格式。

``` json
{
  "squadName": "Super hero squad",
  "homeTown": "Metro City",
  "formed": 2016,
  "secretBase": "Super tower",
  "active": true,
  "members": [
    {
      "name": "Molecule Man",
      "age": 29,
      "secretIdentity": "Dan Jukes",
      "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
    },
    {
      "name": "Madame Uppercut",
      "age": 39,
      "secretIdentity": "Jane Wilson",
      "powers": [
        "Million tonne punch",
        "Damage resistance",
        "Superhuman reflexes"
      ]
    },
  ]
}
```

- 访问 JSON 对象和访问一般对象的方法一致（点表示法/方括号表示法）
- JSON 字符串外部还可以套个方括号，形成 JSON 数组，用数组索引访问数组元素

``` json
[
  {
    "name": "Molecule Man",
    "age": 29,
    "secretIdentity": "Dan Jukes",
    "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
  },
  {
    "name": "Madame Uppercut",
    "age": 39,
    "secretIdentity": "Jane Wilson",
    "powers": [
      "Million tonne punch",
      "Damage resistance",
      "Superhuman reflexes"
    ]
  }
]
```

- JSON 是一种纯数据格式，只包含属性，没有方法
- JSON 要求在字符串和属性名周围使用**双引号**，不得用单引号
- 只有带双引号的字符串才能作为 JSON 属性（所以转为 JSON 的属性自动添加双引号）
- JSON 的值可以是数字、带双引号的字符串、布尔值、数组等，不能是函数
- JSON 不支持注释
- 关于 JSON 的函数
    - `JSON.stringify(value[, replacer, space])`：将对象转换为 JSON 字符串，这个过程被称为序列化(serialization)
        - `value` 包括：对象，数组，甚至基本类型（字符串、数字、布尔值、`null`）
        - `replacer`：（可选）表示要被转换的属性数组或映射函数 `function(key, value)`，只有这些指定的属性才能被转换
            - 若属性数组过长，可用自定义的映射函数制定规则，排除不要的属性

            ??? example "例子"

                ``` js
                let room = {
                number: 23
                };

                let meetup = {
                title: "Conference",
                participants: [{name: "John"}, {name: "Alice"}],
                place: room // meetup 引用了 room
                };

                room.occupiedBy = meetup; // room 引用了 meetup

                alert( JSON.stringify(meetup, function replacer(key, value) {
                alert(`${key}: ${value}`);
                return (key == 'occupiedBy') ? undefined : value;
                }));

                /* key:value pairs that come to replacer:
                :             [object Object]
                title:        Conference
                participants: [object Object],[object Object]
                0:            [object Object]
                name:         John
                1:            [object Object]
                name:         Alice
                place:        [object Object]
                number:       23
                occupiedBy: [object Object]
                */
                ```

        - `space`：（可选）优化格式化的空格数量，是一个整数值（如果值为2，嵌套对象内部缩进 2 个空格）
        - 一些特定的 JS 属性会被 `JSON.stringify` 跳过，包括：函数（方法）属性、`Symbol` 类型的键和值、存储 `undefined` 的属性
        - 支持嵌套对象转换
        - 不能转换有循环引用（两个对象互有一个来自对方的属性）的对象
        - 对象内部提供 `toJSON` 进行 JSON 转换，`JSON.stringify` 会自动调用它。我们也可以自定义 `toJSON`
        
    - `JSON.parse(str[, reviver])`：将 JSON 字符串转换为对象
        - `str`：JSON 字符串
        - `reviver`：（可选）函数 `function(key, value)`，为每个 JSON 键值对调用，并可以对值进行转换
        
        ??? example "例子"

            ``` js
            let schedule = `{
            "meetups": [
                {"title":"Conference","date":"2017-11-30T12:00:00.000Z"},
                {"title":"Birthday","date":"2017-04-18T12:00:00.000Z"}
            ]
            }`;

            schedule = JSON.parse(schedule, function(key, value) {
            if (key == 'date') return new Date(value);
            return value;
            });

            alert( schedule.meetups[1].date.getDate() ); 
            ```

---
??? bug "JS 抽象行为大赏"

    - `typeof null` 的返回值为 `object`
    - `0 == "0" -> true`（因为`"0"` 被转为数字 `0` 了）
    - `0 == '' -> true`（原因同上） 
    - `null == undefined -> true`（原因同上）
    - `null >= 0 -> true  null == 0 -> false`（前者原因同上，后者因为在相等比较中 `null` 不会转化为数字）
    - `0.1 + 0.2 == 0.3 -> false`（JS 无法精确存储小数，这是很多语言的通病）
    - `NaN === NaN -> false`（每个 `NaN` 值都是独一无二的）
    - `[] == [] -> false`（JS 认为这两个数组是不同的对象，只有对同一个数组的引用才是相等的）