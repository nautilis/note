- 查看表结构: 
```sql
select column_name, data_type, character_maximum_length
from INFORMATION_SCHEMA.COLUMNS where table_name = 'a_asset';
```
- 添加序列
```sql
CREATE SEQUENCE gys.mytable_myid_seq
    INCREMENT 1
    START 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 2;
alter table mytable alter column myid set default nextval('mytable_myid_seq');
```

- update ... limit 和 delete ...limit 
```sql
delete from tbl where ctid = any(array(select ctid from tbl where xxx limit xx));

update tbl set xx=xx where ctid = any(array(select ctid from tbl where xxx limit xx));

```
- 删除重复列 delete using 

```sql
-- PostgreSQL
DELETE
FROM
    test_table a
        USING test_table b
WHERE
    a.id < b.id
    AND a.name = b.name
    AND a.email = b.email;
```
```sql
-- mysql delete join
DELETE t1 FROM test_table t1 
    INNER JOIN
	test_table t2
WHERE t1.id < t2.id AND t1.acolumn = t2.acolumn;
```
