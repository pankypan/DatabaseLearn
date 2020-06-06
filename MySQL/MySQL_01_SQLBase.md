# MySQL_01_基础

SQL 是Structure Query Language（结构化查询语言）的缩写

SQL 语句主要可以划分为以下3 个类别

- DDL（Data Definition Languages）语句(create、drop、alter
  等)
- DML（Data Manipulation Language）语句(insert、delete、udpate 和
  select 等)
- DCL（Data Control Language）语句(grant、revoke 等)

## DDL

### 数据库

```sql
-- 创建数据库
CREATE DATABASE dbname;

-- 选择数据库
USE dbname;

-- 查看数据库中的表
show tables;

-- 删除数据库
drop database dbname;
```

### 表

```sql
-- 创建表
CREATE TABLE tablename (column_name_1 column_type_1 constraints，
column_name_2 column_type_2 constraints ， ……column_name_n column_type_n constraints）;

-- 查看表定义
DESC tablename;

-- 查看创建表的SQL 语句
show create table tablename \G;

-- 删除表
DROP TABLE tablename

-- 修改表类型
ALTER TABLE tablename MODIFY [COLUMN] column_definition [FIRST | AFTER col_name]

-- 增加表字段
ALTER TABLE tablename ADD [COLUMN] column_definition [FIRST | AFTER col_name]

-- 删除表字段
ALTER TABLE tablename DROP [COLUMN] col_name

-- 表字段改名
-- 注意：change 和modify 都可以修改表的定义，不同的是change 后面需要写两次列名，不方便。但是change 的优点是可以修改列名称，modify 则不能。
ALTER TABLE tablename CHANGE [COLUMN] old_col_name column_definition
[FIRST|AFTER col_name]

-- 修改字段排列顺序
-- 可选项first|after column_name，这个选项可以用来修改字段在表中的位置
--eg：
alter table emp add birth date after ename;
alter table emp modify age int(3) first;
-- 注意：CHANGE/FIRST|AFTER COLUMN 这些关键字都属于MySQL 在标准SQL 上的扩展，在其他数据库上不一定适用。
                        
-- 表改名
ALTER TABLE tablename RENAME [TO] new_tablename
```





## DML

DML 操作是指对数据库中表记录的操作，主要包括表记录的插入（insert）、更新（update）、删除（delete）和查询（select）

### INSERT

```sql
-- 插入记录
INSERT INTO tablename (field1,field2,……fieldn) VALUES(value1,value2,……valuesn);

-- 一次性插入多条记录
INSERT INTO tablename (field1, field2,……fieldn)
VALUES
(record1_value1, record1_value2,……record1_valuesn),
(record2_value1, record2_value2,……record2_valuesn),
……
(recordn_value1, recordn_value2,……recordn_valuesn)
;
```



### UPDATE

```SQL
-- 更新记录
UPDATE tablename SET field1=value1，field2.=value2，……fieldn=valuen [WHERE CONDITION]

-- 同时更新多个表中数据
-- 注意：多表更新的语法更多地用在了根据一个表的字段，来动态的更新另外一个表的字段
UPDATE t1,t2…tn set t1.field1=expr1,tn.fieldn=exprn [WHERE CONDITION]
```



### DELETE

```SQL
-- 删除记录
DELETE FROM tablename [WHERE CONDITION]

-- 一次删除多个表的数据
DELETE t1,t2…tn FROM t1,t2…tn [WHERE CONDITION]

-- 注意：不管是单表还是多表，不加where 条件将会把表的所有记录删除，所以操作时一定要小心。
```



### SELECT

#### 简单查询

```SQL
-- 查询记录
SELECT * FROM tablename [WHERE CONDITION]

-- 查询不重复的记录
select distinct deptno from emp;

-- 条件查询
select * from emp where deptno=1 and sal<3000;

-- 排序
-- DESC 和ASC 是排序顺序关键字，DESC 表示按照字段进行降序排列，ASC 则表示升序排列
SELECT * FROM tablename [WHERE CONDITION] [ORDER BY field1 [DESC|ASC] ， field2
[DESC|ASC]，……fieldn [DESC|ASC]]
```

```sql
-- 限制
-- 其中offset_start 表示记录的起始偏移量，row_count 表示显示的行数
-- limit 经常和order by 一起配合使用来进行记录的分页显示。
SELECT ……[LIMIT offset_start,row_count]

-- eg
select * from emp order by sal limit 1,3;
```



#### 聚合

```sql
-- 语法
SELECT [field1,field2,……fieldn] fun_name
FROM tablename
[WHERE where_contition]
[GROUP BY field1,field2,……fieldn
[WITH ROLLUP]]
[HAVING where_contition]

-- eg 
select sum(sal),max(sal),min(sal) from emp;
select deptno,count(1) from emp group by deptno having count(1)>1;
```

- `fun_name` 表示要做的聚合操作，也就是聚合函数，常用的有`sum（求和）`、`count(*)（记录数）`、`max（最大值）`、`min（最小值`
- `GROUP BY` 关键字表示要进行分类聚合的字段
- `WITH ROLLUP`是可选语法，表明是否对分类聚合后的结果进行再汇总
- `HAVING` 关键字表示对分类后的结果再进行条件的过滤

```python
# 注意：having 和where 的区别在于having 是对聚合后的结果进行条件的过滤，而where 是在聚合前就对记录进行过滤，如果逻辑允许，我们尽可能用where 先过滤记录，这样因为结果集减小，将对聚合的效率大大提高，最后再根据逻辑看是否用having 进行再过滤。
```



#### 表连接

外连接:

```sql
select ename,deptname from emp left join dept on emp.deptno=dept.deptno;
select ename,deptname from dept right join emp on dept.deptno=emp.deptno;
```

- `left join`左连接：包含所有的左边表中的记录甚至是右边表中没有和它匹配的记录
- `right join`右连接：包含所有的右边表中的记录甚至是左边表中没有和它匹配的记录

内连接：

- `inner join`内连接



#### 子查询

 用于子查询的关键字主要包括in、not in、=、!=、exists、not exists 等

```sql
-- in
select * from emp where deptno in(select deptno from dept);

-- 查询记录数唯一，还可以用=代替in
select * from emp where deptno = (select deptno from dept limit 1);
```



#### 记录联合

将两个表的数据按照一定的查询条件查询出来后，将结果合并到一起显示出来

```sql
-- 语法
SELECT * FROM t1
UNION|UNION ALL
SELECT * FROM t2
……
UNION|UNION ALL
SELECT * FROM tn;
-- UNION 和UNION ALL 的主要区别是UNION ALL 是把结果集直接合并在一起，而UNION 是将UNION ALL 后的结果进行一次DISTINCT，去除重复记录后的结果。
```





## DCL

DCL 语句主要是DBA 用来管理系统中的对象权限时所使用，一般的开发人员很少使用

```sql
-- grant 授权
grant select,insert on sakila.* to 'z1'@'localhost' identified by '123';

-- revoke 回收权限
revoke insert on sakila.* from 'z1'@'localhost';
```





