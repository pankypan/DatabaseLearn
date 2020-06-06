# MongoDB基本常用命令

## 案例需求

存放文章评论的数据存放到MongoDB中，数据结构参考如下：
数据库：articledb  

| 专栏文章评论   | comment        |                  |                           |
| -------------- | -------------- | ---------------- | ------------------------- |
| 字段名称       | 字段含义       | 字段类型         | 备注                      |
| _id            | ID             | ObjectId或String | Mongo的主键的字段         |
| articleid      | 文章ID         | String           |                           |
| content        | 评论内容       | String           |                           |
| userid         | 评论人ID       | String           |                           |
| nickname       | 评论人昵称     | String           |                           |
| createdatetime | 评论的日期时间 | Date             |                           |
| likenum        | 点赞数         | Int32            |                           |
| replynum       | 回复数         | Int32            |                           |
| state          | 状态           | String           | 0：不可见；1：可见；      |
| parentid       | 上级ID         | String           | 如果为0表示文章的顶级评论 |





## 数据库操作

### 选择和创建

选择和创建数据库的语法格式：  

```powershell
use 数据库名称
```

如果数据库不存在则自动创建，例如，以下语句创建 articledb 数据库：  

```powershell
use articledb
```


查看有权限查看的所有的数据库命令

```powershell
show dbs
或
show databases
```

> **注意**: 在 MongoDB 中，集合只有在内容插入后才会创建! 就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建 



### 查看当前正在使用

```powershell
db
```

MongoDB 中默认的数据库为 test，如果你没有选择数据库，集合将存放在 test 数据库中 .



**注意：**

数据库名可以是满足以下条件的任意UTF-8字符串：

- 不能是空字符串（"")
- 不得含有`' '（空格)、.、$、/、\和\0 (空字符)`
- 应全部小写
- 最多64字节 



有一些数据库名是保留的，可以直接访问这些有特殊作用的数据库:

- **admin**: 从权限的角度来看，这是"root"数据库。要是将一个用户添加到这个数据库，这个用户自动继承所有数据库的权限。一些特定的服务器端命令也只能从这个数据库运行，比如列出所有的数据库或者关闭服务器。  
- **local**: 这个数据永远不会被复制，可以用来存储限于本地单台服务器的任意集合
- **config**: 当Mongo用于分片设置时，config数据库在内部使用，用于保存分片的相关信息



### 删除

MongoDB 删除数据库的语法格式如下：

```powershell
db.dropDatabase()
```

> 提示：主要用来删除已经持久化的数据库  





## 集合操作

集合，类似关系型数据库中的表。可以显示的创建，也可以隐式的创建  

### 显式创建

基本语法格式:

```powershell
db.createCollection(name)
```

参数说明：

- name: 要创建的集合名称  



集合的命名规范：

- 集合名不能是空字符串`""`
- 集合名不能含有`\0字符（空字符)`，这个字符表示集合名的结尾
- 集合名不能以`system.`开头，这是为系统集合保留的前缀
- 用户创建的集合名字不能含有保留字符。有些驱动程序的确支持在集合名里面包含，这是因为某些系统生成的集合中包含该字符。除非你要访问这种系统创建的集合，否则千万不要在名字里出现$



例如：创建一个名为 mycollection 的普通集合。  

```powershell
db.createCollection('mycollection')
```



### 查看

查看当前库中的集合:  

```powershell
show collections
或
show tables
```



### 隐式创建

当向一个集合中插入一个文档的时候，如果集合不存在，则会自动创建集合。  

> 提示：通常我们使用隐式创建文档即可。  



### 删除

集合删除语法格式如下：  

```powershell
db.collection.drop()
```

**返回值**

如果成功删除选定集合，则 drop() 方法返回 true，否则返回 false 



例如：要删除mycollection集合

```powershell
db.mycollection.drop()
```





## 文档基本CRUD

文档`document`的数据结构和 JSON 基本一样。所有存储在集合中的数据都是 `BSON` 格式。  



### 插入

#### 单个插入

使用`insert() `或 `save() `方法向集合中插入文档，语法如下:

```powershell
db.collection.insert(
<document or array of documents>,
{
writeConcern: <document>,
ordered: <boolean>
}
)
```

**参数：**

| Parameter    | Type              | Description                                                  |
| ------------ | ----------------- | ------------------------------------------------------------ |
| document     | document or array | 要插入到集合中的文档或文档数组。（(json格式）                |
| writeConcern | document          | Optional. A document expressing the write concern. Omit to use the default write concern. See Write Concern.Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see Transactions and Write Concern. |
| ordered      | boolean           | 可选。如果为真，则按顺序插入数组中的文档，如果其中一个文档出现错误，MongoDB将返回而 不处理数组中的其余文档。如果为假，则执行无序插入，如果其中一个文档出现错误，则继续处理 数组中的主文档。在版本2.6+中默认为true |

**【示例】**
要向comment的集合(表)中插入一条测试数据：  

```powershell
db.comment.insert({"articleid":"100000","content":"今天天气真好，阳光明媚","userid":"1001","nickname":"Rose","createdatetime":new Date(),"likenum":NumberInt(10),"state":null})
```









#### 批量插入





### 基本查询



### 插入



### 更新



### 删除































