# MySQL_04_常用函数

## 字符串函数

|         函数          |                             功能                             |
| :-------------------: | :----------------------------------------------------------: |
|   CANCAT(S1,S2,…Sn)   |                  连接S1,S2,…Sn 为一个字符串                  |
| INSERT(str,x,y,instr) | INSERT(str,x,y,instr) 将字符串str 从第x 位置开始，y 个字符长的子串替换为字符instr |
|      LOWER(str)       |                将字符串str 中所有字符变为小写                |
|      UPPER(str)       |                将字符串str 中所有字符变为大写                |
|     LEFT(str ,x)      |                返回字符串str 最左边的x 个字符                |
|     RIGHT(str,x)      |                返回字符串str 最右边的x 个字符                |
|   LPAD(str,n ,pad)    |   用字符串pad 对str 最左边进行填充，直到长度为n 个字符长度   |
|    RPAD(str,n,pad)    |   用字符串pad 对str 最右边进行填充，直到长度为n 个字符长度   |
|      LTRIM(str)       |                   去掉字符串str 左侧的空格                   |
|      RTRIM(str)       |                   去掉字符串str 行尾的空格                   |
|     REPEAT(str,x)     |                    返回str 重复x 次的结果                    |
|   REPLACE(str,a,b)    |         用字符串b 替换字符串str 中所有出现的字符串a          |
|     STRCMP(s1,s2)     |                      比较字符串s1 和s2                       |
|       TRIM(str)       |                  去掉字符串行尾和行头的空格                  |
|  SUBSTRING(str,x,y)   |          返回从字符串str x 位置起y 个字符长度的字串          |

```sql
-- concat()
select concat('aaa','bbb','ccc') ,concat('aaa',null);

-- insert()
SELECT insert("panky", 4, 2, 'suki');

-- lower(), upper()
SELECT UPPER("panky"), LOWER('NBA CBA');

-- left(), right()
SELECT left('pankyPan', 3), right('pankyPan', 5);
```



## 数值函数

|     函数      |                 功能                 |
| :-----------: | :----------------------------------: |
|    ABS(x)     |            返回x 的绝对值            |
|    CEIL(x)    |        返回大于x 的最大整数值        |
|   FLOOR(x)    |        返回小于x 的最大整数值        |
|   MOD(x，y)   |    返回x/y 的模, 和x%y 的结果相同    |
|    RAND()     |         返回0 到1 内的随机值         |
|  ROUND(x,y)   | 返回参数x 的四舍五入的有y 位小数的值 |
| TRUNCATE(x,y) |    返回数字x 截断为y 位小数的结果    |

```sql
-- abs()
SELECT abs(8.8), abs(-8.8);

-- floor(), ceil()
SELECT floor(-0.8), ceil(-0.8);

-- round(), truncate()
select round(1.235, 2), truncate(1.235, 2);
```



## 日期和时间函数

|               函数                |                     功能                     |
| :-------------------------------: | :------------------------------------------: |
|             CURDATE()             |                 返回当前日期                 |
|             CURTIME()             |                 返回当前时间                 |
|               NOW()               |             返回当前的日期和时间             |
|       UNIX_TIMESTAMP(date)        |          返回日期date 的UNIX 时间戳          |
|           FROM_UNIXTIME           |           返回UNIX 时间戳的日期值            |
|            WEEK(date)             |        返回日期date 为一年中的第几周         |
|            YEAR(date)             |             返回日期date 的年份              |
|            HOUR(time)             |              返回time 的小时值               |
|           MINUTE(time)            |              返回time 的分钟值               |
|          MONTHNAME(date)          |              返回date 的月份名               |
|       DATE_FORMAT(date,fmt)       |      返回按字符串fmt 格式化日期date 值       |
| DATE_ADD(date,INTERVAL expr type) | 返回一个日期或时间值加上一个时间间隔的时间值 |
|       DATEDIFF(expr,expr2)        | 返回起始时间expr 和结束时间expr2 之间的天数  |

```sql
select curtime(), now();
```



## 流程函数

|                           函数                           |                       功能                        |
| :------------------------------------------------------: | :-----------------------------------------------: |
|                      IF(value,t f)                       |         如果value 是真，返回t；否则返回f          |
|                  IFNULL(value1,value2)                   |   如果value1 不为NULL返回value1，否则返回value2   |
|    CASE WHEN [value1] THEN[result1]…ELSE[default]END     |   如果value1 是真，返回result1，否则返回default   |
| CASE [expr] WHEN [value1] THEN[result1]…ELSE[default]END | 如果expr 等于value1，返回result1，否则返回default |

```sql
create table salary (
    userid int,
    salary decimal(9, 2)
);

insert into salary values
(1, 1000),
(2, 2000),
(3, 3000),
(4, 4000),
(5, 5000),
(1, null);

-- if(value, t, f)
select if(salary>2000, 'high', 'low') from salary;

-- ifnull(value1, value2)：这个函数一般用来替换NULL 值的
select ifnull(salary, 0) from salary;

-- CASE WHEN [value1] THEN[result1] ... ELSE[default]END
select case when salary<=2000 then 'low' else 'high' end from salary;

-- CASE [expr] WHEN [value1] THEN [result1] ... ELSE [default] END;
select case salary when 1000 then 'low' when 2000 then 'mid' else 'high' end from salary;

```



### 其他常用函数

|      函数      |             功能              |
| :------------: | :---------------------------: |
|   DATABASE()   |       返回当前数据库名        |
|   VERSION()    |      返回当前数据库版本       |
|     USER()     |      返回当前登录用户名       |
| INET_ATON(IP)  | 返回IP 地址的网络字节序表示。 |
| INET_NTOA(num) | 返回网络字节序代表的IP 地址。 |
| PASSWORD(str)  |   返回字符串str 的加密版本    |
|     MD5()      |    返回字符串str 的MD5 值     |

```sql
select database();

select inet_aton('192.168.1.1');

select inet_ntoa(3232235777);

-- PASSWORD(str)函数：返回字符串str 的加密版本，一个41 位长的字符串。
select password('123');

-- MD5(str)函数：返回字符串str 的MD5 值，常用来对应用中的数据进行加密。
select md5('1234');
```





### 判断表或字段是否存在

```sql
-- 判断表是否存在
SELECT table_name FROM information_schema.TABLES WHERE table_name ='表名';
-- eg
SELECT table_name FROM information_schema.TABLES WHERE table_name='t_iov_vehicle_owner_info'；
```



```sql
-- 判断字段是否存在表中
select count(*) from information_schema.columns where table_name = '表名' and column_name = '字段名';
-- eg
SELECT COUNT(*) FROM information_schema.columns
WHERE TABLE_NAME='country'
AND COLUMN_NAME='country_id';
```



