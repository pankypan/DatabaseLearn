# MySQL_05_存储引擎

## MySQL存储引擎概述

和大多数数据库不同，MySQL 中有一个存储引擎的概念，针对不同的存储需求可以选择最优的存储引擎。

插件式存储引擎是MySQL 数据库最重要的特性之一，用户可以根据应用的需要选择如何存储和索引数据、是否使用事务等。

**MySQL 5.0 常用的存储引擎：**

- MyISAM
- InnoDB
- BDB
- MEMORY
- MERGE
- NDB

```SQL
-- 查看当前的默认存储引擎
show variables like "table_type";

-- 查询当前数据库支持的存储引擎
show engines \G;
show variables like "have%";
```

```sql
-- 在创建新表的时候，可以通过增加ENGINE关键字设置新建表的存储引擎

-- 设置为MyISAM
create table ai(
    i bigint(20) not null auto_increment,
    primary key(i)
)engine=MyISAM default charset=gbk;

-- 设置为InnoDB
create table country (
    country_id smallint unsigned not null auto_increment,
    coutry varchar(50) not null,
    last_update timestamp not null default current_timestamp on update current_timestamp,
    primay key (coutry_id)
)engine=InnoDB default charset=gbk;

-- 将表ai 从MyISAM 存储引擎修改成InnoDB 存储引擎
alter table ai engine=innodb;
show create table ai \G;
```





## 各种存储引擎特性

|     特点     | MyISAM | InnoDB | MEMORY | MERGE |
| :----------: | :----: | :----: | :----: | :---: |
|   存储限制   |   有   |  64T   |   有   |  有   |
|   事务安全   |        |  支持  |        |       |
|    锁机制    |  表锁  |  行锁  |  表锁  | 表锁  |
|   B树索引    |  支持  |  支持  |  支持  | 支持  |
|   哈希索引   |        |        |  支持  |       |
|   全文索引   |  支持  |        |        |       |
|   集群索引   |        |  支持  |        |       |
|   数据缓存   |        |  支持  |  支持  |       |
|   索引缓存   |  支持  |  支持  |  支持  | 支持  |
|  数据可压缩  |  支持  |        |        |       |
|   空间使用   |   低   |   高   |  N/A   |  低   |
|   内存使用   |   低   |   高   |  中等  |  低   |
| 批量插入速度 |   高   |   低   |   高   |  高   |
|   支持外键   |        |  支持  |        |       |

### InnoDB

InnoDB 存储引擎提供了具有提交、回滚和崩溃恢复能力的事务安全。但是对比MyISAM的存储引擎，InnoDB 写的处理效率差一些并且会占用更多的磁盘空间以保留数据和索引。

**自动增长列：**

```sql
create table autoincre_demo(
    i smallint not null auto_increment,
    name varchar(10), primary key(i)
)engine=innodb;

insert into autoincre_demo values
(1, '1'),
(0, '2'),
(null, 3);

insert into autoincre_demo values(4, '4');

select last_insert_id();

insert into autoincre_demo(name) values('5'),('6'),('7');
select last_insert_id();
```

对于InnoDB 表，自动增长列必须是索引。如果是组合索引，也必须是组合索引的第一列，但是对于MyISAM 表，自动增长列可以是组合索引的其他列，这样插入记录后，自动增长列是按照组合索引的前面几列进行排序后递增的。

```sql
create table autoincre_demo(
    d1 smallint not null auto_increment,
    d2 smallint not null,
    name varchar(10),
    index(d2, d1)
)engine=myisam;

insert into autoincre_demo(d2,name) values(2,'2'),(3,'3'),(4,'4'),(2,'2'),(3,'3') ,(4,'4');
```

**外键约束：**

MySQL 支持外键的存储引擎只有InnoDB，在创建外键的时候，要求父表必须有对应的索引，子表在创建外键的时候也会自动创建对应的索引

```sql
create table country (
    country_id smallint unsigned not null auto_increment,
    country varchar(50) not null,
    last_update timestamp not null default current_timestamp on update current_timestamp,
    primary key (country_id)
)engine=InnoDB default charset=utf8;

CREATE TABLE city (
city_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
city VARCHAR(50) NOT NULL,
country_id SMALLINT UNSIGNED NOT NULL,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (city_id),
KEY idx_fk_country_id (country_id),
CONSTRAINT `fk_city_country` FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 在创建索引的时候，可以指定在删除、更新父表时，对子表进行的相应操作，包RESTRICT、CASCADE、SET NULL 和NO ACTION。
-- 其中RESTRICT 和NO ACTION 相同，是指限制在子表有关联记录的情况下父表不能更新；
-- CASCADE 表示父表在更新或者删除时，更新或者删除子表对应记录；
-- SET NULL 则表示父表在更新或者删除的时候，子表的对应字段被SET NULL。
```

**存储方式：**

InnoDB 存储表和索引有以下两种方式：

- 使用共享表空间存储，这种方式创建的表的表结构保存在`.frm `文件中，数据和索引保存在`innodb_data_home_dir 和innodb_data_file_path` 定义的表空间中，可以是多个文件。
- 使用多表空间存储，这种方式创建的表的表结构仍然保存在`.frm `文件中，但是每个表的数据和索引单独保存在`.ibd `中。如果是个分区表，则每个分区对应单独的`.ibd`文件，文件名是“表名+分区名”，可以在创建分区的时候指定每个分区的数据文件的位置，以此来将表的IO 均匀分布在多个磁盘上。

```sql
-- 注意：即便在多表空间的存储方式下，共享表空间仍然是必须的，InnoDB 把内部数据词典和未作日志放在这个文件中。
```



### MyISAM

MyISAM 不支持事务、也不支持外键，其优势是访问的速度快，对事务完整性没有要求或者以`SELECT、INSERT `为主的应用基本上都可以使用这个引擎来创建表。

每个MyISAM 在磁盘上存储成3 个文件，其文件名都和表名相同，但扩展名分别是：

- .frm（存储表定义）；
- .MYD（MYData，存储数据）
- .MYI （MYIndex，存储索引）。

数据文件和索引文件可以放置在不同的目录，平均分布IO，获得更快的速度。要指定索引文件和数据文件的路径，需要在创建表的时候通过`DATA DIRECTORY 和INDEXDIRECTORY `语句指定，也就是说不同MyISAM 表的索引文件和数据文件可以放置到不同的路径下。文件路径需要是绝对路径，并且具有访问权限。

MyISAM 类型的表可能会损坏，原因可能是多种多样的，损坏后的表可能不能访问，会提示需要修复或者访问后返回错误的结果。MyISAM 类型的表提供修复的工具，可以用CHECKTABLE 语句来检查MyISAM 表的健康，并用REPAIR TABLE 语句修复一个损坏的MyISAM 表。

MyISAM 的表又支持3 种不同的存储格式，分别是：

- 静态（固定长度）表

  ```sql
  -- 默认的存储格式。
  -- 字段都是非变长字段，这样每个记录都是固定长度的。
  -- 优点：存储非常迅速，容易缓存，出现故障容易恢复；
  -- 缺点：占用的空间通常比动态表多。
  -- 静态表的数据在存储的时候会按照列的宽度定义补足空格，但是在应用访问的时候并不会得到这些空格，这些空格在返回给应用之前已经去掉。（注意：也会去掉内容后面原本存在的空格）
  ```

- 动态表

  ```sql
  -- 动态表中包含变长字段，记录不是固定长度的，
  -- 优点：占用的空间相对较少
  -- 缺点：频繁地更新删除记录会产生碎片，需要定期执行OPTIMIZE TABLE 语句或myisamchk -r 命令来改善性能，并且出现故障的时候恢复相对比较困难。
  ```

- 压缩表

  ```sql
  -- 由myisampack工具创建，占据非常小的磁盘空间。
  -- 每个记录是被单独压缩的，访问开支非常小。
  ```



### MEMORY

MEMORY 存储引擎使用存在内存中的内容来创建表。每个MEMORY 表只实际对应一个磁盘文件，格式是.frm。MEMORY 类型的表访问非常得快，因为它的数据是放在内存中的，并且默认使用HASH 索引，但是一旦服务关闭，表中的数据就会丢失掉。

服务器需要足够内存来维持所有在同一时间使用的MEMORY 表，当不再需要MEMORY表的内容之时，要释放被MEMORY 表使用的内存，应该执行`DELETE FROM 或TRUNCATE TABLE`，或者整个地删除表（使用`DROP TABLE `操作）。

每个MEMORY 表中可以放置的数据量的大小，受到`max_heap_table_size` 系统变量的约束，这个系统变量的初始值是16MB，可以按照需要加大。此外，在定义MEMORY 表的时候，可以通过`MAX_ROWS` 子句指定表的最大行数。

MEMORY 类型的存储引擎主要用在那些内容变化不频繁的代码表，或者作为统计操作的中间结果表，便于高效地对中间结果进行分析并得到最终的统计结果。对MEMORY 存储引擎的表进行更新操作要谨慎，因为数据并没有实际写入到磁盘中，所以一定要对下次重新启动服务后如何获得这些修改后的数据有所考虑。



### MERGE

MERGE 存储引擎是一组MyISAM 表的组合，这些MyISAM 表必须结构完全相同，MERGE表本身并没有数据，对MERGE 类型的表可以进行查询、更新、删除的操作，这些操作实际上是对内部的实际的MyISAM 表进行的。对于MERGE 类型表的插入操作，是通过`INSERT_METHOD `子句定义插入的表，可以有3 个不同的值，使用FIRST 或LAST 值使得插入操作被相应地作用在第一或最后一个表上，不定义这个子句或者定义为NO，表示不能对这个MERGE 表执行插入操作。

可以对MERGE 表进行DROP 操作，这个操作只是删除MERGE 的定义，对内部的表没有任何的影响。

MERGE 表在磁盘上保留两个文件，文件名以表的名字开始，一个`.frm `文件存储表定义，另一个`.MRG` 文件包含组合表的信息，包括MERGE 表由哪些表组成、插入新的数据时的依据。可以通过修改`.MRG `文件来修改MERGE 表，但是修改后要通过`FLUSH TABLES `刷新。

```SQL
-- 创建三张表
create table payment_2018(
    country_id smallint,
    payment_date datetime,
    amount decimal(15, 2),
    key idx_fk_country_id (country_id)
)engine=myisam;
create table payment_2019(
    country_id smallint,
    payment_date datetime,
    amount decimal(15, 2),
    key idx_fk_country_id (country_id)
)engine=myisam;
create table payment_all(
    country_id smallint,
    payment_date datetime,
    amount decimal(15, 2),
    index(country_id)
)engine=merge union=(payment_2018, payment_2019) insert_method=last;

-- 分别向payment_2018和payment_2019表中插入测试数据
insert into payment_2018 values(1,'2018-05-01',100000),(2,'2018-08-15',150000);
insert into payment_2019 values(1, '2019-02-20', 35000), (2, '2019-07-15', 220000);

-- 分别查看3张表
 select * from payment_2018;
 select * from payment_2019;
 select * from payment_all;
```



## 选择存储引擎

- InnoDB

  ```SQL
  -- 用于事务处理应用程序，支持外键。
  -- 如果应用对事务的完整性有比较高的要求，在并发条件下要求数据的一致性，数据操作除了插入和查询以外，还包括很多的更新、删除操作
  -- InnoDB 存储引擎除了有效地降低由于删除和更新导致的锁定，还可以确保事务的完整提交（Commit）和回滚（Rollback），对于类似计费系统或者财务系统等对数据准确性要求比较高的系统，InnoDB 都是合适的选择。
  ```

- MyISAM

  ```SQL
  -- 是以读操作和插入操作为主，只有很少的更新和删除操作，并且对事务的完整性、并发性要求不是很高，
  -- MyISAM 是在Web、数据仓储和其他应用环境下最常使用的存储引擎之一。
  ```

- MEMORY

  ```SQL
  -- 将所有数据保存在RAM中，在需要快速定位记录和其他类似数据的环境下，可提供极快的访问。
  -- MEMORY的缺陷是对表的大小有限制，太大的表无法CACHE在内存中，
  -- 其次是要确保表的数据可以恢复，数据库异常终止后表中的数据是可以恢复的。
  -- MEMORY 表通常用于更新不太频繁的小表，用以快速得到访问结果。
  ```

- MERGE

  ```SQL
  -- 用于将一系列等同的MyISAM 表以逻辑方式组合在一起，并作为一个对象引用它们。
  -- MERGE 表的优点在于可以突破对单个MyISAM表大小的限制，并且通过将不同的表分布在多个磁盘上，可以有效地改善MERGE表的访问效率。这对于诸如数据仓储等VLDB环境十分适合。
  ```





