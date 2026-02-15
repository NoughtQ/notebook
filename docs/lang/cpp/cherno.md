---
counter: true
draft: false
---

# C++ 笔记（Remake）

!!! recommend "参考资料"

    - The Cherno 的 [C++ 教程](https://www.youtube.com/playlist?list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb)；[中文翻译版](https://www.bilibili.com/video/BV1qh411p7Sa?vd_source=7c38ff5056b0974a26db352a36e1359c)

## Intro

???+ question "为什么学 C++"

    - C++ 仍然是编写高性能代码时最常用的语言之一
    - 需要在一个特定平台/架构上让代码本地(native)运行，对硬件进行直接控制
    - 很多游戏引擎、操作系统（PC/移动端/主机(console)）都是用 C++ 写的

???+ info "和 C#、Java 的区别"

    - C++ 经编译器编译后得到目标平台的机器码，这是能被 CPU 直接执行的指令，所以 C++ 是一种 native language
    - C# 和 Java 首先被编译为中间语言，运行程序时需经过虚拟机在运行时转化为相应的机器码
    - 虽说 C++ 是 native 的，但如果代码写的很烂，甚至跑得比用 C# / Java 写的更慢，因为后者会在运行时优化很多东西但 C++ 不会
    - 如果想要追求极致的性能，更推荐用 C++，否则 C# 和 Java 可能是更好的选择

第一个 C++ 程序：

```cpp title="Main.cpp"
#include <iostream>   // (1)

int main() {          // (2)
    std::cout << "Hello, world!" << std::endl;  // (3)
    std::cin.get();
}
```

1.  这是一条**预处理语句**(preprocessor statement)，将名为 `iostream` 的文件（称为**头文件**(header files)）内的所有东西（包括接下来要用的 `cout` 和 `cin`）拷贝到这个文件里
2.  几乎每个 C++ 程序都有 `main()` 函数，它们被称为**入口点**(entry points)，也就是进入程序的入口；运行程序时，计算机会从这个函数内的代码开始执行；虽然返回类型为 `#!cpp int`，但 `main()` 是个例外，不需要主动返回任何类型的值，它会自动返回 0
3.  这里的 `<<` 在 C 中是左移运算符，但在这里它被**重载**(overloaded)了，得看成是另一种类似 `print` 的函数（其实运算符也是一种函数）

???+ note "源文件 -> 可执行文件"

    1. 编译前的预处理操作（第一条注释解释过了）
    2. 每个 `.cpp` 文件会被单独编译成一个**目标**(object)文件（后缀一般为 `.o`（UNIX/Linux）或 `.obj`（Windows））
    3. **链接器**(linker)通过解析符号(resolve symbols)将所有的目标文件（中的函数）链接起来，组成一个可执行文件（无后缀（UNIX/Linux）或 `.exe` 后缀（Windows））

现在另外编写一个 `Log()` 函数，并将其放在单独的文件中，用来打印消息：

```cpp title="Log.cpp"
#include <iostream>

void Log(const char* message) {        // 定义(definition)
  std::cout << message << std::endl;
}
```

原来的 `Main.cpp` 要想调用 `Log`，就得**声明**(declare)它。这样**编译器**就会相信存在这样一个函数，从而允许编译通过；它不关心这个函数到底是在哪里被**定义**(define)的。编译后，**链接器**会寻找 `Log` 的定义，然后将其和 `main` 函数的调用联系起来；如果没有找到定义，就会得到一个 linker error。

```cpp title="Main.cpp"
#include <iostream>

void Log(const char* message);         // 声明(declaration)

int main() {
    Log("Hello, world!");
    std::cin.get();
}
```

