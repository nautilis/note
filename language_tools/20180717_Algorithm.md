#### HashMap
- 原理：通过一个指针数组存(Key,Value)节点对象，对Key进行hash计算出结果即为指针数组的下标。不同的Key可能进行hash计算出相同的下标（哈希冲突),解决哈希冲突的方法有线性探索发和拉链表法。线性探索在hash冲突产生后hash结果不断加一向前寻找没有使用的数组位置。拉链表法，每个数组位置存一条存放(key,value)对象的单向链表，hash冲突产生时将新节点插入到链表中。
- Java实现(拉链表法）
```java
class Node<K, V>{
    public Node next;
    public K key;
    public V value;

    public Node(K key, V value){
        this.key = key;
        this.value = value;
    }
}
public class MyMap<K,V>{
    private int size;
    private int numBuckets; //指针数组的长度
    private ArrayList<Node<K,V>> bucketArray; //指针数组

    public MyMap(){
        size = 0;
        numBuckets = 10;
        bucketArray = new ArrayList<>();
        int i;

        //初始化指针数组的每个元素为一个空链
        for(i=0;i<numBuckets;i++){
            bucketArray.add(null);
        }
    }

    public int size(){
        return this.size;
    }

    public boolean isEmpty(){
        return this.size <= 0;
    }

    /**
     * 对key做hash运算，返回index为指针数组下标
     * @param key
     * @return
     */
    private int getBucketIndex(K key){
        int hashcode = key.hashCode();
        int index = hashcode % this.numBuckets;
        if(index < 0) //会有负数的现象
            return -index;
        return index;
    }

    public V remove(K key){
        int index = getBucketIndex(key); //找到key所在指针数组的下标
        Node<K,V> head = bucketArray.get(index); //获取下标中链表的头部节点
        if(head == null)
            return null;

        Node<K,V> pre = null;
        while(head != null){ //从头部节点开始遍历链表 直到找到对应的key
            if(head.key.equals(key))
                break;
            pre = head;
            head = head.next;
        }

        if(head == null){ //说明链表遍历完毕仍没有找到
            return null;
        }

        size--;
        if(pre != null){ pre.next = head.next; //head即为要找到node, 前一个节点的下个节点指向head的下个节点
        }else{ // 第一个节点就是要找的节点, 直接设置index 为头部节点的下个节点
            bucketArray.set(index, head.next);
        }
        return head.value;
    }

    public V get(K key){
        int index = getBucketIndex(key);
        Node<K,V> head = bucketArray.get(index);
        while(head != null){ //遍历链表 比较每个节点的key直到找到key相同的返回value
            if(head.key.equals(key)){
                return head.value;
            }
        }
        return null;
    }

    public void add(K key, V value){
        int index = getBucketIndex(key);
        Node<K, V> head = bucketArray.get(index);

        while(head != null){
            if(head.key.equals(key)){ //从头部开始遍历链表，如果找到key相同的节点 直接跟新其value
                head.value = value;
                return;
            }
            head = head.next;
        }

        head = bucketArray.get(index); //节点尚不存在 head恢复为 链表的第一个节点
        size++;
        Node<K,V> newNode = new Node<>(key, value);//创建新节点
        newNode.next = head; //新节点的下个节点有头部节点
        bucketArray.set(index, newNode); //设置新节点为头部节点

        //扩大指针数组的容量
        if((1.0*size)/numBuckets > 0.7){
            ArrayList<Node<K,V>> temp = bucketArray; //暂存数组
            bucketArray = new ArrayList<Node<K,V>>(); //新建指针数组
            numBuckets = 2 * numBuckets;
            size=0;
            for(int i=0;i< numBuckets;i++){ //初始化到翻倍的大小
                bucketArray.add(null);
            }
            for(Node<K,V> node : temp){ //对之前数组进行重新加入, numBuckets 改变了hash结果也变了
                add(node.key, node.value);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(-9 % 4);
        MyMap<String, Integer> map = new MyMap<>();
        map.add("hello", 1);
        map.add("what", 4);
        map.add("hahaha", 10);
        System.out.println(map.get("what"));
        System.out.println(map.size());
        System.out.println(map.remove("what"));
        System.out.println(map.size());

    }
}
```
- C实现
```C
#define _XOPEN_SOURCE 500

#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <string.h>

struct entry_s
{
	char *key;
	char *value;
	struct entry_s *next;
};


typedef struct entry_s entry_t;

struct hashtable_s
{
	int size;
	struct entry_s **table;
};

typedef struct hashtable_s hashtable_t;

hashtable_t *
ht_create(int size)
{

	hashtable_t *hashtable = NULL;
	int i;

	if(size < 1) return NULL;

	if((hashtable = malloc(sizeof(hashtable_t))) == NULL) {
		return NULL;
	}

	if((hashtable->table = malloc(sizeof(entry_t *) * size)) == NULL){ // topizza why * size
		return NULL;
	}

	for(i=0;i<size;i++){
		hashtable->table[i] = NULL;
	}

	hashtable->size = size;
	
	return hashtable;
}

int 
ht_hash(hashtable_t *hashtable, char *key)
{
	unsigned long int hashval;

	int i = 0;
	while(hashval < ULONG_MAX && i < strlen(key)){
		hashval = hashval << 8;
		hashval += key[i];
		i++;
	}

	return hashval % hashtable->size;
}

entry_t *
ht_newpair(char *key, char *value)
{
	entry_t *newpair;

	if( ( newpair = malloc( sizeof( entry_t ) ) ) == NULL ){
		return NULL;
	}

	if( ( newpair->key = strdup( key )) == NULL ){
		return NULL;
	}

	if( ( newpair-> value = strdup( value )) == NULL ){
		return NULL;
	}

	newpair->next = NULL;

	return newpair;
}

void 
ht_set( hashtable_t *hashtable, char *key, char *value )
{
	int bin = 0;
	entry_t *newpair = NULL;
	entry_t *next = NULL;
	entry_t *last = NULL;

	bin = ht_hash(hashtable, key);
	
	next = hashtable->table[bin];

	while(next != NULL && next->key != NULL && strcmp(key, next->key) > 0){
		last = next;
		next = next->next;
	}

    if(next != NULL && next->key != NULL && strcmp(key, next->key) == 0){
		free(next->value);
		next->value = strdup(value);
	}else{
		newpair = ht_newpair(key, value);
		
		if(next == hashtable->table[bin]){
			newpair->next = next;
			hashtable->table[bin] = newpair;
		}else if(next == NULL){
			last->next = newpair;
		}else{
			newpair->next = next;
			last->next = newpair;
		}
	}
}

char *
ht_get(hashtable_t *hashtable, char *key)
{
	int bin = 0;

	entry_t *pair;

	bin = ht_hash(hashtable, key);

	pair = hashtable->table[bin];

	while(pair != NULL && pair->key != NULL && strcmp(key, pair->key) > 0){
		pair = pair->next;
	}

	if(pair == NULL || pair->key == NULL || strcmp(key, pair->key) != 0){
		return NULL;
	}else{
		return pair->value;
	}
}

int
main()
{
	hashtable_t *hashtable = ht_create( 65536 );

	ht_set( hashtable, "key1", "inky" );
	//ht_set( hashtable, "key2", "pinky" );
	//ht_set( hashtable, "key3", "blinky" );


    printf(  "%s\n", ht_get( hashtable, "key1"));
	//printf(  "%s\n", ht_get( hashtable, "key2"));

	return 0;
}

```
