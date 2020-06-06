# MySQL_03_运算符

## 算术运算符

| 运算符  |      作用      |
| :-----: | :------------: |
|    +    |      加法      |
|    -    |      减法      |
|    *    |      乘法      |
| /,  DIV |  除法，返回商  |
| %,  MOD | 除法，返回余数 |

```sql
select 0.1 + 0.333, 0.1 - 0.333333, 0.1*.8, 1/2, 1%2;

select 3%2, mod(3, 2);
```



## 比较运算符

```sql
-- 结果为True返回1， 结果为False返回0
```

|    运算符     |            作用             |
| :-----------: | :-------------------------: |
|       =       |            等于             |
|    <>或!=     |           不等于            |
|      <=>      | NULL安全的等于（NULL-safe） |
|       <       |            小于             |
|      <=       |          小于等于           |
|       >       |            大于             |
|      >=       |          大于等于           |
|    BETWEEN    |       存在于指定范围        |
|      IN       |       存在于指定集合        |
|    IS NULL    |           为NULL            |
|  IS NOT NULL  |          不为NULL           |
|     LIKE      |         通配符匹配          |
| REGEXP或RLIKE |       正则表达式匹配        |

```sql
-- "=", 两侧操作数相等返回值为1，否则为0
-- NULL 不能用于“=”比较
select 1=0, 1=1, NULL=NULL;


-- "<=>", 于"="相似，但"<=>"可以用来比较NULL
select 1<=>1, 2<=>2, null<=>null;

-- a BETWEEN min AND max
select 10 between 10 and 20, 9 between 10 and 20;

-- a IN (value1, value2, ...)
select 1 in (1, 2, 3), 't' in ('t', 'a', 'b', 'l', 'e'), 0 in (1, 2);

-- a IS NULL
select 0 is null, null is null;

-- a LIKE %123%
select 123456 like '123%',123456 like '%123%',123456 like '%321%';

-- str REGEXP str_pat
select 'abcdef' regexp 'ab', 'abcdef' regexp 'k';
```



## 逻辑运算符

逻辑运算符又称为布尔运算符，用来确认表达式的真和假。

|  运算符  |   作用   |
| :------: | :------: |
| NOT 或！ |  逻辑非  |
| AND 或&& |  逻辑与  |
| OR或\|\| |  逻辑或  |
|   XOR    | 逻辑异或 |

```sql
-- NOT: NOT NULL 的返回值为NULL
select not 0, not 1, not null;

-- AND: 操作数中有任何一个为NULL 则返回值为NULL
select (1 and 1), (0 and 1), (1 and null);

-- OR: 当两个操作数均为非NULL 值时，如有任意一个操作数为非零值，则结果为1，否则结果为0。当有一个操作数为NULL 时，如另一个操作数为非零值，则结果为1，否则结果为NULL。
select (1 or 0), (0 or null), (1 or null), (null or null);

-- “XOR”表示逻辑异或。当任意一个操作数为NULL 时，返回值为NULL。对于非NULL 的操作数，如果两个的逻辑真假值相异，则返回结果1；否则返回0。
select 1 xor 1, 0 xor 0, 1 xor 0, null xor null;
```



## 位运算符

| 运算符 |      作用       |
| :----: | :-------------: |
|   &    |  位与（位AND）  |
|   \|   | 位或 （位OR ）  |
|   ^    | 位异或（位XOR） |
|   ~    |     位取反      |
|  \>>   |     位右移      |
|   <<   |     位左移      |



## 运算符优先级

优先级由低到高排列，同一行中的运算符具有相同的优先级。

| 优先级顺序 |                          运算符                          |
| :--------: | :------------------------------------------------------: |
|     1      |                            :=                            |
|     2      |                     \|\|,  OR,  XOR                      |
|     3      |                         &&,  AND                         |
|     4      |                           NOT                            |
|     5      |           BETWEEN,  CASE,  WHEN,  THEN,  ELSE            |
|     6      | =,  <=>,  >=,  >,  <=,  <,  !=,  IS,  LIKE,  REGEXP,  IN |
|     7      |                            \|                            |
|     8      |                            &                             |
|     9      |                         <<,  >>                          |
|     10     |                          -,  +                           |
|     11     |                  *,  /,  DIV,  %,  MOD                   |
|     12     |                            ^                             |
|     13     |               -(一元减号), ~(一元比特反转)               |
|     14     |                            !                             |





