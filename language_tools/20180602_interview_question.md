### 1.Collection
##### 1.1HashMap与Hashtable有何区别?
- HashMap的键值均可为null，而Hashtable不允许键或值为null。
- HashTable 是 同步的，HashMap不是同步的。Java5以上可使用扩展性更好的ConcurrentHashMap
- HashMap可以过度到子类LinkedHashMap 从而能实现有序迭代，而HashTable的顺序无法预测。
- HashMap是fail-fast迭代器，而HashTable不是fail-fast迭代器。
```java
//让HashMap 同步
Map m = Collections.synchronizedMap(hashMap);
```
##### 1.2
### 2.基本知识
##### 2.1 “a==b” 与 a.equals(b)
- equals 用于定义类的逻辑比较; == 比较两个类的引用（内存地址)
##### 2.2 equals 与 hashcode()
- 根据 Java 规范，两个使用 equal() 方法来判断相等的对象，必须具有相同的 hash code。


