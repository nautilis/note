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
