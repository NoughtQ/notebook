---
counter: true
---

# GORM

!!! abstract "参考资料"

    - [GORM 指南](https://gorm.io/zh_CN/docs/index.html)

!!! info "阅读前须知"

    初次学 GORM，仅参考官方指南（~~感觉看得莫名难受~~），有些语法不甚了解，可能有一些错误。若读者发现错误请及时指出，万分感谢！


## 连接

与数据库的连接（以 MySQL 为例）：

``` go
import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

func main() {
    dsn := "user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
    
    // db 为数据库的名称，后面关于数据库的操作一般都以这个名称为前缀
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
}
```

??? info "高级操作"

    === "高级配置"

        ``` go
        db, err := gorm.Open(mysql.New(mysql.Config{
            DSN: "gorm:gorm@tcp(127.0.0.1:3306)/gorm?charset=utf8&parseTime=True&loc=Local", // DSN data source name
            DefaultStringSize: 256,           // string 类型字段的默认长度
            DisableDatetimePrecision: true,   // 禁用 datetime 精度
            DontSupportRenameIndex: true,     // 重命名索引时采用删除并新建的方式
            DontSupportRenameColumn: true,    // 用 `change` 重命名列
            SkipInitializeWithVersion: false, // 根据当前 MySQL 版本自动配置
        }), &gorm.Config{})
        ```

    === "自定义 MySQL 驱动"

        ``` go
        db, err := gorm.Open(mysql.New(mysql.Config{
            DriverName: "my_mysql_driver",
            DSN: "gorm:gorm@tcp(localhost:9910)/gorm?charset=utf8&parseTime=True&loc=Local", 
        }), &gorm.Config{})
        ```

    === "与现有的数据库连接"

        ``` go
        sqlDB, err := sql.Open("mysql", "mydb_dsn")
        gormDB, err := gorm.Open(mysql.New(mysql.Config{
            Conn: sqlDB,
        }), &gorm.Config{})
        ```

## 模型定义

模型：Go **结构体** <-> **数据表**

:chestnut:：

``` go
type User struct {
    ID           uint           
    Name         string         
    Email        *string        
    Age          uint8          
    Birthday     *time.Time     
    MemberNumber sql.NullString 
    ActivatedAt  sql.NullTime   
    CreatedAt    time.Time      
    UpdatedAt    time.Time      
}
```

-  `*string` 和 `*time.Time` 类型表示可空字段
- 一些约定：
    - 字段 `ID` 默认为模型的主键
    - GROM 会将结构名/字段名转为下划线间隔（被称为**蛇形命名法**）（结构名还会加上复数形式）的表名/列名
    - 特殊字段 `CreatedAt` 和 `UpdatedAt` 在记录被创建或更新的时候，GORM 会自动向内填充时间
        - 创建时间追踪：`CreatedAt` 字段后加标签 \`gorm:"autoCreateTime"\`
        - 更新时间追踪：`UpdatedAt` 字段后加标签 \`gorm:"autoUpdateTime"\`
        - 标签末尾可以指定单位（未指定默认为 s）：`nano` 纳秒，`milli` 毫秒（用法：\`gorm:"autoUpdateTime:milli"\`）
- 预定义结构体 `gorm.Model`

``` go
type Model struct {
    ID        uint           `gorm:"primaryKey"`
    CreatedAt time.Time
    UpdatedAt time.Time
    // DeletedAt 用于软删除（标记删除，但实际上并未从数据库删除）
    DeletedAt gorm.DeletedAt `gorm:"index"`
}
```

??? note "字段标签"

    !!! warning "注意事项"

        - 标签以 `gorm:` 开头
        - 推荐驼峰式表示法
        - 用分号间隔不同的标签
        - ...

    - `column`：指定列名
    - `type`：指定列的数据类型
    - `serializer`：序列化器
    - `size`：指定数据类型的大小或长度
    - `primaryKey`：指定该列位表的主键
    - `unique`：指定该列为唯一键（该列所有的值互不相同）
    - `default`：指定列的默认值
    - `precision`：指定列的精度
    - `scale`：指定列的大小
    - `not null`：指定列为非空
    - `autoIncrement`：自动增长
    - `autoIncrementIncrement`：可以控制的自动增长
    - `embedded`：嵌套字段
    - `embeddedPrefix`：嵌入字段的列名前缀
    - `autoCreateTime`
    - `autoUpdateTime`
    - `index`：根据参数创建索引
    - `uniqueIndex`：创建唯一索引
    - `check`：创建检查约束
    - `<-`：设置写入权限
        - `<-:create`：只创建
        - `<-:update`：只更新
        - `<-:false`：无写入权限
        - `<-`：创建&更新
    - `->`：设置读取权限
        - `->:false`：无读取权限
    - `-`：无读写权限
        - `-:migration`：无迁移权限
        - `-:all`：无读写和迁移权限
    - `comment`：添加注释

## CRUD

### 创建

- 创建记录

``` go
// 单条记录
user := User{Name: "NoughtQ", Age: 20, Birthday: time.Now()}

// 多条记录
users := []*User{
    {Name: "Jinzhu", Age: 18, Birthday: time.Now()},
    {Name: "Jackson", Age: 19, Birthday: time.Now()},
}

// 还可以用 map[string]interface{} 或 []map[string]interface{}{} 来创建记录
// 用法上分别对应结构体和结构体数组

result := db.Create(&user) // 通过结构体的指针来创建
```

- 使用：

``` go
user.ID             // 返回插入数据的主键
result.Error        // 返回 error
result.RowsAffected // 返回插入记录的条数
```

- 用指定字段创建记录

``` go
// 选择结构体的指定字段，将其插入到数据表内
db.Select("Name", "Age", "CreatedAt").Create(&user)

// 忽略指定字段，其余字段的数据插入到数据表内
db.Omit("Name", "Age", "CreatedAt").Create(&user)
```

- 批量插入

``` go
// 方法同插入单个记录
var users = []User{{Name: "user1"}, {Name: "user2"}, {Name: "user3"}}
db.Create(&users)

// 指定批量插入的批次大小
db.CreateInBatches(users, 100)
```

- 创建钩子：在调用创建记录相关的方法时会调用钩子函数，与创建记录相关的有四种：`BeforeSave`、`BeforeCreate`、`AfterSave`、`AfterCreate`

    ``` go
    func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
    u.UUID = uuid.New()

        if u.Role == "admin" {
            return errors.New("invalid role")
        }
        return
    }
    ```

    - 创建钩子函数后，如果在创建记录时不想用的话，可以用 `SkipHooks` 会话模式跳过：

    ``` go
    DB.Session(&gorm.Session{SkipHooks: true}).Create(&user)

    DB.Session(&gorm.Session{SkipHooks: true}).Create(&users)

    DB.Session(&gorm.Session{SkipHooks: true}).CreateInBatches(users, 100)
    ```

    - 如果是用映射创建的记录，则不会执行钩子函数

### 查询

- 查询单个记录

    ``` go
    // 获取第一条记录（主键升序）
    db.First(&user)
    // 等价于 SQL 语句：SELECT * FROM users ORDER BY id LIMIT 1;

    // 获取一条记录，没有指定排序字段
    db.Take(&user)
    // 等价于 SQL 语句：SELECT * FROM users LIMIT 1;

    // 获取最后一条记录（主键降序）
    db.Last(&user)
    // 等价于 SQL 语句：SELECT * FROM users ORDER BY id DESC LIMIT 1;

    result := db.First(&user)
    result.RowsAffected // 返回找到的记录数
    result.Error        // 返回 error 或 nil

    // 检查 ErrRecordNotFound 错误
    errors.Is(result.Error, gorm.ErrRecordNotFound)
    ```

    - 如果没有指定主键，那么就按第一个字段进行排序
    - 根据主键查询
        - 数字类型
        ``` go
        db.First(&user, 10)
        // 等价于 SQL 语句：SELECT * FROM users WHERE id = 10;

        db.First(&user, "10")
        // 等价于 SQL 语句：SELECT * FROM users WHERE id = 10;

        db.Find(&users, []int{1,2,3})
        // 等价于 SQL 语句：SELECT * FROM users WHERE id IN (1,2,3);
        ```

        - 字符串型：
        ``` go
        db.First(&user, "id = ?", "1b74413f-f3b8-409f-ac47-e8c062e3472a")
        // 等价于 SQL 语句：SELECT * FROM users WHERE id = "1b74413f-f3b8-409f-ac47-e8c062e3472a";
        ```

- 查询全部记录
``` go

result := db.Find(&users)
// 等价于 SQL 语句：SELECT * FROM users;

result.RowsAffected // 返回找到的记录数, 等价于 `len(users)`
result.Error        // 返回 error
```

- 条件
    - 基本语法：`db.Where(condition, val1, val2, ...).Find(&table_name)`
    - 简单条件（只展示 `db.Where()` 的参数部分）
        - 获取第一个匹配的记录（这里使用 `First()` 方法而不是 `Find()`）：`"field_name = ?", "NoughtQ"`
        - 获取所有匹配的记录：`"name <> ?", "NoughtQ"`
        - IN：`"name IN ?", []string{"person1", "person2"}`
        - LIKE：`"name LIKE ?", "%nought%"`
        - AND：`"name = ? AND age >= ?", "NoughtQ", "20"`
            - 可以使用映射来模拟 AND 语句
        - Time：`"updated_at > ?", lastWeek`
        - BETWEEN：`"created_at BETWEEN ? AND ?", lastWeek, today`
    - Or 条件：格式为 `db.Where(...).Or(...).Find(...)`，其中 `Or` 后面的参数与 `Where` 参数格式一样
    - 否定形式（也就是 SQL 语句的 `NOT`）：使用 `db.Not()` 替代 `db.Where()`，语法类似
- 排序
    - 格式为 `db.Order("column1 desc, column2").Find(&table_name)`
    - 等价 SQL 语句：`SELECT * FROM table_name ORDER BY column1 desc, column2;`
    - 其中 `desc` 表示降序，可换成 `asc` 升序
- `Limit`：限制最大查询数量
- `Offset`
- `Group` 和 `Having`
- `Distinct`
- `Joins`
- `Scan`

### 更新

- 保存所有字段（包括零值）：`db.Save(&table_name)`
- 更新单个列：
``` go
// 根据条件更新
db.Model(&User{}).Where("active = ?", true).Update("name", "hello")
// 等价的 SQL：UPDATE users SET name='hello' WHERE active=true;
```

- 更新多列：
``` go
// 根据 `struct` 更新属性，只会更新非零值的字段
db.Model(&user).Where("id = ?", 111).Updates(User{Name: "hello", Age: 18, Active: false})
// UPDATE users SET name='hello', age=18, active=false WHERE id = 111;

// 根据 `map` 更新属性，效果类似上一句
db.Model(&user).Where("id = ?", 111).Updates(map[string]interface{}{"name": "hello", "age": 18, "active": false})
```

- 配合 `Select()` 或 `Omit()` 可选取指定字段（用于 `Updates()` 之前）
- 更新钩子

### 删除

- 删除一条记录：`db.Delete(&table_name, id)`
    - 删除对象需要指定主键（`id`），否则会触发批量删除
    - 主键可以是数字，也可以是字符串
    - 使用 `Where()` 指定额外条件
- 钩子函数
- 返回被删除的数据：
- 软删除：若结构体包含 `gorm.DeleteAt` 字段，在删除操作中 GORM 不会将数据从数据库中删除，而是将它“隐藏”起来，之后的查询语句无法查到该记录
    - 可以使用 `Unscoped()` 查询被软删除的记录
    ``` go
    db.Unscoped().Where(...).Find(&table_name)
    ```

    - 永久删除：`db.Unscoped().Delete(&table_name)`

???+ note "链式方法"

    有些方法可以连在一起写一长串，被称为链式方法(chain method)，下列方法均属于链式方法：

    - `Where`
    - `Select`
    - `Omit`
    - `Joins`
    - `Scopes`
    - `Preload`
    - `Raw`

    还有一些方法只能用在链上的最后部分，称为完成方法(finisher methods)，包括：

    - `Create`
    - `First`
    - `Find`
    - `Take`
    - `Save`
    - `Update`
    - `Delete`
    - `Scan`
    - `Row`
    - `Rows`

## 迁移

- `AutoMigrate`：用于自动迁移表，保持表是最新状态的

``` go
// 可以一次性迁移多张表
db.AutoMigrate(&User{}, &Order{})

// AutoMigrate 会自动创建数据库外键约束，可以在初始化时禁用此功能
db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{
  DisableForeignKeyConstraintWhenMigrating: true,
})
```

- `Migrator` 接口，为数据库构建独立的迁移
    - 返回当前使用的数据库名：`db.Migrator().CurrentDatabase()`
    - 表
    ``` go
    // 为 `User` 创建表
    db.Migrator().CreateTable(&User{})

    // 将 "ENGINE=InnoDB" 添加到创建 `User` 的 SQL 里去
    db.Set("gorm:table_options", "ENGINE=InnoDB").Migrator().CreateTable(&User{})

    // 检查 `User` 对应的表是否存在
    db.Migrator().HasTable(&User{})
    db.Migrator().HasTable("users")

    // 如果存在表则删除（删除时会忽略、删除外键约束)
    db.Migrator().DropTable(&User{})
    db.Migrator().DropTable("users")

    // 重命名表
    db.Migrator().RenameTable(&User{}, &UserInfo{})
    db.Migrator().RenameTable("users", "user_infos")
    ```

    - 列
    ``` go
    // 添加 name 字段
    db.Migrator().AddColumn(&User{}, "Name")
    // 删除 name 字段
    db.Migrator().DropColumn(&User{}, "Name")
    // 修改 name 字段
    db.Migrator().AlterColumn(&User{}, "Name")
    // 检查 name 字段是否存在
    db.Migrator().HasColumn(&User{}, "Name")
    // 字段重命名
    db.Migrator().RenameColumn(&User{}, "Name", "NewName")
    // 字段类型
    db.Migrator().ColumnTypes(&User{}) ([]gorm.ColumnType, error)
    ```

    - 视图(view)，有以下规则：
        - 需要有 `Query`
        - 如果 `Replace: true`，执行 `CREATE OR REPLACE` SQL 语句，否则执行 `CREATE` 语句
        - 如果 `CheckOption` 非空，将其附加到 SQL 语句后
        ``` go
        query := db.Model(&User{}).Where("age > ?", 20)

        // 创建视图
        db.Migrator().CreateView("users_pets", gorm.ViewOption{Query: query})
        // 等价于 SQL 语句：CREATE VIEW `users_pets` AS SELECT * FROM `users` WHERE age > 20

        // 创建或取代视图
        db.Migrator().CreateView("users_pets", gorm.ViewOption{Query: query, Replace: true})
        // 等价于 SQL 语句：CREATE OR REPLACE VIEW `users_pets` AS SELECT * FROM `users` WHERE age > 20

        // 带有检查选项的创建视图
        db.Migrator().CreateView("users_pets", gorm.ViewOption{Query: query, CheckOption: "WITH CHECK OPTION"})
        // 等价于 SQL 语句：CREATE VIEW `users_pets` AS SELECT * FROM `users` WHERE age > 20 WITH CHECK OPTION

        // 删除视图
        db.Migrator().DropView("users_pets")
        // 等价于 SQL 语句：DROP VIEW IF EXISTS "users_pets"
        ```

    - 约束（可用于创建外键）
    ``` go
    type UserIndex struct {
    Name  string `gorm:"check:name_checker,name <> 'NoughtQ'"`
    }

    // 创建约束
    db.Migrator().CreateConstraint(&User{}, "name_checker")

    // 删除约束
    db.Migrator().DropConstraint(&User{}, "name_checker")

    // 检查约束是否存在
    db.Migrator().HasConstraint(&User{}, "name_checker")
    ```

    - 索引
    ``` go
    type User struct {
    gorm.Model
    Name string `gorm:"size:255;index:idx_name,unique"`
    }

    // 为 Name 字段创建索引
    db.Migrator().CreateIndex(&User{}, "Name")
    db.Migrator().CreateIndex(&User{}, "idx_name")

    // 删除 Name 字段的索引
    db.Migrator().DropIndex(&User{}, "Name")
    db.Migrator().DropIndex(&User{}, "idx_name")

    // 检查索引是否存在
    db.Migrator().HasIndex(&User{}, "Name")
    db.Migrator().HasIndex(&User{}, "idx_name")

    // 重命名索引
    db.Migrator().RenameIndex(&User{}, "Name", "Name2")
    db.Migrator().RenameIndex(&User{}, "idx_name", "idx_name_2")
    ```

## 事务

- 禁用默认事务（可以提升性能）：
``` go
db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{
  SkipDefaultTransaction: true,
})
```

- 创建事务
``` go
db.Transaction(func(tx *gorm.DB) error {
  // 在事务中执行一些 db 操作（从这里开始应该使用 'tx' 而不是 'db'）
  if err := tx.Create(&Users{Name: "Alpha"}).Error; err != nil {
    // 返回任何错误都会回滚事务
    return err
  }

  if err := tx.Create(&Users{Name: "Beta"}).Error; err != nil {
    return err
  }

  // 返回 nil 提交事务
  return nil
})
```

- 事务可以嵌套
- 关于事务的控制方法
    - 开始：`tx := db.Begin()`
    - 回滚：`tx.RollBack()`
    - 提交：`tx.Commit()`
    - 设置标记点：`tx.SavePoint("pt1")`
    - 回滚到指定标记点：`tx.RollbackTo("pt1")`


## 钩子

钩子(hook)是在 CRUD 等操作前后自动调用的（自己指定的）函数。下面分情况介绍可用的钩子及其执行流程：

- 创建
``` go
// 开始事务
BeforeSave
BeforeCreate
// 关联前的 save
// 插入记录至 db
// 关联后的 save
AfterCreate
AfterSave
// 提交或回滚事务
```

- 查询
``` go
// 从 db 中加载数据
// Preloading (eager loading)
AfterFind
```

- 更新
``` go
// 开始事务
BeforeSave
BeforeUpdate
// 关联前的 save
// 更新 db
// 关联后的 save
AfterUpdate
AfterSave
// 提交或回滚事务
```

- 删除
``` go
// 开始事务
BeforeDelete
// 删除 db 中的数据
AfterDelete
// 提交或回滚事务
```

函数声明格式：

``` go
func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
  if condition {
    // ...
  }
  return
}
```

## 关联

关联类型：

- Belongs To：两个模型间建立一对一的连接，这个模型的每一个实例都「属于」另一个模型的一个实例
    ``` go hl_lines="6"
    // 主表
    type User struct {
        gorm.Model
        Name      string
        CompanyID string
        Company   Company `gorm:"foreignKey:CompanyRefer;references:Code"` 
    }

    // 从表
    type Company struct {
        ID   int
        Code string
        Name string
    }
    ```

    - 主表必须有**外键**，外键的名称默认为主表的名称 + 从表主键的字段名称
    - 通过重写**引用**，可以修改参考的从表字段（上面的代码将其改为参考 `Code` 字段（默认参考 `ID` 字段））

- Has One：类似前者（包括语法），但它的关联不是「属于」，而是「包含」或「拥有」
- Has Many：两个模型间建立了一对多的连接
    ``` go
    type User struct {
        gorm.Model
        MemberNumber string
        CreditCards  []CreditCard `gorm:"foreignKey:UserNumber;references:MemberNumber"`
    }

    type CreditCard struct {
        gorm.Model
        Number     string
        UserNumber string
    }
    ```

- Many To Many：在两个模型间添加一张连接表

[关于关联的操作](https://gorm.io/zh_CN/docs/associations.html#%E5%85%B3%E8%81%94%E6%A8%A1%E5%BC%8F)