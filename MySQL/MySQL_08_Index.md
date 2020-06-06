# MySQL_08_索引设计与使用

## 索引概述

所有MySQL 列类型都可以被索引，对相关列使用索引是提高SELECT 操作性能的最佳途径。

根据存储引擎可以定义每个表的最大索引数和最大索引长度，每种存储引擎（如MyISAM、InnoDB、BDB、MEMORY 等）对每个表至少支持16 个索引，总索引长度至少为256 字节。

MyISAM 和InnoDB 存储引擎的表默认创建的都是BTREE 索引。

MySQL 目前还不支持函数索引，但是支持前缀索引，即对索引字段的前N 个字符创建索引。前缀索引的长度跟存储引擎相关，对于MyISAM 存储引擎的表，索引的前缀长度可以达到1000 字节长，而对于InnoDB 存储引擎的表，索引的前缀长度最长是767 字节。

MySQL 中还支持全文本（FULLTEXT）索引，该索引可以用于全文搜索。

```sql
-- 请注意前缀的限制应以字节为单位进行测量，而CREATE TABLE 语句中的前缀长度解释为字符数。在为使用多字节字符集的列指定前缀长度时一定要加以考虑。
```

```sql
-- 给表创建索引
-- index_col_name: col_name [(length)] [ASC | DESC]
CREATE [UNIQUE|FULLTEXT|SPATIAL] INDEX index_name [USING index_type]
ON tbl_name (index_col_name,...);

-- eg: 为city 表创建了10 个字节的前缀索引
create index cityname on city (city(10));
```

```sql
-- 索引删除
DROP INDEX index_name on tbl_name;

-- eg
drop index cityname on city;
```



## 索引设计原则

- 最适合索引的列是出现在WHERE子句中的列，或连接子句中指定的列，而不是出现在SELECT 关键字后的选择列表中的列。

- 使用惟一索引。考虑某列中值的分布。索引的列的基数越大，索引的效果越好。

  ```sql
  -- 例如，存放出生日期的列具有不同值，很容易区分各行。而用来记录性别的列，只含有“ M”和“F”，则对此列进行索引没有多大用处，因为不管搜索哪个值，都会得出大约一半的行。
  ```

- 使用短索引。如果对字符串列进行索引，应该指定一个前缀长度，只要有可能就应该这样做。

  ```sql
  -- 例如，如果有一个CHAR(200)列，如果在前10 个或20 个字符内，多数值是惟一的，那么就不要对整个列进行索引。对前10 个或20 个字符进行索引能够节省大量索引空间，也可能会使查询更快。较小的索引涉及的磁盘IO 较少，较短的值比较起来更快。更为重要的是，对于较短的键值，索引高速缓存中的块能容纳更多的键值，因此，MySQL 也可以在内存中容纳更多的值。这样就增加了找到行而不用读取索引中较多块的可能性。
  ```

- 利用最左前缀。在创建一个n 列的索引时，实际是创建了MySQL 可利用的n 个索引。多列索引可起几个索引的作用，因为可利用索引中最左边的列集来匹配行。这样的列集称为最左前缀。

- 不要过度索引。

  ```sql
  -- 每个额外的索引都要占用额外的磁盘空间，并降低写操作的性能。在修改表的内容时，索引必须进行更新，有时可能需要重构，因此，索引越多，所花的时间越长。如果有一个索引很少利用或从不使用，那么会不必要地减缓表的修改速度。此外，MySQL 在生成一个执行计划时，要考虑各个索引，这也要花费时间。
  
  -- 。创建多余的索引给查询优化带来了更多的工作。索引太多，也可能会使MySQL 选择不到所要使用的最好索引。只保持所需的索引有利于查询优化。
  ```

- 对于InnoDB 存储引擎的表，记录默认会按照一定的顺序保存，如果有明确定义的主键，则按照主键顺序保存。如果没有主键，但是有唯一索引，那么就是按照唯一索引的顺序保存。如果既没有主键又没有唯一索引，那么表中会自动生成一个内部列，按照这个列的顺序保存。按照主键或者内部列进行的访问是最快的，所以InnoDB 表尽量自己指定主键，当表中同时有几个列都是唯一的，都可以作为主键的时候，要选择最常作为访问条件的列作为主键，提高查询的效率。

  ```sql
  -- InnoDB表的普通索引都会保存主键的键值，所以主键要尽可能选择较短的数据类型，可以有效地减少索引的磁盘占用，提高索引的缓存效果。
  ```





## BTREE索引与HASH索引

MEMORY 存储引擎的表可以选择使用BTREE 索引或者HASH 索引

**HASH索引特征：**

- 只用于使用=或<=>操作符的等式比较。
- 优化器不能使用HASH 索引来加速ORDER BY 操作。
- MySQL 不能确定在两个值之间大约有多少行。如果将一个MyISAM 表改为HASH 索引的MEMORY 表，会影响一些查询的执行效率。
- 只能使用整个关键字来搜索一行。

BTREE 索引，当使用`>、<、>=、<=、BETWEEN、!=或者<>，或者LIKE 'pattern'（其中'pattern'不以通配符开始）`操作符时，都可以使用相关列上的索引。

```sql
-- 适用于BTREE 索引和HASH索引的范围查询
select * from t1 where key_col = 1 or key_col in (15, 18, 20);

-- 只适用于BTREE索引的范围查询
select * from t1 where key_col > 1 and key_col < 10;
select * from t1 where key_col like 'ab%' or key_col between 'lisa' and 'simon';
```

BTREE 索引和HASH 索引对比使用

```sql
-- 创建一个和city表完全相同的MEMORY存储引擎的表city_memory
create table city_memory(
    city_id smallint unsigned not null auto_increment,
    city varchar(50) not null,
    country_id smallint unsigned not null,
    last_update timestamp not null default current_timestamp on update current_timestamp,
    primary key (city_id),
    key idx_fk_country_id (country_id)  -- 创建索引
)engined=memory default charset=utf8;

insert into city_memory select * from city;

-- 当对索引字段进行范围查询的时候，只有BTREE索引可以通过索引访问
explain select * from city where country_id > 1 and country_id < 10 \G;

-- HASH索引实际上是全表扫描
explain select * from city_memory where country_id > 1 and country_id < 10 \G;
```





## 小结

索引用于快速找出在某个列中有一特定值的行。如果不使用索引，MySQL 必须从第1条记录开始然后读完整个表直到找出相关的行。表越大，花费的时间越多。

如果表中查询的列有一个索引，MySQL 能快速到达一个位置去搜寻数据文件的中间，没有必要看所有数据。
如果一个表有1000 行，这比顺序读取至少快100 倍。注意如果需要访问大部分行，顺序读取要快得多，因为此时应避免磁盘搜索。

大多数MySQL 索引`（如PRIMARY KEY、UNIQUE、INDEX 和FULLTEXT 等）`在`BTREE `中存储。只是空间列类型的索引使用`RTREE`，并且MEMORY 表还支持`HASH 索引`。


