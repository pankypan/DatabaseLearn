# Mysql_09_视图

## 视图定义

**View（视图）**

1. 一种虚拟存在的表，对于使用视图的用户来说基本上是透明的
2. 视图并不在数据库中实际存在，行和列数据来自定义视图的查询中使用的表，并且是在使用视图时动态生成的。

**视图相对于普通的表的优势:**

- 简单

  ```sql
  -- 使用视图的用户完全不需要关心后面对应的表的结构、关联条件和筛选条件，对用户来说已经是过滤好的复合条件的结果集。
  ```

- 安全

  ```sql
  -- 使用视图的用户只能访问他们被允许查询的结果集，对表的权限管理并不能限制到某个行某个列，但是通过视图就可以简单的实现。
  ```

- 数据独立

  ```sql
  -- 一旦视图的结构确定了，可以屏蔽表结构变化对用户的影响，源表增加列对视图没有影响；源表修改列名，则可以通过修改视图来解决，不会造成对访问者的影响。
  ```



## 视图操作

### 创建或者修改

**创建视图**

- 需要有`CREATE VIEW` 的权限
- 对于查询涉及的列有`SELECT` 权限

```SQL
CREATE [OR REPLACE] [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]
VIEW view_name [(column_list)]
AS select_statement
[WITH [CASCADED | LOCAL] CHECK OPTION]

-- eg
create view staff_list_view as select s.staff_id, s.first_name, s.last_name, a.address
from staff as s, address as a
where s.address_id = a.address_id;
```



**修改视图**

- `CREATE` `REPLACE` 或者 `ALTER`

```sql
ALTER [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]
VIEW view_name [(column_list)]
AS select_statement
[WITH [CASCADED | LOCAL] CHECK OPTION]
```

<mark>MySQL 视图的定义有一些限制，例如，在FROM 关键字后面不能包含子查询，这和其他数据库是不同的，如果视图是从其他数据库迁移过来的，那么可能需要因此做一些改动，可以将子查询的内容先定义成一个视图，然后对该视图再创建视图就可以实现类似的功能了。</mark>



**视图的可更新性和视图中查询的定义有关系，以下类型的视图是不可更新的:**

- 包含以下关键字的SQL 语句：聚合函数（SUM、MIN、MAX、COUNT 等）、DISTINCT、GROUP BY、HAVING、UNION 或者UNION ALL。
- 常量视图
- SELECT中包含子查询
- JOIN
- FROM一个不能更新的视图
- WHERE字句的子查询引用了FROM 字句中的表。



### 删除

```sql
DROP VIEW [IF EXISTS] view_name [, view_name] ...[RESTRICT | CASCADE]

-- eg
drop view staff_list;
```



### 查看



```sql
-- 从MySQL 5.1 版本开始，使用SHOW TABLES命令的时候不仅显示表的名字，同时也会显示视图的名字
SHOW TABLES


-- SHOW TABLE STATUS
SHOW TABLE STATUS [FROM db_name] [LIKE 'pattern']
-- eg
show table status like 'staff_list' \G;


-- 查询某个视图的定义
SHOW CREATE VIEW view_name \G;
-- eg
show create view staff_list \G;


-- 通过查看系统表information_schema.views 也可以查看视图的相关信息
SELECT * FROM information_schema.views where table_name = 'staff_list' \G;
```

























