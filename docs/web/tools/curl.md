---
counter: true
---

# curl

!!! abstract "参考资料"

    - [curl 初学者教程](https://www.ruanyifeng.com/blog/2011/09/curl.html) - by 阮一峰
    - [curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html) - by 阮一峰
    - [Curl Cookbook](https://catonmat.net/cookbooks/curl)


curl 意为客户端(client) URL 工具，是一种命令行工具，用来请求 Web 服务器。以下是 curl 的一些可用参数：

!!! warning "注意"

    下面涉及到的 URL 不一定是真实的 URL，有些是随便杜撰出来的......

!!! card ""

    <div class="fakeTitle">-A</div>

    指定客户端的用户代理(`User-Agent`)标头，默认用户代理字符串是 `curl/[version]`

    ``` sh
    # 将用户代理改为 Chrome 浏览器
    $ curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://example.com

    # 移除用户代理标头
    $ curl -A '' https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-b</div>

    指定要发送的 Cookie

    ``` sh
    $ curl -b 'foo=bar' https://example.com
    ```

    - 可以发送多个 Cookie，中间用分号间隔

    ``` sh
    $ curl -b 'foo1=bar1;foo2=bar2' https://example.com
    ```

    - 也可以发送带 Cookie 的文件

    ``` sh
    $ curl -b cookies.txt https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-c</div>

    将服务器设置的 Cookie 写入一个文件内

    ``` sh
    $ curl -c cookies.txt https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-d / --data-urlencode</div>

    发送 POST 请求的数据体
    
    - 此时会自动加上标头 `Content-Type: application/x-www-form-urlencoded`
    - 并且将请求方法自动设置为 POST，因此下面的 `-X POST` 可省略
    - 两者的唯一区别在于后者会将数据进行 URL 编码

    ``` sh
    $ curl -d 'login=name&password=123456' -X POST https://example.com/login

    # 或者
    $ curl -d 'login=name' -d 'password=123456' -X POST https://example.com/login

    # 读取文件（data.txt）
    $ curl -d '@data.txt' https://example.com/login

    # 数据 'hello world' 中的空格会转为 URL 编码 %20
    $ curl --data-urlencode 'comment=hello world' https://example.com/comments
    ```

!!! card ""

    <div class="fakeTitle">-e</div>

    设置 HTTP 标头 `Referer`（请求来源）

    ``` sh
    curl -e 'https://src.com?q=example' https://dst.com
    ```

!!! card ""

    <div class="fakeTitle">-F</div>

    上传二进制文件（图片、音频、视频等文件）

    ``` sh
    # 上传文件 photo.png
    $ curl -F 'file=@photo.png' https://blog.com/profile
    ```

    - 此时会自动添加标头 `Content-Type: multipart/form-data`
    - 也可以指定 MIME 类型（不设置的话默认为 `application/octet-stream`）

    ``` sh
    # MIME 类型为 image/png
    $ curl -F 'file=@photo.png;type=image/png' https://blog.com/profile
    ```

    - 还可以指定服务器接收到的文件名

    ``` sh
    # 原始文件名为 photo.png，服务器接收到的文件名为 picture.png
    $ curl -F 'file=@photo.png;filename=picture.png' https://blog.com/profile
    ```
!!! card ""

    <div class="fakeTitle">-G</div>

    构造 URL 查询字符串

    ``` sh
    # 实际请求的 URL 为 https://example.com/search?name=noughtq&age=20
    # 若省略 -G 则会发出 POST 请求
    $ curl -G -d 'name=noughtq' -d 'age=20' https://example.com/search

    # 若数据需要 URL 编码，用 --data-urlencode 替代 -d
    ```

!!! card ""

    <div class="fakeTitle">-H</div>

    添加指定的 HTTP 请求标头

    ``` sh
    $ curl -H 'Accept-Language: en-US' https://example.com

    # 添加多个标头
    $ curl -H 'Accept-Language: en-US' -H 'Secret-Message: xyzzy' https://example.com

    # 组合技：发送 JSON 数据
    $ curl -d '{"login": "noughtq", "pass": "123456"}' -H 'Content-Type: application/json' https://example.com/login
    ```

!!! card ""

    <div class="fakeTitle">-i</div>

    额外打印 HTTP 响应标头（先输出标头，空一行再输出网页源码）

    ``` sh
    $ curl -i https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-I / --head</div>

    仅打印 HTTP 响应标头

    ``` sh
    $ curl -i https://example.com
    # 或者
    $ curl --head https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-k</div>

    跳过 SSL 检测

    ``` sh
    $ curl -k https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-L</div>

    让 HTTP 请求跟踪服务器的重定向（默认不跟踪）

    ``` sh
    $ curl -L https://example.com
    ```

!!! card ""

    <div class="fakeTitle">--limit-rate</div>

    限制 HTTP 请求和回应的带宽，可用于模拟慢网速的环境

    ``` sh
    # 带宽限制为 200 KB/s
    $ curl --limit-rate 200k https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-o</div>

    将服务器的响应内容保存在指定文件内（等同于 `wget` 命令）

    ``` sh
    $ curl -o example.html https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-O</div>

    类似上一条指令，但是将 URL 的最后部分作为文件名

    ``` sh
    # 服务器响应内容保存在文件 bar.html 内
    $ curl -O https://example.com/foo/bar.html
    ```

!!! card ""

    <div class="fakeTitle">-s</div>

    不输出错误和进度信息，不发生错误的话会正常显示运行结果

    ``` sh
    $ curl -s https://example.com

    # 不产生任何输出
    $ curl -s -o /dev/null https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-S</div>

    仅输出错误信息，通常与 `-s` 一起使用

    ``` sh
    $ curl -sS -o /dev/null https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-u</div>

    设置服务器认证的用户名和密码

    ``` sh
    $ curl -u 'noughtq:123456' https://example.com/login
    ```

    - 事实上，`curl` 可以自动识别 URL 中的用户名和密码

    ``` sh
    # 等价于上一条命令
    $ curl https://noughtq:123456@example.com/login
    ```

    - 可以仅设置用户名，但 curl 会提示输入密码

    ``` sh
    $ curl -u 'noughtq' https://example.com/login
    Enter host password for user 'noughtq':
    ```

!!! card ""

    <div class="fakeTitle">-v / --trace</div>

    输出通信的全过程，用于调试

    ``` sh
    $ curl -v https://example.com
    ```
    
    `--trace` 还会输出原始的二进制数据

    ``` sh
    $ curl --trace https://example.com
    ```
    
!!! card ""

    <div class="fakeTitle">-x</div>

    指定 HTTP 请求代理（若未指定，默认为 HTTP）

    ``` sh
    # 该请求通过 myproxy.com:8080 的 socks5 代理发出
    $ curl -x socks5://james:cats@myproxy.com:8080 https://example.com
    ```

!!! card ""

    <div class="fakeTitle">-X</div>

    指定 HTTP 请求方法

    ``` sh
    # 发出 POST 请求
    $ curl -X POST https://example.com
    ```

