- 查看表结构: 
```sql
select column_name, data_type, character_maximum_length
from INFORMATION_SCHEMA.COLUMNS where table_name = 'a_asset';
```
