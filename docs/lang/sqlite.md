---
counter: true
---

# SQLite

!!! abstract "参考资料"

    - [官网](https://www.sqlite.org/index.html)
    - [英文教程](https://www.sqlitetutorial.net/)：本笔记主要参考这篇教程写的
        - 为了让笔记更为精简，我忽略了其中一些简单的例子，如果想要跟着例子学习的话请直接阅读这篇教程（~~不过个人觉得没有必要~~）
    - [菜鸟教程](https://www.runoob.com/sqlite/sqlite-tutorial.html)
    - [wiki](https://en.wikipedia.org/wiki/SQLite)
    - SQLite API 相关：
        - [Python sqlite3 库](https://docs.python.org/zh-cn/3.13/library/sqlite3.html)


## 介绍

[SQLite](https://en.wikipedia.org/wiki/SQLite) 是一个提供关系型数据库管理系统的软件库。名称中的 "lite" 表现的是 SQLite 在设置、数据库管理和需求资源等方面的**轻量化**(lightweighted)本质。具体来说，SQLite 具备以下显著特点：

- **自给**(self-contained)：不需要操作系统或外部库提供很多资源，这使得它能够在任何环境下（包括嵌入式系统）运行，可移植性高。
- **无需服务器**(severless)：一般的 RDBMS，比如 MySQL 和 PostgreSQL 需要一台单独的服务器，应用程序通过 TCP/IP 协议的发送和请求来访问数据库服务器。然而，SQLite 的数据库就集成在应用程序中，应用程序可以直接从数据库中读写数据。

<div style="text-align: center">
    <img src="images/sqlite/1.jpg" width="60%" />
</div>

- **零配置**(zero-configuration)：正因为 SQLite 的无服务器架构，因此我们无须事先配置 SQLite
- **事务处理的**(transactional)：SQLite 的事务遵守 ACID，即具备原子性(atomic)、一致性(consistent)、隔离性(isolated)和持久性(durable)的特征

此外，SQLite 还具备以下独特之处：

- 使用动态类型，因此能在表中的任何列存储任何值，可无视声明的类型
- 允许通过单个数据库连接来同时访问多个数据库文件
- 由于 SQLite 创建的数据库位于内存中，因此原型设计(prototyping)和测试的速度会非常快

!!! question "何时使用 SQLite 呢？"

    - 嵌入式应用
    - 本地存储：SQLite 很适合那些需要在本地存储用户偏好、设置和缓存的应用
    - 跨平台应用：SQLite 支持多平台运行
    - 快速的原型设计和开发
    - 物联网(IoT)设备：由于 IoT 使用资源有限，因此轻量级的 SQLite 能胜任这种情况


## 下载&安装

前往官方的[下载页](https://www.sqlite.org/download.html)，根据自己的电脑类型下载合适的版本。下面以 Windows 版本和 Linux 版本为例：

=== "Windows 11"

    1. 在下载页中找到 Windows 版本，点击下图红色方框处的链接下载。

        <div style="text-align: center">
            <img src="images/sqlite/2.png" width="90%" />
        </div>

    2. 下载好后解压压缩包，得到文件夹，然后点击进入。

        <div style="text-align: center">
            <img src="images/sqlite/3.png" width="90%" />
        </div>

    3. 按住 Shift 键，然后右键点击文件夹里的空白部分，呼出 Windows 10 风格的菜单，点击带有“终端”字样的选项。

        <div style="text-align: center">
            <img src="images/sqlite/4.png" width="80%" />
        </div>

        >熟悉命令行操作的小伙伴可以用 `cd` 命令切换到 sqlite 所在目录，无需遵守2, 3两步

    4. 在终端命令行中输入 `sqlite`，如果输出如下所示的信息，则说明 SQLite 可以正常运行。

        <div style="text-align: center">
            <img src="images/sqlite/5.png" width="90%" />
        </div>

    5.（可选，但十分推荐）退出 SQLite 程序（输入 `.quit` 命令），将 sqlite 所在目录迁移到合适的位置，然后设置环境变量，使得 SQLite 在电脑的任何目录下都可以运行。
    
    - 按下 Win + R 键，打开“运行”界面，输入 sysdm.cpl 后敲回车，进入“系统属性”界面

        <div style="text-align: center">
            <img src="images/sqlite/6.png" width="40%" />
        </div>

    - 点击该界面的“高级”选项卡，然后点击“环境变量”按钮

        <div style="text-align: center">
            <img src="images/sqlite/7.png" width="40%" />
        </div>

    - 在“环境变量”界面选中 Path 并双击，编辑该环境变量。然后在该界面新建项，内容为 SQLite 程序的目录（我这里放在 D:\sqlite 目录下）

        <div style="text-align: center">
            <img src="images/sqlite/8.png" width="45%" />
            <img src="images/sqlite/9.png" width="45%" />
        </div>

    - 最后不要忘记点击三个“确定”按钮，依次退出上述打开的界面，这样才能保存我们的设置
    - 重新打开终端，输入 `sqlite3`，如果不出意外的话，在任何目录下应当都可以启动 SQLite 了（现在我在 HOME 目录下也能打开 SQLite 了）！

        <div style="text-align: center">
            <img src="images/sqlite/10.png" width="90%" />
        </div>


=== "Ubuntu 24.04 LTS"

    超级简单，只要输入以下命令即可：

    ```sh
    $ sudo apt update               # 更新
    $ sudo apt install sqlite3      # 不要忘记最后的 3
    $ sqlite3                       # SQLite，启动！
    ```

    如果出现类似下面的打印信息，说明安装成功啦！

    ```
    SQLite version 3.45.3 2024-04-15 13:34:05
    Enter ".help" for usage hints.
    Connected to a transient in-memory database.
    Use ".open FILENAME" to reopen on a persistent database.
    sqlite>
    ```


此外，SQLite 还有 GUI 工具，比如：

- [SQLiteStudio](https://github.com/pawelsalawa/sqlitestudio)
- [DBeaver](https://dbeaver.io/)
- [DB Browser for SQLite](https://sqlitebrowser.org/)

不过，鉴于笔者时间有限，外加笔者喜欢用命令行访问数据库的习惯（~~感觉这样更像一名 CSer~~），所以这些工具的安装和使用就不再介绍了，对此感兴趣的读者可以点击这些链接或者在网上搜索相关教程进行学习。


## 命令行环境

最开始，我们需要在命令行环境执行 `sqlite3 path/to/my_database.db` 指令，用 SQLite **打开**已经存在的数据库文件，或者**创建**不存在的数据库文件。如果命令行的开头变成了 `sqlite>`，说明 SQLite 成功启动。

在 SQLite 中，所有的命令都是以 `.` 开头的。这里先介绍一些最基本，也是最常用的 SQLite 命令：


- `.open .open FILENAME`：也可以在 SQLite 内打开数据库文件
- `.databases`：显示当前 SQLite 连接的数据库，它至少会显示一个名为 `main` 的数据库
    - 如果一个数据库都没有，会显示：

        ```
        sqlite> .databases
        main: "" r/w
        ```

    - 可以使用 `attach` 语句将本地数据库文件连接到 SQLite 上：

        ```sql
        attach database "c:\sqlite\db\chinook.db" AS chinook;
        ```

    - 现在就有一些新的数据库了：

        ```
        sqlite> .databases
        main: "" r/w
        chinook: c:\sqlite\db\chinook.db r/w
        ```

- `.tables`：显示数据库中所有的表
    - 该命令支持模式(pattern)匹配（类似 SQL 的 `LIKE` 子句）
        - 匹配的字符串必须用单引号包裹
        - 比如 `%` 表示一个或多个字符，那么 `%es` 就表示以 `es` 结尾的字符串，因此：

        ```
        sqlite> .open C:\Users\qzy\Downloads\chinook\chinook.db
        sqlite> .tables '%es'
        employees    genres       invoices     media_types
        ```

- `.schema TABLE`：显示名为 `TABLE` 的表的结构，即模式(schema)

    ??? example "例子"

        ```
        sqlite> .schema albums
        CREATE TABLE IF NOT EXISTS "albums"
        (
            [AlbumId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            [Title] NVARCHAR(160)  NOT NULL,
            [ArtistId] INTEGER  NOT NULL,
            FOREIGN KEY ([ArtistId]) REFERENCES "artists" ([ArtistId])
                        ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        CREATE INDEX [IFK_AlbumArtistId] ON "albums" ([ArtistId]);
        ```

    - 如果只输入 `.schema`，那么就会显示所有表的结构
    - 如果想要查看所有表，包括与 SQLite 状态相关的表的结构及其内容，可以输入 `.fullschema` 命令

- `indexes`：显示当前数据库的全部索引
    - `indexes TABLE`：只显示名为 `TABLE` 的表的索引
- `.help`：打印帮助信息，显示各种 SQLite 命令以及选项
- `.quit`：退出 SQLite 命令行界面
- 格式化查询输出相关的命令：
    - `.mode column`：将输出模式设置为 `column`
    - `.header on`：显示列名
    - `.nullvalue NULL`：设置空值字面量

    这样可以使输出的内容更加美观。
    
    ??? example "例子"

        设置完上述指令后，可以打印出更加工整的表结构：

        ```
        sqlite> pragma table_info('albums');
        cid  name      type           notnull  dflt_value  pk
        ---  --------  -------------  -------  ----------  --
        0    AlbumId   INTEGER        1                    1
        1    Title     NVARCHAR(160)  1                    0
        2    ArtistId  INTEGER        1                    0
        ```

- `.output FILENAME`：执行该命令后，之后的查询结果都会保存在 `FILENAME` 文件下（可指定路径）
    - `.output` 命令会重新让查询结果显示在标准输出（即命令行）中

- `.read FILENAME`：执行保存在 `FILENAME` 内的 SQL 语句
    - 对于多行、重复的 SQL 语句而言，这个功能就很有用了

- `.dump`：将 SQLite 数据库的整个结构和数据转化为单个的文本文件
    - 默认情况下，该命令会在屏幕上输出 SQL 语句。为了将输出转向文件，需要在 `.dump` 命令前使用 `.output FILENAME` 命令，这样就可以将数据库存在 `FILENAME` 文件中
    - `.dump TABLE`：可以存储指定的表格
    - `.schema` 命令也可以实现转存功能

- CSV 文件导入：
    - 先使用 `.mode` 命令让 SQLite 切换到 CSV 模式
    - 然后使用 `.import FILE TABLE` 命令导入 csv 文件
    
        ```
        sqlite> .mode csv
        sqlite> .import c:/sqlite/city.csv cities
        ```

- CSV 文件导出：
    - 使用 `.header` 以显示结果集合的标题行
    - 使用 `.mode` 命令让 SQLite 切换到 CSV 模式
    - 输出 CSV 文件
    - 最后还可以跟一个 `SELECT` 语句，用于指定数据库的哪些数据要存在 CSV 文件内

    ???+ example "例子"

        ```
        >sqlite3 c:/sqlite/chinook.db
        sqlite> .headers on
        sqlite> .mode csv
        sqlite> .output data.csv
        sqlite> SELECT customerid,
        ...>        firstname,
        ...>        lastname,
        ...>        company
        ...>   FROM customers;
        sqlite> .quit
        ```

---
在 SQLite 中，我们可以输入任何合法的 SQL 语句。

- SQL 语句可以拆成多行，敲回车可以切换到下一行，用分号表示一条语句的结束，比如：

    ```sql
    sqlite> select *
        ...> from albums
        ...> order by AlbumId
        ...> limit 3;
    ```

    再敲回车的话，SQLite 就开始执行这条语句，并给出相应的输出。

- 如果敲到一半，发现语句写错的话，那么很遗憾，SQLite 不支持退格到上面的行，所以若发现前面行的错误的话，就不得不提前结束，从头再来——输入分号敲回车，提前结束 SQL 语句的编写。


## 基础语法

学了《数据库系统》课程后，发现 SQLite 只是 SQL 的其中一种实现，它支持大多数的 SQL 语句，因此这里就不再列出详细的语法规则。对此不太了解的读者可以阅读我的数据库笔记的 Lec 3-5（正在更新中）。

- [Lec 3: Introduction to SQL](../system/db/3.md)
- [Lec 4: Intermediate SQL](../system//db/4.md)
- [Lec 5: Advanced SQL](../system/db/5.md)

下面只会介绍一些带有 SQLite 特色的语法。


### 全文本搜索

在介绍**全文本搜索**(full-text search)的功能前，有必要了解一下**虚拟表格**(virtual table)的概念——它是 SQLite 的一种扩展，它看起来像一般的表格，但它们的区别在于数据的来源不同：一般表格的数据来源于数据库文件；而虚拟表格则通过调用自定义代码，从多个数据源来获取数据。

SQLite 的全文本搜索功能便是借助 **FTS5** 虚拟表格模块实现的。下面使用 `CREATE VIRTUAL TABLE` 语句来创建 FTS5 表格：

```sql
CREATE VIRTUAL TABLE table_name 
USING FTS5(column1, column2...);
```

注意，创建 FTS5 表格时不得添加类型、约束和主键声明，否则 SQLite 就会报错。创建 FTS5 表格时，SQLite 还会添加一个隐式的 `rowid` 列。

默认情况下，FTS5 对大小写不敏感。

下面介绍全文本搜索的三种方式：

- 在 `WHERE` 子句中使用 `MATCH` 运算符，比如：

    ```sql
    SELECT * 
    FROM posts 
    WHERE posts MATCH 'fts5';
    ```

- 在 `WHERE` 子句中使用 `=` 运算符，比如：

    ```sql
    SELECT * 
    FROM posts 
    WHERE posts = 'fts5';
    ```

- 使用“表格-值函数”语法，更为简便，比如：

    ```sql
    SELECT * 
    FROM posts('fts5');
    ```

一个真正的全文本搜索是由多个短语构成的，每个短语之间用 `+` 运算符拼接。

???+ example "例子"

    ```sql
    SELECT * 
    FROM posts 
    WHERE posts MATCH 'learn SQLite';
    ```

    该语句会查找所有包含 `learn SQLite` 的记录。

`*` 运算符用于**前缀搜索**(prefix search)，即匹配以某个短语开头的项。

???+ example "例子"

    ```sql
    SELECT * 
    FROM posts
    WHERE posts = 'search*';
    ```

    该语句会查找所有包含以 `search` 开头的短语的记录。

---
还可以在 `MATCH` 匹配字符串内使用布尔运算符 `AND`、`OR`、`NOT`，它们的作用分别是：

- `"q1 AND q2"`：需要同时匹配 `q1` 和 `q2`
- `"q1 OR q2"`：只需匹配 `q1` 和 `q2` 中的一个就算成功匹配了
- `"q1 NOT q2"`：需要匹配 `q1` 但不匹配 `q2`

可以使用多个布尔运算符连接多个短语，并且可以用 `()` 改变求解顺序。

???+ example "例子"

    === "例1"

        ```sql
        SELECT * 
        FROM posts 
        WHERE posts MATCH 'search AND sqlite OR help';
        ```

        该语句会查找所有同时包含 `search` 和 `sqlite`，或者只包含 `help` 的记录。


    === "例2"

        ```sql
        SELECT * 
        FROM posts 
        WHERE posts MATCH 'search AND (sqlite OR help)';
        ```

        该语句会查找所有同时包含 `search`，以及 `sqlite` 或 `help` 的记录。

---
SQLite 还为 FTS5 表格的全文本查询提供了三个内建的辅助函数：

- `bm25()`：返回一个值，反应当前匹配的精度，值越低表示匹配效果越好
- `highlight()`：返回查询内容的副本，并且搜索条目的外面用特殊的标记包裹，比如 `<b> search term </b>`
- `snippet()`：选择文本中的一个短片段，以最大化其包含搜索条目的数量

???+ example "例子"

    ```sql
    SELECT highlight(posts,0, '<b>', '</b>') title, 
        highlight(posts,1, '<b>', '</b>') body
    FROM posts 
    WHERE posts MATCH 'SQLite'
    ORDER BY rank;
    ```

    返回结果：

    <div style="text-align: center">
        <img src="images/sqlite/17.png" width="90%" />
    </div> 


## API

目前有大量的编程语言提供了 SQLite 相关的 API，所以这里列举一些常用的 API 使用方法。

!!! warning "注意"

    本笔记假定读者已经十分熟悉这些编程语言，所以不会介绍这些编程语言的语法细节。


### Python

Python 提供了内建的 `sqlite3` 模块，可以让程序员在 Python 上定义和操纵 SQLite 数据库，无需使用第三方库。不要忘记在程序开头处先导入 `sqlite3` 模块：

```py
import sqlite3
```


#### 创建数据库

首先，通过 `sqlite3` 模块的 `connect()` 函数创建一个新的 SQLite 数据库，或者打开一个已经存在的数据库。该函数会返回一个 `Connection` 对象实例，我们可以在该实例上执行各种数据库操作。

```py
conn = sqlite3.connect(database_file)
```

当我们不使用数据库的时候，不要忘记关闭与数据库的连接（就像文件的打开和关闭那样），这一操作通过 `close()` 方法实现：

```py
conn.close()
```

实际编写代码的时候，建议按照以下方式创建数据库：

```py
import sqlite3

try:
    with sqlite3.connect("my.db") as conn:
        # interact with database
        pass
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
```

- 使用 `with` 语句，程序会自动帮我们关闭与数据库的连接，这样就无需显式调用 `close()` 方法了
- 使用 `try...except` 语句捕获创建数据库时发生的错误

---
可以向 `connect()` 函数中传入字符串字面量 `':memory:'`，这样可以把新创建的数据库放在**内存**中，这种数据库会一直存在，直到整个程序结束为止。

```py
conn = sqlite3.connect(':memory:')
```


#### CRUD

下面介绍如何在 Python 中实现对 SQLite 表格的增删查改。

- 创建表格：
    - 在创建/打开数据库后（假定数据库内容存在 `conn` 这一 `Connection` 对象实例内），调用其 `cursor()` 方法，以创建 `Cursor` 对象

        ```py
        cursor = conn.cursor()
        ```

- 然后，调用 `Cursor` 对象的 `execute()` 方法，向里面传入 SQLite 的 `CREATE TABLE` 语句，让 Python 执行其中的语句
- 之后，调用 `commit()` 函数来完成对数据库的更改
    - 如果忘记调用的话，数据库的内容就不会被改动
- 完整的代码为：

        ```py
        import sqlite3

        database = '<your_database>'
        create_table = '<create_table_statement>'

        try:
            with sqlite3.connect(database) as conn:
                cursor = conn.cursor()
                cursor.execute(create_table)   
                conn.commit()

        except sqlite3.OperationalError as e:
            print(e)
        ```

    ??? example "例子"

        ```py
        import sqlite3

        sql_statements = [ 
            """CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY, 
                    name text NOT NULL, 
                    begin_date DATE, 
                    end_date DATE
                );""",

            """CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL, 
                    priority INT, 
                    project_id INT NOT NULL, 
                    status_id INT NOT NULL, 
                    begin_date DATE NOT NULL, 
                    end_date DATE NOT NULL, 
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                );"""
        ]

        # create a database connection
        try:
            with sqlite3.connect('my.db') as conn:
                # create a cursor
                cursor = conn.cursor()

                # execute statements
                for statement in sql_statements:
                    cursor.execute(statement)

                # commit the changes
                conn.commit()

                print("Tables created successfully.")
        except sqlite3.OperationalError as e:
            print("Failed to create tables:", e)
        ```

- 插入数据：大体流程与创建表格类似，唯一的不同在于要让 Python 执行的是 SQLite 插入语句，因此传入 `execute()` 方法的参数应该是类似下面的插入语句：

    ```sql
    INSERT INTO table_name(c1, c2)
    VALUES(?,?)
    ```

- 更新数据：大体流程与创建表格类似，唯一的不同在于要让 Python 执行的是 SQLite 更新语句，因此传入 `execute()` 方法的参数应该是更新语句，但可以用 `?` 作为占位符，该占位符之后会被真实的值替代。下面给出完整的代码：

    ```py
    update_statement = 'UPDATE sample_table SET column1=?, column2=? WHERE id = ?'

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(update_statement, (value1, value2, id,))
    conn.commit()
    conn.close()
    ```

- 删除数据：大体流程与创建表格类似，唯一的不同在于要让 Python 执行的是 SQLite 删除语句，因此传入 `execute()` 方法的参数应该是删除语句，但可以用 `?` 作为占位符，该占位符之后会被真实的值替代。下面给出完整的代码：

    ```py
    sql = 'DELETE FROM sample_table WHERE id = ?'
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    conn.close()
    ```

- 查询数据：大体流程与创建表格类似，但有以下区别：
    - 传入 `execute()` 方法的参数为查询语句
    - 用 `fetch` 类方法获取数据，替代原来 `commit()` 函数改变数据库的操作。有以下几种不同的 `fetch` 方法：
        - `fetchall()`：获取满足查询语句的行记录，返回的是元组列表，每个元组包含一个行记录的字段值
        - `fetchone()`：返回的是表示一个行记录的元组
        - `fetchany(size)`：返回数量为 `size` 的元组
    - 也可以使用 `?` 占位符

    ??? example "例子"

        ```py
        import sqlite3

        def get_task_by_id(id: int) -> tuple:
            try:
                with sqlite3.connect('my.db') as conn:
                    cur = conn.cursor()
                    cur.execute('select id, name, priority from tasks where id =?', (id,))
                    row = cur.fetchone()
                    return row, None
            except sqlite3.OperationalError as e:
                return None, e      

        if __name__ == '__main__':
            task, error = get_task_by_id(1)
            if error is not None:
                print(f'Error: {error}')
            else:
                print(task)
        ```


### Node.js


### Java


### C#


### Go