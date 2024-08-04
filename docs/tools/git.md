---
counter: true
---

# Git

!!! info "动机"

    其实早在大一开学没多久就已接触到 Git，但是由于缺乏实践的磨炼（还没有上到很需要 Git 的课），所以我只记得一些最简单的用法，足够我平时更新自己的笔记本和博客仓库。然而，我想更深入地了解 Git 的用法，或者更进一步悟得「Git 之禅」，让我不至于只会用一些 `git add`、`git commit -m "xxx"`、`git push origin main` 之类简单的命令，或者看到报错不知所措。所以我用这篇笔记记录我第二次学习 Git 的过程。

## 开始

### 为什么用 Git

（~~因为大家都在用 Git~~）

设想一下，你和小组成员要完成一个大作业，必然会有不同的分工。假设你要完成 A 部分，另一位同学要完成 B 部分（A 部分与 B 部分有依赖关系），你们通过 vx 或者 qq 等通讯工具交流。那么在完成作业的过程中，你们的聊天记录中势必会有很多份不同版本的作业，而系统应该会自动为同名文件加“（数字）”，并偷偷将所有的版本保存到本地设备中。如果出现以下情况，阁下该如何应对？

- 你改了半天的文件，发现越改越不对劲，于是想要拿回原来的文件，结果你前不久刚清理了系统缓存，而且你的小组成员已经在原来文件的基础上修改了他自己的一部分，已经找不回原来的版本了（悲）。
- 有一天，你们的工作效率突然提高，短短几小时内交上了多个版本的文件，可由于系统该死的命名规则 + 你没有仔细看上传时间，一不小心在过旧版本的基础上修改文件，而且你和队友都没发现，结果到“完工”的时候发现整个程序无法运行......
- 在大作业的后期（代码量已经很大了），你的 A 部分和队友的 B 部分都做了一次大修改，而且由于相互依赖关系，在合并的时候遇到了大麻烦，而你们只能用肉眼检查两份版本的不同，花费了很多的时间。
- ...

Git 的出现解决了上述问题——它是一个开源、成熟、现代的版本控制工具，有许多项目都是由 Git 进行管理的，虽然学习曲线有些陡峭，但一旦熟练掌握后它将称为开发人员的一大利器。在之后的学习中，我们将会看到上面的问题是如何通过 Git 轻松解决的。

### 安装

!!! abstract "注"

    笔者的本地环境是 vscode + WSL 2（Ubuntu 24.04 LTS）。

``` bash
# 检查更新
$ sudo apt update
# 安装 Git
$ sudo apt install git

# 检查安装是否成功
$ git --version
git version 2.43.0

# 配置用户名和邮箱（替换为自己的用户名和邮箱）
$ git config --global user.name "Nought"
$ git config --global user.email "haha@hehe.xyz"
```

## 基础命令

### 新建本地仓库

- 法一：切换到想要作为仓库的目录下，不带额外参数

``` shell
$ cd /path/to/the/repository 
$ git init
```

- 法二：在当前所在目录新建名为 "new_repo" 的仓库

``` shell
$ git init new_repo
```

### 克隆远程仓库至本地

基础命令：
``` shell
$ git clone <repo_url>
```
其中 `<repo_url>` 既可以是 HTTPS URL，也可以是 SSH URL，以笔者 Github 上的某个<u>曾经存在</u>的仓库为例：

- HTTPS：`https://github.com/NoughtQ/blog.git`
- SSH：`git@github.com:NoughtQ/blog.git`

HTTPS 较为简单，这里稍微介绍一下 Git SSH URL。它的一般格式是：`git@HOSTNAME:USERNAME/REPONAME.git`，在上例中，主机名为`github.com`，用户名为`NoughtQ`，仓库名为`blog`。

!!! info "注"

    无论是 `git init` 还是 `git clone`，都会生成一个名为 .git 的隐藏目录，它保存了与 Git 相关的重要信息（也包含一些个人隐私信息），请不要随便乱动！所有的项目文件应该与 `.git` 位于同一目录下。

### 保存变更

假如新增文件 hello.txt，现在我想保存这一变更，
<div style="text-align: left">
    <img src="images/git/1.png" width=30%>
</div>

那么可以执行以下命令：
``` shell
$ git add hello.txt
$ git commit -m "Add hello.txt to the repo"
```

- 执行 `git add <list of filenames>` 命令可将文件上传至暂存区。平时我喜欢使用 `git add .`，简单粗暴地将当前目录下所有文件（不管有没有更新）全部放到暂存区内，如果文件不多且简单的话可以这样偷懒，否则出什么意外我不敢保证。
- 可以用 `git status` 查看暂存区的情况。
<div style="text-align: center">
    <img src="images/git/2.png" width=60%>
</div>

- 使用 `git reset` 可以清除暂存区内所有的文件，也就是撤销 `git add` 命令

- 执行 `git commit -m "some message"` 提交暂存区内的文件，创建了一个包含消息的新提交（也可以认为是一份「快照」或「存档」），此时本地仓库中便有了这份提交的记录，并且会对它进行跟踪。
- 可用 `git log` 查看提交日志。
<div style="text-align: center">
    <img src="images/git/4.png" width=60%>
</div>
<div style="text-align: center">
    <img src="images/git/3.png" width=60%>
</div>

### 查看变更信息

前面稍微讲到点 `git status` 和 `git log` 命令，这里稍微展开讲讲。

#### git status

该命令可以显示工作目录和暂存区域的状态，观察哪些变更**已暂存**，哪些尚**未暂存**，以及哪些文件**未被 Git 跟踪**。下面的例子包含了这三类状态：

```
$ git status

On branch main
Changes to be committed:
(use "git reset HEAD <file>..." to unstage)

modified: hello.py

Changes not staged for commit:
(use "git add <file>..." to update what will be committed)
(use "git checkout -- <file>..." to discard changes in working directory)

modified: main.py

Untracked files:
(use "git add <file>..." to include in what will be committed)

hello.pyc
```

其中未跟踪的文件可以分为两类，要么是 `git add` 命令后用户新增的文件，要么是编译后的二进制文件，但后者往往不需要用 Git 上传，可以通过编辑 .gitignore 文件来忽略这些文件（见后面[忽略特殊文件](#忽略特殊文件)一节）。

#### git log

`git log` 用来显示已提交的快照（或者说历史记录），下面是一些关于 `git log` 的命令：

``` bash
# 使用默认格式显示整个提交历史记录，默认查看器的使用类似 vim，需要按 q 退出
$ git log
```
某条记录：
<div style="text-align: center">
    <img src="images/git/11.png" width=70%>
</div>

``` bash
# 按 <limit> 限制显示的提交个数
$ git log -n <limit>
```

``` bash
# 将每个提交信息压缩成一行，只显示前几位哈希值和提交信息
$ git log --oneline
```
某条记录：
<div style="text-align: center">
    <img src="images/git/12.png" width=60%>
</div>

``` bash
# 除了普通的 git log 信息外，还有各种文件的修改信息，比如增减的行数等
$ git log --stat
```

某条记录：
<div style="text-align: center">
    <img src="images/git/13.png" width=60%>
</div>

``` bash
# 可以理解为 git log --stat 的 plus 版，将每份文件的内容都用 diff 比对
$ git log -p
```

某条记录：
<div style="text-align: center">
    <img src="images/git/14.png" width=60%>
</div>

``` bash
# 找到指定用户的提交
$ git log --author="<name>"

# 找到包含指定信息的提交
$ git log --grep="<pattern>"

# 仅显示从 <since> 到 <until> 之间发生的提交。这两个参数可以是提交的哈希值、分支名称等其他类型的修订版本引用。
$ git log <since>..<until>

# 仅显示包含指定文件的提交
$ git log <file>
```

``` bash
# 查看所有分支的提交信息（git log 只能查看当前分支的提交）
$ git log --branches=*
```

部分结果（这里运行的是 `git log --branches=* --oneline`）：
<div style="text-align: center">
    <img src="images/git/16.png" width=60%>
</div>

``` bash
# 显示提交记录的图画形式（用 * 表示一次提交）
$ git log --graph --decorate --oneline
```

结果（由于这个仓库没有进行过多分支合并等操作，所以只有一条线）：

<div style="text-align: center">
    <img src="images/git/15.png" width=50%>
</div>


### 向远程仓库上传变更

!!! info "前提"

    要么用 `git clone` 获取远程仓库（此时已自动将本地仓库与远程仓库连接），要么手动连接远程仓库。

    手动连接远程仓库（`git clone`得到的仓库无需此步骤）：
    ``` shell
    $ git remote add <remote_name> <remote_repo_url>
    ```
    其中 `<remote_name>` 可以随便起，但是要记住你取的名字。

``` shell
$ git push <remote_name> <local_branch_name>
```
这条命令会将当前跟踪的记录上传至远程仓库（`<remote_name>`，如果是 `git clone` 下来的仓库默认名为 origin）的某一指定分支上（`<local_branch_name>`），这中间往往会出（~~我曾遇到过的~~）各种各样的问题：

- SSH 配置错误（后面会讲到）
- 网络连接问题：需要挂梯子，~~或者重启电脑试试？~~
- 上传文件内容过大（比如单个文件不得超过 100 M 等）

!!! summary "总结"

    >图可能画的不对，若有问题请指出

    <figure style=" width: 80%" markdown="span">
        ![](images/git/5_dark.png#only-dark)
        ![](images/git/5_light.png#only-light)
        <figcaption></figcaption>
    </figure>

### 连接远程仓库

上一小节中我们简单提到了 `git remote` 命令，通过该命令可以创建、查看和删除与其他存储库的远程连接。注意这里所谓的“连接”并不会让信息在仓库之间来回传递，只有用户手动推送本地提交（commit）才会改变远程仓库的内容。

下面介绍一些常用命令：

``` shell
# 列出和其他仓库的远程连接
$ git remote

# 与上一条命令类似，但是会列出仓库名称和 url
$ git remote -v

# 只列出指定仓库的 url
$ git remote get-url <name>
# 参数 --push 查看 push url 而非 fetch url
# 参数 --all 列出远程仓库的所有 url

# 列出仓库的详细信息
$ git remote show <name>

# 创建与远程仓库的连接（前面讲过了）
$ git remote add <remote_name> <remote_repo_url>

# 移除与远程仓库的连接
$ git remote rm <remote_name>

# 重命名远程仓库
$ git remote rename <old_name> <new_name>

# 删除远程仓库中不存在的所有本地分支
$ git remote prune <name>
# 参数 --dry-run 会列出会被删掉的分支，但实际上不会删掉它们
```

## 进阶命令

### 撤销提交或更改

- 执行 `git checkout <hash_id>` 命令回到哈希值为 `<hash_id>` 的提交记录，可以查看、编译、运行甚至编辑该记录的文件，无需担心目前状态下文件的丢失问题（可以使用`git checkout <current_branch_name>` 命令回到当前状态（最新的提交））。

    !!! warning "注意：使用该命令前确保本地仓库的文件已提交，否则无法执行。"

    执行此命令后会使仓库处于“脱离头指针（HEAD）”的状态，也就是说现在的工作不在任何一条分支上。如果回到已存在的分支后，执行那条命令后的任何提交都会被孤立掉，这些孤立的提交最后会被扔掉，永久损毁。若要避免这种情况，可以建立新的分支来保存这些提交，但是这种做法对其他提交具有一定破坏性，不推荐这么做。

- 一种比较好的做法是使用 `git revert HEAD`，这样就能撤销最近的一次提交，而且保证仍然在当前分支上，缺点是 Git 仍旧保留了被撤销了的提交记录和撤销操作的记录，看着有些繁琐。

- 如果想要有一个干净的提交记录，`git reset --hard <hash_id>` 就派上用场了，它可以将不想要的提交撤销地干干净净，不留痕迹。但它会影响到和远程仓库的交互，比如我撤销了某个最新的提交，如果此时 `git push`，Git 就会认为我推送的分支不是最新的，这就比较麻烦了。而 `git revert` 就不会有这种麻烦了，因此还是上一种撤销策略更合适。

!!! summary "总结"

    `git revert` 适用于撤销公共变更（远程仓库），而 `git reset` 适用于撤销私有变更（本地仓库）。

- `git commit --amend` 可以用来修改最近一次的提交。比如你一顿 `git add xxx`、`git commit -m "xxx"` 操作后发现漏了几个文件没提交，这时可以先 `git add <forgotten_files>`，再 `git commit --amend`，就可以补上漏掉的文件而无需新开一个提交。

- `git clean`：暂时略过

### Git 分支

分支的形象化表示：

<figure style=" width: 80%" markdown="span">
    ![](images/git/17_dark.png#only-dark)
    ![](images/git/17_light.png#only-light)
    <figcaption></figcaption>
</figure>

``` bash
# 列出本地仓库所有分支，同 git branch --list
$ git branch

# 创建名为 <name> 的新分支
$ git branch <name>

# 在远程仓库 origin 创建名为 <name> 的新分支
git push origin <name>~

# 安全删除名为 <name> 的分支
$ git branch -d <name>

# 强制删除名为 <name> 的分支
$ git branch -D <name>

# 删除名为 <name> 的远程仓库 origin 的分支
$ git push origin --delete <name>
# or 
$ git push origin :<name>

# 修改分支名字
$ git branch -m <old_name> <new_name>

# 列出本地仓库和远程仓库的所有分支
$ git branch -a
```

### 拉取请求

#### 功能分支工作流

功能分支工作流使用共享的 Bitbucket 仓库来管理协作，开发者在隔离的分支中创建功能。在合并到主分支之前，开发者需要发起一个拉取请求（pull request），与项目维护者讨论并决定是否合并到主分支，之后项目维护者可以关闭 pr 。这样的 pr 中源仓库和目标仓库是同一个仓库。

除此之外，开发者还可以通过 pr 一份功能不完整的提交，向其他开发者获取建议和帮助；其他开发者利用讨论功能提建议，或者直接另外提交一份来解决问题。

#### 使用拉取请求拷贝工作流程

开发者可以先拷贝（fork）一份项目维护者的共享仓库，然后将功能完善过的文件推送到刚拷贝下来的仓库。之后提出 pr ，让项目维护者进行审查。这种 pr 的源仓库和目标仓库不是同一个仓库了，前者是自己拷贝下来的公共仓库，而后者才是项目维护者自己的仓库。

就我个人感觉，这种方法对项目维护者来说可能更加“干净”一些：前面的「功能分支工作流」会让主仓库开出很多分支，有些凌乱；而 fork 项目维护者的仓库下来不会对主仓库有什么很大的影响。所以我更喜欢这种方法。


## 其他

>注：可能不是那么重要的内容，或者扩展性的内容

### 配置仓库

用到 `git config` 命令

``` shell
# 设置当前系统（全局）用户名
$ git config --global user.name <name>

# 设置当前仓库（本地）用户的邮箱
$ git config --local user.email <email>

# 为 git 命令设置别名，提高敲命令的效率
$ git config --global alias.<alias-name> <git-command>
# 比如：
$ git config --global alias.ci commit
$ git config --global alias.st status 
$ git config --global alias.co checkout 
$ git config --global alias.br branch 
$ git config --global alias.up rebase 

# 选定编辑器，比如 vi
$ git config --system core.editor <editor>

# 打开全局配置文件并手动编辑
$ git config --global --edit
```

### 忽略特殊文件

!!! question "问题"

    你可能为这样一件事犯愁：为了方便管理，你将某些重要文件放在本地仓库下，但是它们不应该传到远程仓库上。每次当你用 `git status` 查看时，就会看到这些标红的文件，心里总感觉不舒服。

`.gitignore` 文件可以根据我们设定的内容，自动忽略仓库下指定的文件，从而为我们带来了便利和安全。该文件通常放在仓库的根目录下。

首先了解一下忽略文件的原则（by [廖雪峰](https://liaoxuefeng.com/books/git/customize/ignore/)）：

- 忽略**操作系统自动生成的文件**，比如缩略图等
- 忽略**编译生成的中间文件、可执行文件**等，比如Java编译产生的.class文件等
- 忽略**带有敏感信息的配置文件**，比如存放口令的配置文件等

基本语法：

- 规范起见，每行只写一个文件名
- '#' 开头表示注释
- 直接写完整的文件名/目录名，Git 就会自动忽略该文件/目录
- 写 `*.<extension>` 可忽略所有文件扩展名为`<extension>`的文件
- 若想忽略某一类文件，但是又不想忽略一个属于该类的文件，那么可以使用`!<filename>` 表示将该文件排除于 .gitignore 的规则之外

命令相关：

- 符合 .gitignore 名单的所有文件均无法直接进行 `git add` 操作,但是可以使用 `git add -f <file>` 强制将文件传入暂存区，忽略 .gitignore 的规则
- 可用 `git check-ignore -v <file>` 检查该文件是否在 .gitignore 的规则下，并在控制台上打印结果

### Git SSH 密钥配置

SSH 密钥是 SSH（Secure Shell，安全外壳）网络协议的访问凭证，这种协议用于不安全开放网络上计算机之间的远程通信，包括远程文件传输、网络管理和远程操作系统访问等。

密钥包含公钥和私钥，公钥可以放在公共场合下，而私钥必须由个人安全保管。可以将公钥理解为「锁」:lock:，私钥理解为「钥匙」:key:。密钥通过公钥加密算法生成，比如 RSA 算法等，它能确保公钥能从私钥中产生，但反之不行。

下面介绍在 Linux 上生成 SSH 密钥，并且在 Github 上添加 SSH 密钥（默认已注册 Github 账号）：

1. 创建密钥

``` bash
$ ssh-keygen -t ed25519 -b 4096 -C "your_email@example.com"
```

2. 系统将提示输入要保存密钥的文件，既可以指定文件位置，也可以按回车键接受默认文件位置（这里选择后者）

3. 系统接下来提示输入口令，这样每当使用 SSH 密钥时都需要口令，提供了额外的一层防护

结果：

<div style="text-align: center">
    <img src="images/git/6.png" width=70%>
</div>

4. 将新的 SSH 密钥添加到 ssh-agent

    - 先检查 ssh-agent 是否正常运行：
    
    ``` bash
    $ eval "$(ssh-agent -s)"
    ```
    如果显示 pid，说明是正常运行的

    - 若正常运行，将新的 SSH 密钥添加到本地 SSH 代理：
    ``` bash
    ssh-add /Users/you/.ssh/id_rsa
    ```

    还要输入一遍刚刚设定的口令才能完成添加。

结果：

<div style="text-align: center">
    <img src="images/git/7.png" width=70%>
</div>

5. 进入 Github [官网](https://github.com)，点击右侧用户头像，在弹出的列表中找到 Settings，点击进入后在左侧列表中的 Access 区域中找到 SSH and GPG keys，点击后再点击右侧 New SSH key，开始新建 SSH 密钥。

6. 取好标题，并将公钥内容复制到 Key 一栏，如图所示：

<div style="text-align: center">
    <img src="images/git/10.png" width=70%>
    <img src="images/git/8.png" width=70%>
</div>

7. 点击 Add SSH key 后完成创建，可以在 SSH keys 一栏查看结果

<div style="text-align: center">
    <img src="images/git/9.png" width=70%>
</div>

这样的话 Linux 本地环境就可以与自己 Github 账户上的远程仓库进行连接了。
