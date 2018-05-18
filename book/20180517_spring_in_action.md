### 第一章 
#### bean的加载过程 p45
!["spring-bean-load"](https://raw.githubusercontent.com/changzeyamei/pictures/master/note/spring-bean-load-process.png)
- Spring对bean进行实例化.
- Spring将值和bean的引用注入到bean对应的属性中.
- 如果bean实现了BeanNameAware接口,Spring将bean的ID传递给 setBean-Name()方法;
- 如果bean实现了BeanFactoryAware接口,Spring将调用setBeanFactory()方法,将BeanFactory容器实例传入
- 如果bean实现了ApplicationContextAware接口,Spring将调用setApplicationContext()方法,将bean所在的应用上下文的引用传入进来;
- 如果bean实现了BeanPostProcessor接口,Spring将调用它们的post-ProcessBeforeInitialization()方法;
- 如果bean实现了InitializingBean接口,Spring将调用它们的after-PropertiesSet()方法。类似地,如果bean使用init-method声明了初始化方法,该方法也会被调用;
- 如果bean实现了BeanPostProcessor接口,Spring将调用它们的post-ProcessAfterInitialization()方法;
- 此时,bean已经准备就绪,可以被应用程序使用了,它们将一直驻留在应用上下文中,直到该应用上下文被销毁;
- 如果bean实现了DisposableBean接口,Spring将调用它的destroy()接口方法。同样,如果bean使用destroy-method声明了销毁方法,该方法也会被调用。

#### 常见应用上下文(P44)
- AnnotationConfigApplicationContext:从一个或多个基于Java的配置类中加载Spring应用上下文。(我推荐使用类型安全并且比XML更加强大的JavaConfig p62)
- AnnotationConfigWebApplicationContext:从一个或多个基于Java的配置类中加载Spring Web应用上下文。
- ClassPathXmlApplicationContext:从类路径下的一个或多个XML配置文件中加载上下文定义,把应用上下文的定义文件作为类资源。
- FileSystemXmlapplicationcontext:从文件系统下的一个或多个XML配置文件中加载上下文定义。
- XmlWebApplicationContext:从Web应用下的一个或多个XML配置文件中加载上下文定义。

```java
ApplicationContext context = new 
       ClassPathXmlApplicationContext("knight.xml");
```
### 第二章 装配bean
#### 通过注解自动装配
```java
package autoconfig;

public interface CompactDisc {
    void play();
}
// =========================

package autoconfig;
import org.springframework.stereotype.Component;

@Component//自动给bean id 将类名首字母变小写 显示给类名@Component("")
public class SgtPeppers implements CompactDisc {

    private String title = "Sgt.pepper's Lonely Hearts Club Band";
    private String artist = "The Beatles";
    public void play() {
        System.out.println("playing" + title + " by " + artist );
    }
}
// ========================================

package autoconfig;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan /**
无任何配置自动扫描同个包下的文件,可设置基础包
@ComponentScan(basePackages={"", " "}或者
@ComponentScan(basePackageClasses={A.class,b.class}, A,B
 所在的包将作为基础包，
 */
public class CDPlayerConfig {
}

// ===================================================

package autoconfig;
import static org.junit.Assert.*;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.beans.factory.annotation.Autowired;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes=CDPlayerConfig.class)
public class CDPlayerTest {
    @Autowired// 自动装配了CompactDIsc进来， 可以添加到构造器，setter @Autowired(request=false) 找不到bean时不会报错(注意null校验)
    public CompactDisc cd;

    @Test
    public void cdShouldDoNotBeNull(){
        assertNotNull(cd);
    }
}
```
#### Java代码装配bean
> 尽管在很多场景下通过组件扫描和自动装配实现Spring的自动化配置
> 是更为推荐的方式,但有时候自动化配置的方案行不通,因此需要明
> 确配置Spring。比如说,你想要将第三方库中的组件装配到你的应用
> 中,在这种情况下,是没有办法在它的类上添加@Component和
> @Autowired注解的,因此就不能使用自动化装配的方案了。

> JavaConfig也不应该侵入到业务逻辑代码,通常会将JavaConfig放到单独的包中,使它与其他的应用程序逻辑分离开来
