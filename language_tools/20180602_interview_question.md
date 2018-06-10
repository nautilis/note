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
- 排序算法（冒泡，选择，插入,希尔，归并，快排，堆排）
### 3.Spring
##### 依赖注入
- 依赖注入，是IOC的一个方面，是个通常的概念，它有多种解释。这概念是说你不用创建对象，而只需要描述它如何被创建。你不在代码里直接组装你的组件和服务，但是要在配置文件里描述哪些组件需要哪些服务，之后一个容器（IOC容器）负责把他们组装起来。
- ***构造器依赖注入***:构造器依赖注入通过容器触发一个类的构造器来实现的，该类有一系列参数，每个参数代表一个对其他类的依赖。
- ***Setter方法注入***:Setter方法注入是容器通过调用无参构造器或无参static工厂 方法实例化bean之后，调用该bean的setter方法，即实现了基于setter的依赖注入。
- 你两种依赖方式都可以使用，构造器注入和Setter方法注入。最好的解决方案是用构造器参数***实现强制依赖***，setter方法实现***可选依赖***。
##### Spirng中Bean的生命周期
- Spring容器 从XML 文件中读取bean的定义，并实例化bean。
- Spring根据bean的定义填充所有的属性。
- 如果bean实现了BeanNameAware 接口，Spring 传递bean 的ID 到 setBeanName方法。
- 如果Bean 实现了 BeanFactoryAware 接口， Spring传递beanfactory 给setBeanFactory 方法。
- 如果有任何与bean相关联的BeanPostProcessors，Spring会在postProcesserBeforeInitialization()方法内调用它们。
- 如果bean实现IntializingBean了，调用它的afterPropertySet方法，如果bean声明了初始化方法，调用此初始化方法
- 如果有BeanPostProcessors 和bean 关联，这些bean的postProcessAfterInitialization() 方法将被调用。
- 如果bean实现了 DisposableBean，它将调用destroy()方法。
##### ApplicationContext通常的实现是什么?
- FileSystemXmlApplicationContext ：此容器从一个XML文件中加载beans的定义，XML Bean 配置文件的全路径名必须提供给它的构造函数。
- ClassPathXmlApplicationContext：此容器也从一个XML文件中加载beans的定义，这里，你需要正确设置classpath因为这个容器将在classpath里找bean配置。
- WebXmlApplicationContext：此容器加载一个XML文件，此文件定义了一个WEB应用的所有bean。
### 4.SQL
### 5.Http
- cookie & session
### 6.SpringMVC
##### SpringMVC的工作流程?
- 用户发送请求至前端控制器DispatcherServlet
- DispatcherServlet收到请求调用HandlerMapping处理器映射器。
- 处理器映射器根据请求url找到具体的处理器，生成处理器对象及处理器拦截器(如果有则生成)一并返回给DispatcherServlet。
- DispatcherServlet通过HandlerAdapter处理器适配器调用处理器
- 执行处理器(Controller，也叫后端控制器)。
- Controller执行完成返回ModelAndView
- HandlerAdapter将controller执行结果ModelAndView返回给DispatcherServlet
- DispatcherServlet将ModelAndView传给ViewReslover视图解析器
- ViewReslover解析后返回具体View
- DispatcherServlet对View进行渲染视图（即将模型数据填充至视图中）。
- DispatcherServlet响应用户.



### Java QA
- String s = "a" + "b" + "c" +"d" + "e";创建了几个对象?  
***A***: 只创建了一个。赋值符号右边的"a", "b", "c"...都是常量（？基本类型)对于常量，编译时直接存储其字面值而不是它们的引用。
- String s = a + b + c + d + e, (a,b,c,d,e为常量
