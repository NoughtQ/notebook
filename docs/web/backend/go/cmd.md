---
counter: true
---

# Go 命令

!!! abstract "参考资料"

    - [官方 reference](https://pkg.go.dev/cmd/go)
    - `go help` 命令查看
    - [Go 命令详解](https://zhuanlan.zhihu.com/p/161494871) - from 知乎（2020 年）
    - [golang 命令详解](https://studygolang.com/articles/21091)

!!! card ""

    <div class="fakeTitle">bug</div>

    - 打开默认浏览器，跳转至 [Go 官方仓库](https://github.com/golang/go)的 Issues 界面并给出模板，直接报告 bug；
    - 但我这里（WSL2 + Ubuntu 24.04 LTS，没有装默认浏览器）仅在终端给出 bug 报告模板，如果有 bug 可以到 [Go 官方仓库](https://github.com/golang/go)下用该模板提 Issue

    用法：

    ``` sh
    $ go bug
    Please file a new issue at golang.org/issue/new using this template:
    # 给出模板
    ```

!!! card ""

    <div class="fakeTitle">build</div>

    编译指定源码文件/代码包（依赖包）并生成可执行文件。

    用法：

    ``` sh
    $ go build [-o output] [build flags] [packages]
    ```

    - `go build`：若目录内只有一个带 `main` 函数的 go 文件，输入此命令会会自动编译该文件
    - `go build exp1.go`：指定被编译的文件（生成的可执行文件名为 `exp1`）
    - 参数表
        - `-o`：指定输出文件名（可带路径）
        - `-i`：安装指定的包，命令等价于 `go build` + `go install`
        - `-a`：更新所有除标准包之外的包
        - `-n`：打印需要执行的编译命令，但不执行编译操作
        - `-x`：类似上一个参数，但执行编译操作
        - `-p n`：指定并行可编译的数目，默认为 CPU 数目
        - `-v`：打印正在编译的包名
        - `-work`：打印编译时生成的临时文件夹名，且编译完成后不删除这些临时文件夹


!!! card ""

    <div class="fakeTitle">clean</div>

    删除执行其他命令时产生的文件或目录，包括：

    ``` 
    _obj/            
    _test/           
    _testmain.go     
    test.out         
    build.out        
    *.[568ao]        

    DIR(.exe)        
    DIR.test(.exe)   
    MAINFILE(.exe)   
    *.so             
    ```

    用法：

    ``` sh
    $ go clean [-i] [-r] [-cache] [-testcache] [-modcache] [-fuzzcache] [build flags] [packages]
    ```

    参数表：

    - `-i`：清除关联的安装包和可执行文件（即 `go install` 安装的文件）
    - `-n`：打印需要执行的清除命令，但不执行
    - `-r`：递归清除 `import` 引入的包
    - `-x`：类似 `-n`，但执行命令


!!! card ""

    <div class="fakeTitle">doc</div>

    查看指定包或符号的文档。

    用法：

    ``` sh
    $ go doc [doc flags] [package|[package.]symbol[.methodOrField]]
    ```

    - `go doc`：直接运行该命令会打印当前目录下的包的文档
    - 可以简写包的名称（比如 `encoding/json` 可简写为 `json`）



!!! card ""

    <div class="fakeTitle">env</div>

    查看 Go 的环境变量。

    用法：

    ``` sh
    $ go env [-json] [-changed] [-u] [-w] [var ...]
    ```

    参数表：

    - `-json`：以 JSON 格式打印环境变量
    - `-u`：使用 `-w` 参数的前提
    - `-w`：后面跟一个或多个形如 NAME = VALUE 的参数，用于改变指定环境变量的值
    - `-changed`：仅打印与默认设置不同的环境变量

!!! card ""

    <div class="fakeTitle">fix</div>

    更新代码包的源码为新版本的代码。

    用法：

    ``` sh
    $ go fix [-fix list] [packages]
    ```



!!! card ""

    <div class="fakeTitle">fmt</div>

    检查指定文件并将其整理成规范的 go 语言格式（一般使用 `gofmt` 工具代替）。

    用法：

    ``` sh
    $ go fmt [-n] [-x] [packages]
    ```

    参数表：

    - `-l`：显示需要整理的文件
    - `-w`：将整理后的内容直接写入该文件，而不只是打印出来
    - `-r`：添加整理规则，便于批量替换
    - `-s`：简化文件代码
    - `-d`：显示整理前后文件的差别（类似 `diff` 指令）（默认值为 `false`）
    - `-e`：打印所有的语法错误（若不用此参数，默认只打印前 10 个错误）
    - `-cpuprofile`

    ``` sh
    # 整理 mod 模块下的所有文件
    $ gofmt mod

    # 整理单个文件
    $ gofmt exp.go
    ```

!!! card ""

    <div class="fakeTitle">generate</div>

    >目前不太懂，先空着

!!! card ""

    <div class="fakeTitle">get</div>

    获取远程的代码包及其依赖包，并进行编译和安装（一般安装在 `GOPATH` 目录下的 `src` 子目录中）。

    用法：

    ``` sh
    $ go get [-t] [-u] [-v] [build flags] [packages]
    ```

    - 在下载路径的最后加上 `@version` 可以指定版本为 `version`（`latest` 表示最新版）
    
    ``` sh
    $ go get golang.org/x/tools/cmd/godoc@latest
    ```

    - 参数表：
        - `-d`：只下载不安装
        - `-f`：（使用前提：需要用到 `-u`）忽略对已下载代码包的导入路径的检查
        - `-fix`：先修正，再进行编译和安装
        - `-t`：额外下载需要用到的依赖包
        - `-u`：更新已有代码包及其依赖包（默认只下载本地不存在的包而不更新已有的包）

    ???+ warning "注意"

        由于国内网络限制原因，无法直接访问 `golang.org`，所以在执行该命令前需要配置好 Go 的代理服务器，具体方法如下：

        - 前往[Goproxy.cn](https://goproxy.cn/)
        - 按照步骤设置环境变量
        
        ``` sh
        $ export GO111MODULE=on
        $ export GOPROXY=https://goproxy.cn
        ```

        - 之后用 `go env` 查看环境变量，若 `GOPROXY` 的值为该网址，说明配置成功

!!! card ""

    <div class="fakeTitle">install</div>

    先编译指定文件，后将生成的二进制文件放到指定目录中（一般放在 `GOPATH` 目录下的 `bin` 子目录中）。

    用法：

    ``` sh
    $ go install [build flags] [packages]
    ```

    先用 `go env` 检查环境变量 `GOBIN` 是否有值，若为空则需手动设置
    
    ``` sh
    $ export GOBIN=...

    $ go install exp.go
    ```

!!! card ""

    <div class="fakeTitle">list</div>

    列出当前安装的包。

    用法：

    ``` sh
    $ go list [-f format] [-json] [-m] [list flags] [build flags] [packages]
    ```



!!! card ""

    <div class="fakeTitle">mod</div>

    用于对 Go 包的管理。

    用法：

    ``` sh
    $ go mod <command> [arguments]
    ```

    !!! info "使用前提"

        环境变量 `GO111MODULE` 的值为 `'on'`（较新版本的 Go 默认开启）或 `'auto'`（如果没有开启，项目文件只能放在 `GOPATH` 下的 `src` 子目录内）

    假如创建了一个 go 项目文件，该文件引用了第三方包。在编译该文件前，需要先创建 go.mod 文件：

    ``` sh
    # 最后的名称为模块名（module），而非文件名（始终为 go.mod）
    $ go mod init module
    ```

    然后编译并运行该文件，此时 Go 会自动查找依赖关系并下载必要的包，写入 go.mod 文件内，并生成 go.sum 文件（检查依赖模块是否被篡改）。下载的包均保存在 `GOPATH/pkg/mod` 目录下。

    参数表：

    - `download`：下载代码包
    - `edit`：编辑 go.mod
    - `graph`：打印包的依赖图
    - `init`：在当前目录初始化新的模块（go.mod）
    - `tidy`：补上缺少的包，移除没用的包
    - `vendor`：将依赖包复制到 vendor 下
    - `verify`：检验依赖关系是否正确
    - `why`：解释为什么需要这些包


!!! card ""

    <div class="fakeTitle">work</div>

!!! card ""

    <div class="fakeTitle">run</div>

    编译并运行源码文件

    ``` sh
    $ go run exp.go
    ```

!!! card ""

    <div class="fakeTitle">test</div>

!!! card ""

    <div class="fakeTitle">tool</div>

!!! card ""

    <div class="fakeTitle">version</div>

    查看当前 Go 的版本

!!! card ""

    <div class="fakeTitle">vet</div>