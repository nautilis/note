##### 索引
- 原理: 使用B-Tree或其他数据结构降低IO
- MySQL 只对以下操作符号使用索引 < , <=, =, >, >=, between, in 以及某些时候的like(不以匹配符%或者_开头的情形),在列上运算会导致索引失效（eg:```Year(addDate) < 2007```)

- 哪些列适合建立索引：where/join子句中常出现的列. 
- 不要过度索引，只保持所需的索引。每个额外的索引都要占用额外的磁盘空间，并降低写操作的性能（需要重建索引)


##### 前缀索引。只对文本的前n个字符建立索引
- 语法
```SQL
ALTER TABLE table_name ADD KEY(column_name(prefix_length));
```
- 长度的选择,尽量接近***索引选择性***(不重复条目与总条目的比值)
```SQL
SELECT 1.0*COUNT(DISTINCT column_name)/COUNT(*); --索引选择性
SELECT 1.0*COUNT(DISTINCT LEFT(column_name, n))/COUNT(*); --改变n的值试探出最优结果
```
- 弊端：MySQL 不能在 ORDER BY 或 GROUP BY 中使用前缀索引，也不能把它们用作覆盖索引(Covering Index)。
##### 索引类型
###### 单列
- 普通索引: 无任何限制
- 唯一索引: 不允许重复，但可以为NULL
- 主键: 不重复不为NULL
###### 组合
- KEY(多列)  

- ***多个查询条件下组合索引比多个单列索引高效***: 因为虽然多个单列索引但MySQL只能用到它认为似乎最有效的单列索引。

##### 最左匹配原则
- 索引匹配遵循最左匹配原则，所以建立索引时，从左到右应按最常使用的查询条件排序。
- 多列索引查询时只有指定了索引左边的列时才能命中索引。
```SQL
CREATE INDEX name_cid_INX ON student(cid, name);
EXPLANE SELECT * FROM student WHERE name = 'nautilis'; --会用index但是需要\对整改索引文件进行扫描(因为单单name这个索引是无序的)。
EXPLANE SELECCT * FROM student WHERE cid = 1 AND name = 'nautilis'; --命中索引，应该用了组合索引的最左边列做查询条件。
```

##### MySQL 分析
- SHOW命令
- EXPLAIN 分析查询
- PROFILING 分析查询
- 开启慢查询日志
```shell
# my.cnf [mysqld]下加入
slow_query_log = 1 # 0关1开
slow_query_log_file = /usr/local/mysql/data/slow-query.log # 日志文件
```
