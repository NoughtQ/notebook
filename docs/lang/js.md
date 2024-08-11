---
counter: true
---

# JavaScript

!!! abstarct "参考资料"

    - [现代 JavaScript 教程](https://zh.javascript.info/)
    - [MDN JavaScript 学习](https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript)
    - [Google JS 风格指南](https://google.github.io/styleguide/jsguide.html)

!!! info "一些有用的工具"

    - 开发者工具 - 控制台，[调试方法](https://zh.javascript.info/debugging-chrome)
    - [ESlint](https://eslint.org/)（自动检查器，检查代码风格）


## 基础知识

- 引入 JavaScript 脚本的方式：
    - 内部嵌入：使用 `<script>` 标签，里面直接写 JS 代码（仅适用于代码量少的情况，不推荐）
    - 外部导入：在 `<script>` 元素中使用 `src` 属性，它的值为 JS 外部文件的地址（本地或 URL 均可），此时会忽略标签内的任何内容。推荐用这种方法，因为浏览器会下载 JS 文件并保存到缓存中，下次打开网页无需再次下载，使页面加载更快
- 注释：同 C 语言
- 在 JS 代码开头添上 `"use strict";`，JS 将启用严格模式，使用新版本的特性，推荐使用
- 变量
    - `let` 关键字用于声明各种类型的变量
        - 推荐一行声明一个变量，方便阅读
        - 同一个变量声明两次会报错
        - 变量命名：类似 C 语言，但它还允许符号 `$`，且 `$` 和 `_` 在命名时被视为字母（~~甚至可以用中文，但别这么做~~）（[保留字列表](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#keywords)）
        - 推荐的做法：使用易读的名称，避免使用缩写，名称能够准确描述变量功能，为不同的值使用不同的变量
    - ~~`var`~~
    - `const` 关键字用于声明常量变量，这类变量无法被修改
        - 推荐的命名法：使用大写字母和下划线来命名，用于存储一些难以记住且确保不变的值
- 数据类型（可以使用 `typeof x` 运算符返回变量 `x` 的类型）
    - number：整数、浮点数，以及一些「特殊数值」：`Infinity`、`-Infinity`、`NaN`（计算错误），安全范围为 $-(2^{53} - 1) \sim (2^{53} - 1)$
    - bigint：任意长度的整数
    - string：可用单引号、双引号或反引号表示字符串
        - 但是反引号的字符串允许将变量或表达式传进去（还需使用 `${}` 包装，类似 Python） 
    - boolean：`true`、`false`
    - null：未知值
    - undefined：未定义的值（未被赋值...）
    - symbol：对象的唯一标识符
    - object：复杂的数据结构
- 类型转换
    - `String(value)` 将 `value` 转为字符串型
    - 数字型
        - 自动转换：算术运算
        - 显示转换：`Number(value)`，一些特殊规则：
            - `Number(undefined) -> NaN`
            - `Number(null) -> 0`
            - `Number(true) -> 1  Number(false) -> 0`
            - 字符串转数字会先去掉空白字符，若剩余部分为空返回0，若无法转为数字返回 `NaN`
    - 布尔型：`Boolean(value)`，除了 `0`、空字符串、`null`、`undefined`、`NaN` 返回 `false`，其余值都返回 `true` 
- 运算符（与 C 语言相同的部分就不再赘述，这里着重介绍 JS 特有的部分）
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
- 条件分支
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
- 循环（类似 C 语言）
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
- 交互
    - `alert(msg)` 函数：运行该函数后会显示一个名为模态窗(modal window)的东西，内容为 msg（字符串），直到点击“确定”按钮后用户才能与页面交互
    - `prompt(title, [default])`：显示内容为 `title` 的模态框，还有一个输入框和确认/取消按钮。它会将我们输入的内容作为函数返回值，如果点击取消或直接退出（`Esc`），返回值为 `null`
        - 第二个参数 `default` 可选，作为默认的输入内容出现在输入框上，推荐使用
    - `confirm(question)`：显示内容为 `question` 的模态框，带确认/取消按钮，点击确认返回 `true`，点击取消或直接退出返回 `false`
- 函数
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

## 对象

对象用于存储键值对或更复杂的实体。它是一个由花括号包起来的属性列表，一个属性就是一个键值对（`key:value`），键(key，又称属性名)是一个字符串，值(value)可以是任何值

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

- 方括号表示法（`obj["property"]`） vs `.` 表示法（`obj.property`）：

    - 属性名可以由多个单词构成，但需要用引号括起来，比如 `"likes birds": true;`。如果要访问这样的多词属性，需要用方括号替代 `.`，比如 `user["likes birds"]`。

    - 方括号访问元素比用 `.` 访问元素更加灵活，因为只要方括号内的表达式的值为键名（字符串），那么就可以成功访问该属性，而 `.`表示法就不能这样，比如：

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

    - 总结：`[]` 虽然强大但很麻烦，能够用 `.` 表示法就用它，实在不行用 `[]`

- 属性名的命名更加自由：只要不是保留字的字符都会被接受（~~甚至可以是一串数字~~），JS 会自动将名称转化为字符串
- 如果属性名和作为它对应值的变量的名称相同，则可以进行属性值简写，比如一个键值对 `name: name` 等价于 `name`
- `in` 操作符：判断属性是否存在，语法：`"key" in object`，其中 `key` 为属性名，`object` 为被检测的对象
- `for` 循环：`for (key in object) { ... }`，这样会遍历对象所有的键
- 属性的顺序问题：如果属性名是一个整数（只有数字字符），JS 会自动根据整数值进行升序排序，否则就按照创建时的顺序排序（对对象进行遍历的时候就会发现这个顺序）

- 对象引用：实际上，一个赋值了对象的变量并不是一个对象，它仅保存了该对象**在内存中的地址**，也就是该对象的**引用**。因此对于下列语句：

    ``` js
    let user = { name: "NoughtQ" };

    let admin = user;
    ```

    `admin` 和 `user` 是同一个对象的引用。如果用 `admin` 修改这个对象的属性，那么用 `user` 也可以访问该对象修改后的属性。

- `Object.assign`
    - 语法为 `Object.assign(dest, [src1, src2, src3...])`，其中 `dest` 是目标对象，后面的可选参数为源对象，该方法会将所有源对象的属性拷贝到目标对象内，最后返回 `dest`
    - 如果 `dest` 存在与源对象名称相同的属性，则该属性会被源对象的属性覆盖
    - 使用该方法实现浅拷贝：`let clone = Object.assign({}, obj)`
    >要实现深拷贝，需要用到 `.cloneDeep(obj)` 函数


??? bug "JS 抽象行为大赏"

    - `typeof null` 的返回值为 `object`
    - `0 == "0" -> true`（因为`"0"` 被转为数字 `0` 了）
    - `null == undefined -> true`（原因同上）
    - `null >= 0 -> true  null == 0 -> false`（前者原因同上，后者因为在相等比较中 `null` 不会转化为数字）
