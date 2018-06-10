### Java VS Python
- java: ```i++```. Python: ```i +=1```
- 三元操作符号 
```java 
int smaller = x < y ? x : y //java
```
```python
smaller = x if x < y else y #python
``` 
- 逻辑真假 Java 小写```true; false``` python 大写```True False```
- ```else``` python可以在while和for循环使用else, java不行。

### Python
- range() & xrange() range返回列表，xrange返回迭代器对象,不会在内存中创建列表的完整拷贝。
- 列表解析。 
```python 
x = map(lambda x : x**2, range(6)) # map(function, iterable, ...)
```
```python 
z = [x**2 for x in range(6)]
# [expr for iter_var in iterable if cond_expr]
```

