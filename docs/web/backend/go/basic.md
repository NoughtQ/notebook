---
counter: ture
---

# Go 基本语法

## 基础

- 基本指令
    - `go run test.go`：编译 + 运行
    - `go build test.go`：生成编译后的二进制文件 `test`，运行该文件还需再执行 `./test` 命令
- 包：本质上是一个目录，里面包含一个或多个 .go 源程序，或者其他的包
     - 如果某个包内的变量、函数等要被其他包引用，需要在命名时首字母大写，否则只能在包内（包括包内的其他文件，不需要 `import`）使用
     - 包的类型：
        - Go 标准库自带的包
        - 第三方包
        - 项目内部的包
        - 其他项目的包
     - 导入包：
        - 单个包：`import "packageName"`
        - 多个包：`import( "pack1", "path/to/pack2", ...)`
        - 为包创建别名：
            ``` go
            import (
                newName "pack1"
            )
            // 之后可用 newName.xxx 访问 pack1 包内的成员
            ```

            - 如果 `newName` 为一个 `.`，那么后续无需再使用点表示法访问成员，前面不用跟包的名称了

     - 包中的源码均以 `package packageName` 开头，其中 `packageName` 表示导入路径的最后一个元素



## 变量

- 基本数据类型
    ```
    int int8 int16 int32 int64
    uint uint8 uint16 uint32 uint64 uintptr

    byte  // uint8 别名

    rune  // int32 别名，表示一个 Unicode 码位

    float32 float64

    complex64 complex128  // 复数

    bool

    string
    ```
    
    - `int`、`uint`、`uintptr` 在 32 bit 系统上为 32 bit，在 64 bit 系统上为 64 bit
    - 平时应使用 `int` 类整数，除非有特殊情况
    - 复数
        - `complex64`：实部和虚部都是 `float32` 类型的值
        - `complex128`：实部和虚部都是 `float64` 类型的值
        - 虚部为 1 时，1 不可省略
        ``` go
        var v complex64 = 1 + 1i
        ```
    - 字符串
        - 访问字符串：`str[index]` / `for...range` 循环
        - `len(str)`：获取字符串长度
        - 不能直接修改字符串的字符，除非对整个字符串重新赋值
        - 也不能获取字符串某个字符的地址
        - 字符串也有类似[切片](#复杂类型)的操作（`str[low: high]`），但和切片不同之处在于：对截取的部分字符串的修改不会影响原字符串，而对部分切片的修改会改变原切片的值
        - [Cheat Sheet](https://yourbasic.org/golang/string-functions-reference-cheat-sheet/)
    - `reflect.Typeof(var)` 或在 `fmt.Println()` 使用 `%T` 占位符打印来查看变量 `var` 的类型
- `var` 语句用于声明一系列变量
    - 全局变量：函数外定义的变量，允许声明后不使用。有以下声明方法：
        ``` go
        // 法1
        var name type = value
        // 法2（注意：这样声明的变量只能在函数内赋值，不能在全局范围内赋值）
        var name type
        // 法3
        var name = value
        // 法4（不常用）
        var (
            name1 type1 = value1
            name2 type2
            name3 = value3
            // ...
        )
        ```

        - 作用域：整个包，甚至可以作为外部包的成员用于其他程序中
    - 局部变量：函数内定义的变量（包括函数的参数和返回值），**声明后必须使用**，否则编译报错。有以下使用方法：
        ``` go
        // 前面提到的 4 种方法均可采用
        // 法5（短变量声明，由程序自行推断变量类型）
        name := value
        // 法6（其实还是法2）
        var name type
        name = value
        ```

        - 作用域：函数内部
        - 局部变量可以“隐藏”全局同名变量
- 零值：没有明确初始值的变量会自动赋予一个对应类型的零值
    - 数值类型：0（复数是 0 + 0i）
    - 布尔型：`false`
    - 字符串型：`""`
    - 指针、切片、映射、函数、通道、接口：`nil`
    - 结构体：每个字段都有对应类型的零值
- 类型转换 `T(exp)`，将表达式 `exp` 的值转为类型 `T`
    - 不同类型的变量赋值时需要这种显式类型转换
- 常量 `const`
    - 声明的同时必须赋值，之后值无法修改
    - 不能用 `:=` 声明
    - 声明后可以不用（无论全局还是局部），不会报错
    - 枚举
        - `iota`：特殊常量，用于由常量构成的「枚举」，作为索引值（从 0 开始）
        - 如果枚举中某个常量未赋值
            - 若它的前一个常量值是 `iota`，则它的值为该常量值 + 1
            - 否则它的值等于前一个常量值
    ``` go
    // 实现类似 C 语言的枚举
    const (
        c1 = iota // 0
        c2  // 0
        c3 = iota // 2
        c4 // 3
        c5 = "abc" 
        c6 // "abc"
        c7 = iota // 6
    )
    ```
- 运算符
    - 算术运算符：+、-、*、/、%、++、--
    - 关系运算符：==、!=、>、>=、<、<=
    - 逻辑运算符：&&、||、!
    - 位运算符：&、|、^（异或、**取反**均为该运算符）、<<、>>、&^（）
    - 赋值运算符：=、+=、-=、*=、/=、%=、<<=、>>=、&=、^=、|=
    - 优先级：

    ``` 
    Precedence    Operator
        5             *  /  %  <<  >>  &  &^
        4             +  -  |  ^
        3             ==  !=  <  <=  >  >=
        2             &&
        1             ||
    ```


## 控制流

!!! warning "所有控制语句的大括号都是必需的"

### 条件语句

- `if` 判断
    - 类似 `for` 循环：条件表达式可以不加括号，大括号是必需的
    - 可以在条件表达式前先执行一条简短的语句，该语句声明的变量作用域仅在 `if` 语句之内
    ``` go
    if v:= math.Pow(x, n); v < lim {
        return v
    }
    ```
    
    - `else` 和 `if else` 语句同 C 语言
    - 在 `if` 简短语句声明的变量在所有分支中均可使用
- `switch` 分支
    ``` go
    switch os := runtime.GOOS; os{
        case "darwin":
            fmt.Println("macOS.")
        case "linux"
            fmt.Println("Linux.")
        default:
            fmt.Println("%s.\n", os)
    }
    ```
    - 与 C 语言的不同：
        - 和 `if` 语句一样也可以在条件表达式前有一个简单的声明语句，作用域在 `switch` 语句内
        - 可以省略 `switch` 条件（同 `switch true`）
        - 只会执行其中一个 `case` 分支，而不会继续执行后面的所有分支（相当于 C 语言中自动为每个分支加上 `break`）
            - 如果想要继续执行后面的分支，可以在分支后面加 `fallthrough` 关键词（当然后面的分支没有 `fallthrough` 的话就会在该分支停止）
        - `case` 的值无需是常量，且不限于整数

>注：没有三目运算符`?`

### 循环语句

- `for` 循环
    ``` go
    for i := 0; i < 10; i++ {
        sum += i
    }
    ```
    - 由三部分构成：初始化语句、条件表达式、后置语句（类似去括号版的 C 语言 `for` 循环）
        - 初始化语句和后置语句是可选的（分号可去掉）
    - 只保留条件表达式的循环可视为（C 语言的）while 循环
    ``` go
    for sum < 1000 {
        sum += sum
    }
    ```

    - 省略这三者会形成一个死循环
    - `break`：跳出当前循环，`continue`：进入下一轮循环
- `range` 迭代：适用于字符串、数组、切片、集合或通道
``` go
// 以遍历字符串为例
// 用法1：仅获取索引
// (1)
for index, _ := range str {
    // ...
}
// (2)
for index := range str {
    // ...
}

// 用法2：仅获取值
for _, value := range str {
    // ...
}

// 用法3：索引 + 值
for index, value := range str {
    // ...
}
// 
```

``` go
label: statement
goto label
```

### defer
        
`defer` 推迟：用于函数或方法调用前，使该函数或方法在外层函数返回之后再执行

``` go
defer fmt.Println("hello")
```

- 被 `defer` 的函数的参数值在执行到 `defer` 语句时就被确定下来了
- 若函数内调用多次 `defer`，则在该函数返回前，按照 LIFO 原则，先 `defer` 的函数后执行，后 `defer` 的函数先执行
- 用途：用于成对的操作，比如文件的开关，锁的创建和释放等
- 如果函数因调用 `os.Exit()` 退出，那里面的 `defer` 就不会执行了 


## 函数

- 函数定义：

``` go
func name([parameter list]) [return_type] {
    // ...
}

// 举例：
// 有四个参数，两个返回值
func name(a, b int, c, d string) (int, string) {
    // ...
}
```

- 所有源文件都需要有一个 `main()` 函数作为主程序（且在开头声明 `package main`），否则程序无法通过编译
- 当参数类型相同时，可以只保留最后一个类型（比如 `x int, y int` 可简写为 `x, y int`）
- 函数可以同时返回多个值（比如 `return x, y`），
- 可以为返回值命名（介于函数名和参数列表之间），但是要同时为所有返回值都命名，部分命名会报错
``` go
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return
}
```

- 空函数：`var f func()`，它的值为 `nil`，执行该函数会报错
- 函数传参**只有值传递**一种类型，**没有引用传递**！
    - 虽然形参可以是指针，能够改变传入的参数值，但它本质上是**拷贝了该参数的地址**，所以还是一种值传递
- 函数也可以像值一样传递，比如将函数赋给某个变量，作为其他函数的参数或返回值等
- 递归函数：同 C 语言
- 函数闭包：引用函数体之外的变量的函数（简单理解为“定义在一个函数内部的函数”，是一种匿名函数），这类函数被绑定在变量上，从而使变量的值始终保存在内存中

??? example "例子"

    ``` go
    package main

    import "fmt"

    func adder() func(int) int {
        sum := 0
        // 返回一个闭包，被绑定在外面的 sum 变量上
        // 所以 sum 直到程序结束前不会消失
        return func(x int) int {
            sum += x
            return sum
        }
    }

    func main() {
        // 创建 2 个独立的闭包
        pos, neg := adder(), adder()
        for i := 0; i < 10; i++ {
            fmt.Println(
                pos(i),
                neg(-2*i),
            )
        }
    }
    ```

- `init` 函数
    - 无参数、无返回值
    - `init` 函数不能被显式调用，在 `main` 函数执行前自动调用
    - 一个包里可以有多个 `init` 函数，调用顺序不确定
    - 无论某个 `init` 函数被多少个包导入，在程序中只调用一次 
    
        
## 复杂类型

### 指针

- 声明
``` go
var var_name *var_type
```

- 其零值为 `nil`
- 与指针相关的运算符
    - `&` 操作符：取变量的内存地址，即指向该变量的指针
    ``` go
    i := 42
    p := &i
    ```

    - `*` 操作符：解引用操作，即获取指针指向的底层值
    ``` go
    *p = 21
    ```

- 指针数组
``` go
var ptr [SIZE]*type_name
```
- 多重指针
``` go
var val int = 100
var ptr1 *int = &a
var ptr2 **int = &ptr1
var ptr3 ***int = &ptr2
```

- 与 C 语言不同的地方
    - 数组名不是指向数组首元素的地址
    - 指针没有算术运算

### 结构体

结构体 `struct`：可看作一组字段

- 声明和初始化
``` go
type struct_name struct {
    mem1 type1
    mem2 type2
    mem3, mem4 type3
}

// 初始化
// 法1：全体成员赋值
v := struct_name{val1, val2, val3, val4}
// 法2：部分成员赋值（未赋值的成员值为零值）
v := struct_name{mem1: val1, mem4: val4}
```

- 结构体指针
``` go
var struct_ptr *struct_name
struct_pointer := &v
```

- 成员访问运算符 `.`
    - 不同于 C 语言，即使是指向结构体的指针也是用 `.` 访问成员（隐式解引用）
- [方法](#方法)：为结构体定义方法，可以使结构体类似 C++ 的类
- 如果结构体要被外部包使用，那么该结构体及其成员的名称开头需大写
- 标签(tag)：结构体字段后面可以跟一个可选的字符串，作为相应字段的属性，这被称为标签
    - 一个标签可用于多个字段
    - 设置空标签和不使用标签的效果相同
    ``` go
    type T struct {
        f1     string "f one"
        f2     string
        f3     string `f three`
        f4, f5 int64  `f four and five`
    }
    ```

    - 使用 `reflect` 包来访问结构体的标签
    ``` go
    func main() {
        t := reflect.TypeOf(T{})
        f1, _ := t.FieldByName("f1")
        fmt.Println(f1.Tag) // f one
        f4, _ := t.FieldByName("f4")
        fmt.Println(f4.Tag) // f four and five
        f5, _ := t.FieldByName("f5")
        fmt.Println(f5.Tag) // f four and five
    }
    ```

    - 相关方法（注意标签需要用双引号包裹，反引号包裹的标签无法使用）
        - `Lookup()` 函数：返回两个值——与键关联的值和表示是否找到键的布尔值
        ``` go
        type T struct {
            f string `one:"1" two:"2"blank:""`
        }
        func main() {
            t := reflect.TypeOf(T{})
            f, _ := t.FieldByName("f")
            fmt.Println(f.Tag) // one:"1" two:"2"blank:""
            v, ok := f.Tag.Lookup("one")
            fmt.Printf("%s, %t\n", v, ok) // 1, true
            v, ok = f.Tag.Lookup("blank")
            fmt.Printf("%s, %t\n", v, ok) // , true
            v, ok = f.Tag.Lookup("five")
            fmt.Printf("%s, %t\n", v, ok) // , false
        }
        ```


        - `Get()` 函数：仅返回与键关联的值
        ``` go
        func (tag StructTag) Get(key string) string {
            v, _ := tag.Lookup(key)
            return v
        }
        ```

    - 将结构体转换为其他类型的结构体时要求底层类型相同，但在转换过程中会忽略掉标签

### 数组、切片

- 声明：
    ``` go
    var variable_name [size]variable_type

    // e.g.
    var a [10]int  // 10 个整数数组
    ```

    - 数组一旦声明，长度便固定下来
- 字面量：`[n]T{x1, x2, ..., xn}`，其中长度 `n` 可以省略，`x1` 到 `xn` 为 n 个 `T` 类型的值
    - 可以不直接指出长度，用 `...` 替代 `n`，由编译器自行推断
    - 在数组长度已知的情况下，可以根据索引指定对应的元素值
    ``` go
    balance := [5]int{1: 10, 3:30}
    // balance == [0, 10, 0, 30, 0]
    ```

- 访问数组
    - 下标法
    - `range` 遍历：用于 `for` 循环
        - 每次迭代都会返回两个值，分别是索引和对应索引下的元素副本
        ``` go
        pow := []int{1, 2, 4, 8}

        for i, v := range pow {
            // ...
        }
        ```

        - 可以使用空白标识符 `_` 忽略不想获取的值
        ``` go
        for i, _ := range pow {
            // ...
        }

        for _, value := range pow {
            // ...
        }
        ```

        - 如果只需要索引，可以直接忽略第二个变量
        ``` go
        for i := range pow {
            // ...
        }
        ```

- `len(s)`：获取数组长度
- 多维数组
``` go
var variable_name [size1][size2]...[sizeN]variable_type
```
- 数组作为参数
    - 形参必须指定长度（`[N]type`），且实参的长度必须与形参相同，否则报错
    - 若要改变数组内容，需要将数组指针作为参数（`*[N]type`），实参为数组的地址（`&array`）
    - 如果没有指定长度（`[]type`），那就是切片参数，不是数组啦
- 切片：数组的一种抽象
    - 切片的底层数据结构
        ``` go
        type slice struct {
            array unsafe.Pointer // 指向底层数组的指针
            len int              // 切片长度
            cap int              // 切片容量
        }
        ```

        - 所以对切片的修改就是对底层数组的修改
    - 声明和初始化
    ``` go
    var slice_var []type
    // make() 函数，容量参数可选
    var slice_var []type = make([]type, len[, cap])
    // 字面量
    slice_bar := []type{}
    ```

    - 零值为 `nil`，此时长度和容量均为0且没有底层数组
    - 访问：同数组
    - 截取（类似 Python）
        - `a[low: high]`，获取索引值在 `low` 到 `high - 1` 之间的数组元素。截取到的切片有一个指向原数组的指针，所以修改切片也会修改该数组
        - 可以省略切片的上下界，下界默认为 0，上界默认为数组长度
        ``` go
        // 这 4 个切片等价
        a[0: 10]
        a[: 10]
        a[0: ]
        a[:]
        ```
    - 常用函数
        - `len(s)`：获取切片长度
        - `cap(s)`：获取切片容量（从它的第一个元素开始，到其底层数组元素末尾的个数）
        - `append(s, x1, x2, ...)` 函数：向切片 `s` 后面附加 `x1` 等同类型的元素，返回值新添加元素后的切片
            - 如果加入元素太多超出容量，程序会分配一个更大的数组
            - 只能用于切片，不能用于数组
        - `copy(dstSlice, srcSlice)`：将 `srcSlice` 切片的元素拷贝到另一个切片 `dstSlice` 内
            - 若 `len(dstSlice) < len(srcSlice)`，则只会拷贝 `srcSlice` 中前 `len(dstSlice)` 个元素
            - 若 `len(dstSlice) == 0`，那么不会拷贝任何元素
    - 多维切片：每一维的切片大小可以不同
    - 切片作为参数
        - 切片传参有**类似引用传递**的效果——无需指针也可以在函数内修改切片的值（当然也会修改底层函数的值）（记住本质上还是值传递，只是因为切片有一个指向底层数组地址的指针）
        - 但是如果在函数体内使用 `append()` 为切片添加新元素，则不会改变外部切片的值


### 映射

映射 `map`：将键映射到值上，是一组无序的键值对（类似 Python 字典）

- 键必须支持 `==` 和 `!=` 比较，因此切片、函数、映射不能作为键
- 声明和初始化
``` go
// 法1
var map_var map[key_type]value_type = map[key_type]value_type{}
// 法2
// 花括号内可以像结构体那样指定字面量
map_var := map[key_type]value_type{}
// 法3
map_var := make(map[key_type]value_type[, cap])
```

- 零值：`nil`，此时既没有键，也不能添加键
- 若映射的值的类型是一样的，那么可以在字面量的元素中省略它们（在上例中就是将两个键后面的 `Vertex` 去掉）
- 插入/修改元素：`m[key] = elem`
- 获取元素：`elem = m[key]`
- 删除元素：`delete(m, key)`
    - 允许删除不存在的键，不会报错
- 检查某个键是否存在：`elem, ok = m[key]`
    - 若在 `ok` 为 `true`
    - 否则为 `false`，此时 `elem` 为该类型的零值，且不会插入新的元素
    - 如果 `elem` 和 `ok` 在之前未声明，请使用 `:=` 短变量声明
- 元素个数：`len(m)`
- 映射作为函数形参，可以在函数体内改变外部实参的值
    

## 方法和接口

### 方法

方法：虽然 Go 没有类，但是可以为任意类型（一般是自定义类型或结构体）定义方法——这是一类带特殊的**接收者**(receiver)参数的函数

- 接收者位于 `func` 和方法名之间，有一个自己的参数列表
``` go
type Vertex struct {
    X, Y float64
}

func (v Vertex) Abs() float64{
    return math.Sqrt(v.X * v.X + v.Y * v.Y)
}
```

- 接收者的类型定义和方法声明必须位于同一个包内
- 接收者参数可以是指针类型的，这样就可以在方法内修改接收者的值了。调用方法时接受者既可以是指针，也可以是值（此时会自动转化为指针（`&x`））
- 接收者参数是一般的值时，调用方法时接收者也可以是一般值或指针（此时会自动转化为值（`*p`））
>推荐用**指针**接收者参数：不仅可以修改接收者的值，而且避免拷贝占用大量内存
- 将方法修改为一般函数：将接收者放入参数列表内即可

### 接口

接口(interface)：可理解为一组仅包含方法的集合

- 声明（隐式实现）：接口的实现（方法）可以出现在任何包内，且无需在每个实现上增加新的接口名称
``` go
package main

import (
    "fmt"
    "math"
)

type Abser interface {
    Abs() float64
}

func main(){
    var a Abser
    f := MyFloat(-math.Sqrt2)
    // v := Vertex{3, 4}

    a = f
    // a = &v
    fmt.Println(a.Abs())
}

type MyFloat float64

func (f MyFloat) Abs() float64 {
    if f < 0 {
        return float64(-f)
    }
    return float64(f)
}

type Vertex struct {
    X, Y float64
}

func (v *Vertex) Abs() float64{
    return math.Sqrt(v.X * v.X + v.Y * v.Y)
}
```

- 多个类型可以共用一个接口，一个类型可以使用多个接口
- 接口可嵌套
- 接口也是值，可以像值一样传递，作为函数的参数或返回值。具体来说，接口值保存了包含值和类型的元组 `(value, type)`
    - 不要误会，还是得把接口值看作单个值，只是它有两种表现形式，既可以表示底层类型的值，也可以表示当前所指类型
    - 如果底层值为 `nil`（接口自身不为 `nil`），方法仍然会被 `nil` 接收者调用而不会报错
    - 如果接口自身为 `nil`，那么它既不保存值也不保存类型，这会产生运行时错误
- 空接口：没有指明方法的接口 `interface{}`，可保存任何类型的值，因此可以用来存储未知类型的值
- 类型断言(type assertion)：用于访问接口的底层值
    - `t := i.(T)`：接口 `i` 保存了类型为 `T` 的底层值（若类型不对就会报错），将其赋给 `t`
    - `t, ok := i.(T)`：用 `ok` 检查 `i` 是否保存类型为 `T` 的底层值，若是 `ok` 为 `true`，否则为 `false`，但是此时不会报错
    - 类型选择(type switches)：根据类型断言来选择分支，类似 `switch` 语句（此时的 `case` 为类型而不是值）
    ``` go
    switch v := i.(type) {
        case T:
            // v 的类型为 T
        case S:
            // v 的类型为 S
        default:
            // 没有匹配，v 与 i 类型相同
    }
    ```

- 常用接口
    - `fmt` 包的 `Stringer` 接口，定义了将其他类型转为字符串的方法
    ``` go
    type Stringer interface {
        String() string
    }
    ```

    ??? example "例子"

        ``` go
        package main

        import "fmt"

        type Person struct {
            Name string
            Age  int
        }

        func (p Person) String() string {
            return fmt.Sprintf("%v (%v years)", p.Name, p.Age)
        }

        func main() {
            a := Person{"Arthur Dent", 42}
            z := Person{"Zaphod Beeblebrox", 9001}
            fmt.Println(a, z)
        }

        // Output:
        // Arthur Dent (42 years) Zaphod Beeblebrox (9001 years)
        ```

    - `error` 接口：定义了处理错误情况的方法。通常函数会返回一个 `error` 值，如果值为 `nil` 表示成功，否则表示失败，需要有对应的错误处理
    ``` go
    type error interface {
        Error() string
    }
    ```

    ??? example "例子"

        ``` go
        package main

        import (
            "fmt"
            "time"
        )

        type MyError struct {
            When time.Time
            What string
        }

        func (e *MyError) Error() string {
            return fmt.Sprintf("at %v, %s",
                e.When, e.What)
        }

        func run() error {
            return &MyError{
                time.Now(),
                "it didn't work",
            }
        }

        func main() {
            if err := run(); err != nil {
                fmt.Println(err)
            }
        }

        // Output:
        // at 2009-11-10 23:00:00 +0000 UTC m=+0.000000001, it didn't work
        ```

    - `io` 包的 `Reader` 接口，表示数据流的读取端
        - `io.Reader` 接口有一个 `Read` 方法
        ``` go
        func (T) Read(b []byte) (n int, err error)
        // 用数据填充给定的字节切片并返回填充的字节数和错误值
        // 遇到数据流的结尾时会返回一个 io.EOF 的错误
        ```

    ??? example "例子"

        ``` go
        package main

        import (
            "fmt"
            "io"
            "strings"
        )

        func main() {
            r := strings.NewReader("Hello, Reader!")

            b := make([]byte, 8)
            for {
                n, err := r.Read(b)
                fmt.Printf("n = %v err = %v b = %v\n", n, err, b)
                fmt.Printf("b[:n] = %q\n", b[:n])
                if err == io.EOF {
                    break
                }
            }
        }

        // Output（每次读取 8 Byte 信息）:
        // n = 8 err = <nil> b = [72 101 108 108 111 44 32 82]
        // b[:n] = "Hello, R"
        // n = 6 err = <nil> b = [101 97 100 101 114 33 32 82]
        // b[:n] = "eader!"
        // n = 0 err = EOF b = [101 97 100 101 114 33 32 82]
        // b[:n] = ""
        ```

    - `image` 包的 `Image` 接口

        ``` go
        package image

        type Image interface {
            ColorModel() color.Model
            Bounds() Rectangle
            At(x, y int) color.Color
        }
        ```

        - `color.Color` 和 `color.Model` 也是接口，但通常使用它们的预定义实现（`image.RGBA` 和 `image.RGBAModel`）因而忽略这一本质

## 泛型

- 类型参数(type parameters)
    - 类型参数列表：`[P, Q constraint1, R constraint2]`
        - 其中 `P, Q, R` 都是类型参数，`constraint1, constraint2` 都是类型限制
        - 类型参数列表介于函数名和参数列表之间
        - 不能用于方法，只能用于函数
        
    
    ??? example "例子"

        ``` go
        func min[T constraints.Ordered] (x, y T) T {
            if x < y {
                return x
            }
            return y
        }

        // 调用泛型函数
        m := min[int](2, 3)
        ```

    - 实例化(instantiation)：在泛型函数的基础上生成一个非泛型函数，用于真正的函数执行，实现过程如下：
        - 把泛型函数的类型参数替换为类型实参（比如将类型参数 `T` 替换为 `int`）
        - 检查类型实参是否满足泛型函数定义的类型限制
        - 若任何一步失败，泛型函数调用失败
    - 类型参数除了用于泛型函数外，还用于创建泛型类型(generic types)
    
    ??? example "例子"

        ``` go
        // 实现一个泛型二叉树结构
        type Tree[T interface{}] struct {
            left, right *Tree[T]
            data T
        }

        func (t *Tree[T]) Lookup(x T) *Tree[T] 

        var stringTree Tree[string]
        ```

- 类型集(type sets)：类型参数的类型限制包含多个具体类型，这些具体类型构成了类型集，泛型函数只支持这些类型
    - 举例：类型限制 `constraints.Ordered` 包含如下具体类型：
    ``` go
    type Ordered interface {
        Integer | Float | ~string
        // Integer 和 Float 也是定义在 constraints 包里的类型限制
    }
    ```

    - 类型限制必须是 `interface` 类型
    - 类型限制相关的符号
        - `|`：取并集（上面的例子中就用到了）
        - `~T`：表示底层类型是 `T` 的所有类型
        
        ??? example "例子"

            ``` go
            // 字面意思，表示限定所有底层类型为字符串的类型
            type AnyString interface{
            ~string
            }
            ```

    - 类型限制字面量：可以直接在类型限制列表里现场定义类型限制
        - `interface{E}` 可简写为 `E`
        - `any` 可作为 `interface{}` 的别名，表示支持任意类型

        ``` go
        [S interface{~[]E}, E interface{}]

        [S ~[]E, E interface{}]

        [S ~[]E, E any]
        ```


- 类型推导(type inference)：在调用泛型函数时，可以不指定（全部或部分）类型实参，由编译器根据传入的函数实参（或部分已知的类型参数）来推导出类型实参，这样使代码更简洁
    ``` go
    func min[T constraints.Ordered] (x, y T) T {
        if x < y {
            return x
        }
        return y
    }

    var a, b, m1, m2 float64
    // 不指定类型参数，让编译器进行类型推导
    m2 = min(a, b)
    ```

    - 类型推导不一定成功，比如类型参数用于函数的返回值，或者用于别的函数内

???+ question "何时用泛型"

    - `slice`、`map`、`channel` 里的元素类型较多
    - 设计通用的数据结构，比如链表、二叉树等
    - 当一个方法的实现逻辑对所有类型都一样时


## 并发编程

### goroutine、通道

- goroutine：一种轻量级的用户态线程，实现并发编程
    - 语法：`go` 后面跟函数调用，这样为该函数启用一个 goroutine
    - Go 为 main() 函数创建一个默认的 goroutine。如果 main() 函数运行结束，则所有在 main() 中启动的 goroutine 会立马结束
    
    ??? example "例子"

        ``` go
        package main

        import "fmt"

        func hello() {
            fmt.Println("hello")
        }

        func main() {
            go hello()
            fmt.Println("main end")
        }
        ```

        有以下几种可能的输出结果：

        - `main end`    
        - `main end`
        `hello`
        - `hello`
        `main end`

        因为 main() 函数的 goroutine 和 `hello()` 函数的 goroutine 是并发执行的，所以谁先谁后都有可能

    - goroutine 和闭包一起使用时需注意：避免多个 goroutine 闭包使用同一个变量
        - 可以为每个 goroutine 声明一个新变量来解决这一问题

- 通道(channel)：作为多个 goroutine 通信的“桥梁”，一个 goroutine 可以发送数据到指定通道，其他 goroutine 可以从该通道获取数据
    - 类似队列，满足 FIFO 原则
    - 零值为 `nil`，值为零值的通道不能用于通信
    - 声明和初始化
    ``` go
    // 法1
    // channel_size 表示通道的缓冲区容量，表示最多存放的元素个数（可选）
    // type 可以是数组、结构体等
    var channel_name chan type = make(chan type[, channel_size])

    // 法2
    channel_name := make(chan type[, channel_size])
    ``` 

    - 向通道发送值：`channel_name <- value`
    - 从通道接收值：`value = <-channel_name`
    - 关闭通道：`close(channel_name)`
        - 关闭空通道会报错
    - 通道缓冲区：用 `make` 函数声明时可以指定缓冲区容量，要考虑**阻塞**问题
        - 可用 `cap(channel_name)` 获取容量大小
        - 无缓冲区
            - 向通道发送值时，必须确保其他通道会从该通道接收值，发送才能成功
            - 从通道接收值时，必须确保其他通道会向该通道发送值，接收才能成功
        - 有缓冲区
            - 若缓冲区未满，那么发送方发送数据到通道缓冲区后，便可以继续往下执行，而无需等待接收方从通道接收数据
            - 若缓冲区已满，那么发送方发送数据到通道缓冲区后会阻塞，直到接收方从通道接收数据，缓冲区有空间存储发送方发送的数据时，发送发才能继续往下执行
    - 遍历通道（`for...range`）
        - 死循环读取通道
            - 若通道已关闭，那么继续从通道获取的值是对应类型的零值
            - 若通道未关闭，则会遇到阻塞报错

    ??? example "例子"
    
        ``` go
        package main

        import "fmt"
        import "time"


        func addData(ch chan int) {
            /*
            每3秒往通道ch里发送一次数据
            */
            size := cap(ch)
            for i:=0; i<size; i++ {
                ch <- i
                time.Sleep(3*time.Second)
            }
            // 数据发送完毕，关闭通道
            close(ch)
        }


        func main() {
            ch := make(chan int, 10)
            // 开启一个goroutine，用于往通道ch里发送数据
            go addData(ch)

            /* range迭代从通道ch里获取数据
            通道close后，range迭代取完通道里的值后，循环会自动结束
            */
            for i := range ch {
                fmt.Println(i)
            }
        }
        ```

    - 通道作为函数形参时，可以控制数据和通道之间的数据流向
        - 只读（仅可以从通道读取数据）：`<- chan type`
        - 只写（仅可以向通道写入数据）：`chan <- type`

## 错误处理

Go 用两套机制区分**错误**(error)和**异常**(panic)

- 错误：以返回值的形式返回
    - 通过多返回值的方式处理调用函数时发生的错误
    ``` go
    return_value, err := function(...)
    if err != nil {
        // ...
        return
    }
    ```

    - 也可以自定义方法来处理错误

- 异常：导致终止程序
    - `panic()` 函数：调用该函数直接抛出异常
        - 参数值可以是数字、字符串、函数
        - 如果参数是函数 F，那么会有以下行为
            - 执行 F 中被 `defer` 的函数
            - 如果 F 有上一级函数 E，E 也被视为异常，因此执行 E 中被 `defer` 的函数
            - 重复上一步，直至没有上一级函数
            - 程序终止
    - `recover()` 函数：用于捕获异常，必须结合 `defer` 才能生效
        - 如果当前 goroutine 出现异常，可以在代码适当位置调用 `recover()`，使程序继续正常执行而不停止
        - 函数返回 `nil` 的情况：
            - 没有异常发生
            - `panic()` 函数的参数为 `nil`
            - `recover()` 函数不是在被 `defer` 的函数里面被直接调用执行的

        ??? example "例子"

            ``` go
            package main

            import (
                "fmt"
            )

            func a() {
                defer func() {
                    /*捕获函数a内部的panic*/
                    r := recover()
                    fmt.Println("panic recover", r)
                }()
                panic(1)
            }

            func main() {
                defer func() {
                    /*因为函数a的panic已经被函数a内部的recover捕获了
                    所以main里的recover捕获不到异常，r的值是nil*/
                    r := recover()
                    fmt.Println("main recover", r)
                }()
                a()
                fmt.Println("main")
            }

            // Output:
            // panic recover 1
            // main
            // main recover <nil>
            ```

## 后端库相关

- [JSON](https://attilaolah.eu/2014/09/10/json-and-struct-composition-in-go/)

## 其他

### go get 命令相关

执行 `go get` 之前的准备工作：

- 配置 Go 的代理服务器（不配置的话很容易出现连接失败的问题）：前往[这个网站](https://goproxy.cn/)，按照步骤输入一些命令。之后用 `go env` 查看环境变量，若 `GOPROXY` 的值为该网址，说明配置成功。
- 在**源代码的同一目录中**执行 `go mod init xxx`（`xxx` 名称任意），创建一份 .mod 文件

做好这些准备工作后，再执行 `go get` 命令获取 Go 在线资源。

