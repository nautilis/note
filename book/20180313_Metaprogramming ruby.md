
## 问题  
- 对象能否调用同属于一个类的其他对象的私有方法？
- 可否通过导入一个模块创建类方法？
- Rake如何构件Ruby系统?
- 代码块可以控制作用域？
## 第一章  
#### 概念
- 内省  
运行时仍可询问语言构件（类，变量，方法等）,甚至创建新的语言构件。

## 第二章
#### 基础补充
- Ruby中的类方法
```Ruby
#way 1
class Foo
  def self.bar
  	puts 'class method'
  end
end

Foo.bar

#way 2
class Foo
  class << self
    def bar
	  puts 'class method'
	end
  end
end

Foo.bar

#way 3
class Foo; end
def Foo.bar
  puts 'class method'
end

Foo.bar
```
#### 概念
- 打开类：Ruby的class在类不存在时创建类，存在时跟像作用域操作符，把你带到类的上下文打开类并可进行动态修改。
- 打开类有可能覆盖原来的类属性。
```ruby 
[].methods.grep /RE/ #查看数组对象现有方法 
```
- 对象中的实例变量和方法。实例变量存在于对象本身，方法存在于对象自身的类，一个类的对象共享同样的方法，不共享实例变量。
- 类本身也是对象。类是Class的一个实例对象。
- 常量：ruby中任何以大写字符开头的引用都是常量(包括类名，模块名）。ruby使用模块组织常量类似文件系统，可以通过路径访问，可以调用Moudle.nesting查看当前代码所在路径.
```Ruby
Y = 'a root-level constant'
module M
  class C
    X = "Inner constant"
  end
  Y = 'a constant in M'

  Y     # => "a constant in M"
  ::Y   # => "a root-level constant"
  C::X  # => "Inner constant"
end
M::C::X # => "Inner constant"
```
- 命名空间：充当常量容器的模块，防止命名冲突eg:``` Rake::Task```  
- 对象：是一组实例变量外加一个指向其类的引用。对象的方法并不存在对象本身而存在类中。在类中这些方法被称为类的实例方法。
- 类：是一个对象（Class类的一个实例)外加一组实例方法和一个对超类的引用。类有自己的方法如new,这些是Class类的实例方法。 

- **方法执行**  
    ***找到方法:***  
    - 接收者：调用方法所在的对象。  
	- 祖先连: Object -> class -> superclass -> Object -> Kernel -> BasicObject(都是对象) ``` MySubClass.ancestors # 查看祖先链 ``` ***include***插入包含它的类的上方，***prepend***插入下方，一个模块已经出现在祖先链后续include或prepend都会被忽略。   
    ***执行方法*** 
	- self:对用一个方法接收者就成为self, 所有的实例变量都是self的实例变量，所有没明确指定接收者的方法都在self上调用。
	- 私有规则：调用方法的接收者如果不是自己，就必须明确指明接收者，其次，私有方法只能通过隐性的接收调用。
	- 细化（refine):定义一个模块在模块(module)中使用refine, 定义新方法((除了源编程相关方法methods,ancestors等）或重新定义已有方法（包括include和prepend)，在需要使用的地方调用using改模块。 
```Ruby
module StringExtensions
  refine String do
    def reverse
	  "esrever"
	end
  end
end

module StringStuff
  using StringExtensions
  "my_string".reverse # => "esrever"
end
```

## 第三章 方法
#### 基础补充
- Kernel#respond_to?(:method) 用于检测方法是否存在
#### 概念
- 动态方法，```obj.send(:method_name, args) eg: 1.send(:+, 2) #=> 3``` send可以动态调用方法(包括调用private方法)。如果要避免可以使用public_send，不过有时就是为了调用私有方法。
- 动态定义方法：运行时定义方法```Module#define_method() ```
```Ruby
class MyClass
  define_method :my_method do |my_arg|
    my_arg * 3
  end
end

obj = MyClass.new
obj.my_method(2) # => 6
```
- method_missing 方法: 调用不存在的方法时会延祖父链查找方法，如果不存在则执行Object#method_missing(method_name, *args, &blk)默认会触发NoMethodError。通过覆写method_missing方法,可以实现***幽灵方法**。
- 使response_to?感知幽灵方法。通过覆写response_to_missing?(method, include_private = false)。 response_to 执行过程使用了response_to_missing?()   ??
- const_missing: 当引用不存在的常量时，Ruby会把这个常量名作为符号传给Module#const_missing。
- 幽灵方法，如果在覆写method_missing时调用了不存在的方法，会持续调用method_missing 造成死循环，难以被发现。为此只有在必要时才使用幽灵方法，并且不知道如何处理的方法要调用BasicObject#methdo_missing方法(用super)。
- 如果祖父链存在幽灵方法同名方法，那么幽灵方法会被忽略，可以使用BaseObject白板类避免在Object继承过多的方法。
- 动态定义及调用方法与幽灵方法的对比：   
1 幽灵方法存在风险，需要在method_missing中总是调用super，总是重新定义response_to_missing?方法，即使这样还是会带来让人疑惑的Bug。  
2 幽灵的风险根本原因是它不是真正的方法，只是对调用的拦截。而动态方法是普通方法，可以在obj#methods中查找到。  
3 有时还是只能用幽灵方法，比如非常多运行时会调用的不知名方法。
## 第四章 代码块
#### 概念
- 块是可调用对象，这个家族中还有proc和lambda。
- 块基础：
```Ruby
def a_method(a,b)
  a + yield(a,b)
end

a_method(1,2) {|x, y| (x+y) * 3}  # => 10
```
通过Kernel#block_given?查看方法调用是否包含块。
- 闭包，定义一个代码块是它会获得获得环境中的绑定。当块被传入一个方法时，他会带着绑定一起传入。
```Ruby
def my_method
  x = "GoodBye"
  yield("cruel")
end

x = "hello"
my_method{|y| "#{x} #{y} world"} # => "hello cruel world" 局部环境中的x绑定到代码块，看不到方法中定义的x。
```
- 作用域：在java中内部作用域可以看到外部作用域，但Ruby没有这种嵌套式作用域，作用域之间截然分开，一旦进入新作用域原先的绑定会被替换为一组新的绑定。
```Ruby
v1 = 1
class MyClass
  v2 = 2
  local_variables #=> [:v2]
  def my_method
    v3 = 3
	local_variables
  end
  local_variables  # => [:v2]
end

obj = MyClass.new
obj.my_method #=> [:v3]
obj.my_method #=> [:v3]
local_variables # => [:v1, :obj]

```
- 作用域门，在一个在类定义，模块定义，方法定义时关闭前一个作用域，打开一个新作用域。   
- **让变量穿越作用域**   
1.扁平化作用域：用Class.new代替class, 用Moodule#define_method代替def
```Ruby
my_var = "Success" # 顶级作用域
MyClass = Class.new do 
  puts "#{my_var} in the class definition ！"
  define_method :my_method do 
    "#{my_var} in the method"
  end
end

MyClass.new.my_method
```
2.共享作用域名:只在特定一组方法将分享变量，其他方法无法访问。
```Ruby
def define_methods # def定义作用域门防止其他方法访问
  shared = 0
  # 通过扁平作用域在counter和inc方法间共享shared变量
  Kernel.send :define_method, :counter do 
    shared # 这个代码块能绑定当前环境中的shared
  end
  Kernel.send :define_method, :inc do |x|
    shared +=x
  end
end

define_methods

counter  # => 0
inc(4)   
counter  # => 4
```
- **上下文探针** 将代码块传递给instance_eval或instance_exec，使其在对象上下文执行。   
1、BaseObjet#instance_eval  
```Ruby
class MyClass
  attr_accessor :v
  def initialize
    @v = 1
  end
end

obj = MyClass.new
obj.instance_eval do
  self      # =><MyClass:0x3340dc @v=1>
  @v        # => 1
end 

v = 2
obj.instance_eval{ @v = v }
obj.instance_eval { @v }  # => 2 打开并修改类的实例变量@v 
obj.v       # => 2
```
2、BaseObject#instance_exec, 与1不同是instance_exec可以传入参数。
```Ruby
class C
  def initialize
    @x = 1
  end
end

class D
  def twisted_method
    @y = 2
	C.new.instance_exec(@y) {|y| "@x: #{@x}, @y: #{y}}
  end
end

D.new.twisted_method  # => "@x: 1, @y: 2"
```
- 可调用对象：延迟执行可以多次调用代码块 Proc
```Ruby
#way 0
p = proc { |x| x +1 }
p.call(2)

#way 1
inc = Proc.new {|x| x + 1 }
inc.call(2)      # => 3

#way 2
dec = lamdba { |x| x -1 }
dec.class       # => Proc
dec.call(2)

#way 3
p = ->(x) { x +1 }
p.call(2)      # => 3
```
- 方法中接收代码块
```Ruby
def math(a,b) 
  yield(a,b) # 通过yield执行传给它的代码块
end

def do_math(a,b, &operation)
  math(a, b, &operation)
end

do_math(2,3) { |x, y| x * y } # => 6

#& 操作符号接受代码块

```
- **lamdba与Proc**  
1、都是Proc对象，通过Proc#lamdba?检测是不是lamdba  
2、return在lamdba只表示从lamdba中返回，而proc中的return表示从proc定义的作用域返回。
```Ruby
def double(callable_object)
  callable_object.call * 2
end
l = lamdba { return 10 }
double(l)     # => 20

```
```Ruby
def another_double
  p = Proc.new { return 10 } #改方法已经返回
  result = p.call
  return result * 2
end
another_double    # => 10
```
3、lamdba调用时参数不对会直接报错，proc会调整参数（忽略过多的，用nil代替没有的）  

- 方法也是可调用对象
```Ruby
class MyCalss
  def my_method
    1
  end
end

obj = MyClass.new
m = obj.method :my_method
m.call     # => 1
```
- 自由方法，从最初定义它的类或者方法脱离。 获取方式一，通过Method#unbound,二，通过Module#instance_method从模块中脱离一个方法。重新绑定自由方法，UnboundMethod#bind 或通过Module#define_method

## 第五章 类定义
#### 概念
- 类是增强的模块，类定义同样适用于模块定义。
- 当前类：   
1,在程序顶层当前类是Object,这是main对象所属的类。   2,在一个方法中当前类即时当前对象的类。   
3,用class打开类时那个类为当前类。   
- class_eval方法（别名module_eval),在一个已存在类的上下文执行一个块。  
1,与Object#instance_eval不同，instance_eval只修改self,而class_eval修改self和当前类。   
2,与class操作的区别，class只能用于常量，class_eval 可以用于任何代表类的变量。class会打开新作用域从而失去当前绑定，class_eval则使用扁平作用域。
- 单件方法，Ruby允许给单个对象添加一个方法。通过def obj.method_name或Object#define_singleton_method定义。
- 类方法的实质就是单间方法。
- 类宏
```Ruby
class Book
  def initialize(name)
    @title = name
  end

  def title
    @title
  end

  def self.deprecate(old_method, new_method)
    define_method(old_method) do | *args, &block |
      warn "Warning: #{old_method}() is deprecated. Use #{new_method}()."
      send(new_method, *args, &block)
    end
  end

  deprecate :GetTitle, :title
end

b = Book.new("rubbbby")
b.GetTitle  # => "rubbbby"
```
## 第六章 编写代码的代码
#### 概念
- eval执行代码字符串
```Ruby
eval "puts hello world"   # => "hello world"
eval <<-EOF
  puts "hello world"
EOF                      # => "hello world"
```
- Kernel#binding可以创建Binding对象来捕获并带走当前作用域。可以通过eval在Binding对象所携带的作用域执行代码 
```Ruby
class MyClass
  def my_method
    @x = 1
	binding
  end
end
b = MyClass.new.my_method
eval "@x", b  # => 1
```
- TOPLEVEL_BINDING是一个顶级作用域的预定义常量。
