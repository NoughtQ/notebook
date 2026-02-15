---
counter: true
---

# 入门部分

## OpenGL

[**OpenGL**](https://www.opengl.org/) 主要被视为一种提供一系列可用于操作图形和图像的函数的 API，但它本身是一种**规范**(specification)而非 API，由开发者根据规范**实现**这些函数。

实际开发 OpenGL 库的是**显卡制造商**，因此一旦实现中出现错误，通常可以通过更新显卡驱动程序来解决。


### 核心配置模式与即时模式

过去 OpenGL 采用的是**即时模式**(immediate mode)（通常指代**固定功能管线**(fixed function pipeline)）。

- 虽然易于使用和理解，但由于大部分功能隐藏在库内部，开发者对 OpenGL 的计算几乎没有控制权
- 并且随着开发者对灵活性需求的不断增长，规范也随之变得更加灵活，开发者获得了对图形的更多控制权

因此从 3.2 版本开始，该模式逐渐被弃用，并且鼓励采用更现代的**核心配置模式**(core-profile mode)。

- 在该模式下，OpenGL 会强制开发者使用现代编程实践；若尝试使用已弃用的函数，OpenGL 将停止绘制并抛出错误
- 虽然更难学习，但优势在于其灵活性和高效性，并且有助于开发者真正理解 OpenGL 和图形编程


### 扩展

OpenGL 的一大优势在于其对**扩展**(extensions)的支持。

- 每当出现新的渲染技术或大型优化方案时，通常都会在驱动程序中实现相应的扩展
- 如果硬件支持此类扩展，开发者就可以利用扩展提供的功能来实现更高级或更高效的图形效果，这样就无需等待 OpenGL 在未来的版本中正式加入这些功能，只需检查显卡是否支持该扩展即可使用这些新的渲染技术
- 通常情况下，当某个扩展非常流行或实用时，它最终会被纳入到未来的 OpenGL 版本中


### 状态机

- OpenGL 本身就是一个大型**状态机**(state machine)：它由一些定义了 OpenGL 当前的运行方式的变量组成
- OpenGL 状态通常被称为 OpenGL **上下文**(context)；在使用 OpenGL 时，我们经常通过设置一些选项，操作一些缓冲区，然后使用当前上下文进行渲染来改变其状态
- **改变状态**(state-changing)的函数：改变 OpenGL 的上下文
- **使用状态**(state-using)的函数：基于 OpenGL 的当前状态执行某些操作


### 对象

在 OpenGL 中，**对象**(objects)是一组选项的集合，代表 OpenGL 状态的一个子集，类似 C 语言的结构体。

```cpp
struct object_name {
    float  option1;
    int    option2;
    char[] name;
};
```

使用对象（其中 OpenGL 的上下文被可视化为一个大型结构体）：

```cpp
// The State of OpenGL
struct OpenGL_Context {
  	...
  	object_name* object_Window_Target;
  	...  	
};
```

使用对象的好处在于：可以在应用程序中定义多个对象，设置它们的选项，并在每次启动使用 OpenGL 状态的操作时，将对象绑定到我们预设的设置，而无需再次设置所有选项。


## 创建窗口

在开始绘制图形前，首先要做的便是创建一个 OpenGL 上下文和一个用于绘制的应用程序窗口。然而，这些操作因操作系统而异，OpenGL 也刻意将这些操作抽象化。这意味着我们需要自行创建窗口、定义上下文并处理用户输入。好在有一些库提供了这些功能，下面将采用较为流行的 **GLFW 库**。


### GLFW

官网下载链接：<https://www.glfw.org/download.html>。

>下面仅提供在 macOS / 部分 Linux 发行版上有效的安装步骤。Windows 上的安装见 [LearnOpenGL 教程对应章节](https://learnopengl.com/Getting-started/Creating-a-window)（需提前安装最新版 Visual Studio；个人认为 Windows 上的安装过程更加繁琐）。

建议下载源码后在本地编译（确保本地已安装 CMake），编译命令为（需自行创建 `build` 目录）：

```sh
$ cmake -S . -B build \
  -DBUILD_SHARED_LIBS=OFF \
  -DGLFW_BUILD_DOCS=ON \
  -DGLFW_BUILD_EXAMPLES=ON \
  -DGLFW_BUILD_TESTS=ON \
  -DGLFW_INSTALL=ON

$ make
```

编译后，可将 GLFW 安装在系统目录中供任何项目使用：

```sh
$ sudo cmake --install build
```

如果项目用到了 GLFW，只需在 C/C++ 源文件开头包含 GLFW 的头文件即可：

```cpp
#include <GLFW/glfw3.h>
```


### GLAD

由于 OpenGL 实际上只是一个标准/规范，并且 OpenGL 驱动程序有很多不同的版本，其大多数函数的位置在编译时是未知的，需要在**运行时**查询。好在有 [**GLAD 库**](https://github.com/Dav1dde/glad)帮我们摆脱这一繁琐的工作。它提供了一个 [Web 服务](https://glad.dav1d.de/)，点击链接进入该网站后，按下图所示步骤获取库文件：

<div align=center>
    <img src="images/getting-started/glad-download-1.png" width=80% />
    <img src="images/getting-started/glad-download-2.png" width=80% />
</div>

解压后，其目录结构如下：

```
.
├── include
│   ├── glad
│   │   └── glad.h
│   └── KHR
│       └── khrplatform.h
└── src
    └── glad.c
```

将目录内的这些内容移动/拷贝到项目目录下。然后在使用 OpenGL 的源文件中包含 GLAD 头文件即可。

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>  // 一定要放在 glad 头文件下，否则会产生编译错误
```

### 初始化

创建主函数，并在其中实例化 GLFW 窗口：

```cpp
int main() {
    glfwInit();    // 初始化 GLFW
    // glfwWindowHint(int target, int hint)：配置 GLFW
    // 一旦设置好，其值将保持不变，直到再次调用 glfwWindowHint 更改为止
    // target: 要更改的目标/选项，以 GLFW_ 为前缀的 GLFW 枚举
    // hint: 要设置的目标值/提示
    
    // 3.3 版本
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    
    // 核心配置模式
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);   // 仅 macOS 使用
  
    return 0;
}
```

创建窗口对象：

```cpp
// glfwCreateWindow 的参数：
//      int width
//      int height
//      const char* title
//      GLFWmonitor* monitor：用于全屏模式的显示器，nullptr 表示窗口模式
//      GLFWwindow* share：要与之共享资源的窗口，nullptr 表示不共享任何资源
GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", nullptr, nullptr);
if (window == nullptr) {
    std::cout << "Failed to create GLFW window" << std::endl;
    // 销毁所有剩余窗口，释放所有已分配资源，并将库设置为未初始化状态
    glfwTerminate();
    return -1;
}
// 指定窗口的上下文设置为调用线程的当前上下文
// 一个上下文在同一时间只能在一个线程上处于当前状态，并且每个线程在同一时间也只能拥有一个当前上下文
glfwMakeContextCurrent(window);
```

初始化 GLAD：

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
    std::cout << "Failed to initialize GLAD" << std::endl;
    return -1;
} 
```

设置渲染窗口的大小：

```cpp
// 前两个参数设置窗口左下角的位置，
// 第三个和第四个参数设置渲染窗口的宽度和高度（以像素为单位）
// 这里设置为与 GLFW 的窗口大小相同
glViewport(0, 0, 800, 600);
```

???+ note "注"

    在后台，OpenGL 使用通过 `glViewport` 指定的数据，将处理后的二维坐标转换为屏幕上的坐标。例如，处理后的点 `(-0.5, 0.5)` 最终会被映射到屏幕坐标系中的 `(200, 450)`。需要注意的是，OpenGL 中处理后的坐标范围为 [-1, 1]，因此实际上是将这一范围分别映射到 `(0, 800)` 和 `(0, 600)` 上。





### 视口

### 结束

### 输入

### 渲染



## 绘制三角形

## 着色器

## 纹理

## 变换

## 坐标系

## 相机