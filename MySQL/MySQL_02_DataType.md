# MySQL_02_数据类型

## 数值类型

MySQL 支持所有标准SQL 中的数值类型，其中包括严格数值类型`（INTEGER、SMALLINT、DECIMAL、NUMERIC）`，以及近似数值数据类型`（FLOAT、REAL 和DOUBLE PRECISION）`，并在此基础上做了扩展。扩展后增加了`TINYINT、MEDIUMINT` 和`BIGINT` 这3 种长度不同的整型，并增加了`BIT` 类型，用来存放位数据。

**整数：**

|   整数类型   | 字节 |               最小值                |                         最大值                         |
| :----------: | :--: | :---------------------------------: | :----------------------------------------------------: |
|   TINYINT    |  1   |         有符号-128;无符号 0         |                 有符号 127;无符号 255                  |
|   SMALLINT   |  2   |        有符号-32768;无符号 0        |               有符号 32767;无符号 65535                |
|  MEDIUMINT   |  3   |       有符号-8388608;无符号 0       |             有符号 8388607;无符号 1677215              |
| INT、INTEGER |  4   |     有符号-2147483648;无符号 0      |          有符号 2147483647;无符号 4294967295           |
|    BIGINT    |  8   | 有符号-9223372036854775808;无符号 0 | 有符号 9223372036854775807;无符号 18446744073709551615 |

**小数：**

| 浮点数类型 | 字节 |          最小值          |          最大值          |
| :--------: | :--: | :----------------------: | :----------------------: |
|   FLOAT    |  4   |     ±1.175494351E-38     |     ±3.402823466E+38     |
|   DOUBLE   |  8   | ±2.2250738585072014E-308 | ±1.7976931348623157E+308 |

|      定点数类型       | 字节 |                             描述                             |
| :-------------------: | :--: | :----------------------------------------------------------: |
| DEC(M,D),DECIMAL(M,D) | M+2  | 最大取值范围与DOUBLE 相同，给定DECIMAL 的有效取值范围由M和D决定 |

**BIT：**

| 位类型 | 字节 | 最小值 | 最大值  |
| :----: | :--: | :----: | :-----: |
| BIT(M) | 1～8 | BIT(1) | BIT(64) |



### 整数

整型数据，MySQL 还支持在类型名称后面的小括号内指定显示宽度

```sql
create table t1 (
    id1 int,
    id2 int(5)
);

desc t1;

alter table t1 modify id1 int zerofill;
alter table t1 modify id2 int(5) zerofill;
```

整数类型还有一个属性：`AUTO_INCREMENT`。在需要产生唯一标识符或顺序值时，可利用此属性，这个属性只用于整数类型。

对于任何想要使用`AUTO_INCREMENT `的列，应该定义为`NOT NULL`，并定义为`PRIMARY KEY` 或定义为`UNIQUE `键。

```sql
create table ai (
    id int auto_increment not null primary key
);

create table ai2(
    id int auto_increment not null,
    primary key(id)
);

create table ai3(
    id int auto_increment not null,
    unique(id)
);
```

### 小数

MySQL表示小数：

- 浮点数--`float`&`double`
- 定点数--`decimal`。定点数在MySQL 内部以字符串形式存放，比浮点数更精确，适合用来表示货币等精度高的数据。

浮点数和定点数都可以用类型名称后加`(M,D)`的方式来进行表示，“(M,D)”表示该值一共显示M 位数字（整数位+小数位），其中D 位位于小数点后面，M 和D 又称为精度和标度。

```sql
create table t1(
    'id1' float(5, 2) default null,
    'id2' float(5, 2) default null,
    'id3' decimal(6, 2) default null
);

desc t1;
```

### BIT

BIT（位）类型，用于存放位字段值，BIT(M)可以用来存放多位二进制数，M 范围从1～64，如果不写则默认为1 位。对于位字段，直接使用SELECT 命令将不会看到结果，可以用bin()（显示为二进制格式）或者hex()（显示为十六进制格式）函数进行读取。

```sql
select bin(id), hex(id) from t2;
```





## 日期和时间类型

| 日期和时间类型 | 字节 |       最小值        |       最大值        |
| :------------: | :--: | :-----------------: | :-----------------: |
|      DATE      |  4   |     1000-01-01      |     9999-12-31      |
|    DATETIME    |  8   | 1000-01-01 00:00:00 | 9999-12-31 23:59:59 |
|   TIMESTAMP    |  4   |   19700101080001    |  2038 年的某个时刻  |
|      TIME      |  3   |     -838:59:59      |      838:59:59      |
|      YEAR      |  1   |        1901         |        2155         |

这些数据类型的主要区别如下：

- 如果要用来表示年月日，通常用DATE 来表示
- 如果要用来表示年月日时分秒，通常用DATETIME 表示
- 如果只用来表示时分秒，通常用TIME 来表示
- 如果需要经常插入或者更新日期为当前系统时间，则通常使用TIMESTAMP 来表示。TIMESTAMP 值返回后显示为“YYYY-MM-DD HH:MM:SS”格式的字符串，显示宽度固定为19 个字符。如果想要获得数字值，应在TIMESTAMP 列添加+0。
- 如果只是表示年份，可以用YEAR 来表示，它比DATE 占用更少的空间。YEAR 有2 位或4 位格式的年。默认是4 位格式。在4 位格式中，允许的值是1901～2155 和0000。在2 位格式中，允许的值是70～69，表示从1970～2069 年。MySQL 以YYYY 格式显示YEAR值。

```sql
create table t (
    'd' date,
    't' time,
    'dt' datetime
);

desc t;

-- 用now()函数插入当前日期
insert into t values(
    now(),
    now(),
    now()
);
```

TIMESTAMP特性：

- 系统给`field`自动创建了默认值`CURRENT_TIMESTAMP（系统日期）`

  ```sql
  create table t (
      'id1' timestamp
  );
  
  desc t;
  
  -- ，MySQL只给表中的第一个TIMESTAMP字段设置,默认值为系统日期，如果有第二个TIMESTAMP类型，则默认值设置为0值
  alter table t id2 timestamp;
  
  show create table t \G;
  ```

- 和时区相关

  ```sql
  create table 't8' (
      'id1' timestamp not null default current_timestamp,
      'id2' datetime default null
  );
  
  show variables like 'time_zone';
  
  -- 修改时区为东九区
  set time_zone='+9:00';
  ```

TIMESTAMP和DATETIME比较：

- TIMESTAMP支持的时间范围较小，其取值范围从19700101080001到2038年的某个时间，而DATETIME是从1000-01-01 00:00:00到9999-12-31 23:59:59，范围更大。
- 表中的第一个TIMESTAMP列自动设置为系统时间。如果在一个TIMESTAMP列中插入NULL，则该列值将自动设置为当前的日期和时间。在插入或更新一行但不明确给TIMESTAMP列赋值时也会自动设置该列的值为当前的日期和时间，当插入的值超出取值范围时，MySQL认为该值溢出，使用“0000-00-00 00:00:00”进行填补。
- TIMESTAMP的插入和查询都受当地时区的影响，更能反应出实际的日期。而DATETIME则只能反应出插入时当地的时区，其他时区的人查看数据必然会有误差的。
- TIMESTAMP的属性受MySQL版本和服务器SQLMode的影响很大，本章都是以MySQL5.0为例进行介绍，在不同的版本下可以参考相应的MySQL帮助文档。





## 字符串类型

MySQL 包括了`CHAR、VARCHAR、BINARY、VARBINARY、BLOB、TEXT、ENUM 和SET `等多种字符串类型。

|   字符串类型   | 字节 |                     描述及存储需求                     |
| :------------: | :--: | :----------------------------------------------------: |
|   CHAR（M）    |  M   |                 M 为0～255 之间的整数                  |
|  VARCHAR（M）  |  M   |       M 为0～65535 之间的整数，值的长度+1 个字节       |
|    TINYBLOB    |      |         允许长度0～255 字节，值的长度+1 个字节         |
|      BLOB      |      |        允许长度0～65535 字节，值的长度+2 个字节        |
|   MEDIUMBLOB   |      |      允许长度0～167772150 字节，值的长度+3 个字节      |
|    LONGBLOB    |      |     允许长度 0～4294967295 字节，值的长度+4 个字节     |
|    TINYTEXT    |      |         允许长度0～255 字节，值的长度+2 个字节         |
|      TEXT      |      |        允许长度0～65535 字节，值的长度+2 个字节        |
|   MEDIUMTEXT   |      |      允许长度0～167772150 字节，值的长度+3 个字节      |
|    LONGTEXT    |      |     允许长度 0～4294967295 字节，值的长度+4 个字节     |
| VARBINARY（M） |  M   | 允许长度0～M 个字节的变长字节字符串，值的长度+1 个字节 |
|  BINARY（M）   |  M   |          允许长度0～M 个字节的定长字节字符串           |



### CHAR 和VARCHAR 类型

CHAR 和VARCHAR 很类似，都用来保存MySQL 中较短的字符串。二者的主要区别在于存储方式的不同：CHAR 列的长度固定为创建表时声明的长度，长度可以为从0～255 的任何值；而VARCHAR 列中的值为可变长字符串，长度可以指定为0～255（5.0.3 以前）或者65535（5.0.3以后）之间的值。在检索的时候，CHAR 列删除了尾部的空格，而VARCHAR 则保留这些空格。

```sql
create table vc (
    'v' varchar(4),
    'c' char(4)
);

insert into vc values ('ab  ', 'ab  ');

select length(v), length(c) from vc;

select concat(v, '+'), concat(c, '+') from vc;
```



### BINARY 和VARBINARY 类型

BINARY 和VARBINARY 类似于CHAR 和VARCHAR，不同的是它们包含二进制字符串而不包含非二进制字符串。

```sql
create table t10 (
    c binary(3)
);

-- 当保存BINARY 值时，在值的最后通过填充“0x00”（零字节）以达到指定的字段定义长度。
insert into t10 set c='a';

select *, hex(c), c='a', c='a\0', c='a\0\0' from t10;
```



### ENUM 类型

ENUM 中文名称叫枚举类型，它的值范围需要在创建表时通过枚举方式显式指定，对1～255 个成员的枚举需要1 个字节存储；对于255～65535 个成员，需要2 个字节存储。最多允许有65535 个成员。

```sql
create table t (
    gender enum('M', 'F')
);

insert into t values ('M'), ('1'), ('f'), (null);

-- ENUM 类型是忽略大小写的，对'M'、'f'在存储的时候将它们都转成了大写，还可以看出对于插入不在ENUM 指定范围内的值时，并没有返回警告，而是插入了enum('M','F')的第一值'M'
select * from t;
```



### SET类型

Set 和ENUM 类型非常类似，也是一个字符串对象，里面可以包含0～64 个成员。

- 1～8 成员的集合，占1 个字节。
- 9～16 成员的集合，占2 个字节。
- ...
- 33～64 成员的集合，占8 个字节。

Set 和ENUM 除了存储之外，最主要的区别在于

- Set 类型一次可以选取多个成员
- 而ENUM则只能选一个。

```sql
create table t (
    col set ('a', 'b', 'c', 'd')
);

insert into values 
('a, b'),
('a, d, a'),
('a, b'),
('a, c'),
('a');

-- 选择一个或多个
-- 超出范围不写入
-- 重复成员去重
select * from t;
```















