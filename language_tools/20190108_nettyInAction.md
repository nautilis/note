### 《Netty实战》

##### 第二章
- echo 服务端
> ChannelHandler 处理业务逻辑
```Java
 /**
 * @author: zpf
 * ChannleHandler
 * 1.针对不同类型的事件来调用 ChannelHandler；
 * 2.应用程序通过实现或者扩展 ChannelHandler 来挂钩到事件的生命周期，并且提供自
 * 定义的应用程序逻辑；
 * 3.在架构上，ChannelHandler 有助于保持业务逻辑与网络处理代码的分离。这简化了开
 * 发过程，因为代码必须不断地演化以响应不断变化的需求。
 **/
@ChannelHandler.Sharable /*标志handler可被多个channel安全共享*/
public class EchoServerHandler extends ChannelInboundHandlerAdapter {
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        ByteBuf in = (ByteBuf) msg;
        System.out.println(
                "Server received: " + in.toString(CharsetUtil.UTF_8));
        ctx.write(in); /*接收到的消息写给发送者， 不冲刷出站消息*/
    }
    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) {
        ctx.writeAndFlush(Unpooled.EMPTY_BUFFER) /*将未决消息写给发送者，并关闭该channel*/
                .addListener(ChannelFutureListener.CLOSE);
    }
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx,
                                Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
```
> 引导 ServerBootstrap
```Java

/**
 * @author: zpf
 * 1.绑定到服务器监听的端口
 * 2.配置Channel,将入站消息通知给EchoServerHandler实例
 **/
public class EchoServer {
    private final int port;
    public EchoServer(int port) {
        this.port = port;
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println(
                    "Usage: " + EchoServer.class.getSimpleName() +
                            " <port>");
        }
        int port = Integer.parseInt(args[0]);
        new EchoServer(port).start();
    }
    public void start() throws Exception {
        final EchoServerHandler serverHandler = new EchoServerHandler();
        EventLoopGroup group = new NioEventLoopGroup();
        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(group)
                    .channel(NioServerSocketChannel.class) /*指定所使用的NIO传输Channel*/
                    .localAddress(new InetSocketAddress(port)) /*指定端口套接字地址*/
                    .childHandler(new ChannelInitializer<SocketChannel>(){ /*⑤添加业务handler 到子ChannelHandler的ChannelPipeline*/
                        @Override
                        public void initChannel(SocketChannel ch)
                                throws Exception {
                            ch.pipeline().addLast(serverHandler);
                        }
                    });
            ChannelFuture f = b.bind().sync(); /*绑定服务器，同步阻塞直到完成*/
            f.channel().closeFuture().sync(); /*获取channel的CloseFuture阻塞直到完成*/
        } finally {
            group.shutdownGracefully().sync(); /*关闭EventLoopCroup释放所有资源*/
        }
    }
    /**
     * ⑤ 在 处，你使用了一个特殊的类——ChannelInitializer。这是关键。当一个新的连接
     * 被接受时，一个新的子 Channel 将会被创建，而 ChannelInitializer 将会把一个你的
     * EchoServerHandler 的实例添加到该 Channel 的 ChannelPipeline 中。
     */

}
```

- echo 客户端
> 客户端handler
```Java
/**
 * @author: zpf
 * 1.channelActive()——在到服务器的连接已经建立之后将被调用；
 * 2.channelRead0当从服务器接收到一条消息时被调用
 * 3.exceptionCaught在处理过程中引发异常时被调用。
 **/
@ChannelHandler.Sharable
public class EchoClientHandler extends
        SimpleChannelInboundHandler<ByteBuf> {
    @Override
    public void channelActive(ChannelHandlerContext ctx) {
        ctx.writeAndFlush(Unpooled.copiedBuffer("Netty rocks!",
                CharsetUtil.UTF_8)); /*当被通知channel是活跃时发一条消息*/
    }
    @Override
    public void channelRead0(ChannelHandlerContext ctx, ByteBuf in) {
        System.out.println( 
                "Client received: " + in.toString(CharsetUtil.UTF_8)); /*记录已转收的消息*/
    }
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx,
                                Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
```
> 客户端引导 Bootstrap
```Java
public class EchoClient {
    private final String host;
    private final int port;
    public EchoClient(String host, int port) {
        this.host = host;
        this.port = port;
    }
    public void start() throws Exception {
        EventLoopGroup group = new NioEventLoopGroup();
        try {
            Bootstrap b = new Bootstrap();
            b.group(group) /*指定EventLoopGroup处理客户端事件*/
                    .channel(NioSocketChannel.class)
                    .remoteAddress(new InetSocketAddress(host, port)) /*设置服务端的InetSocketAddress*/
                    .handler(new ChannelInitializer<SocketChannel>() { /*创建Channel时向ChannelPipeline中添加一个EchoClientHandler*/
                        @Override
                        public void initChannel(SocketChannel ch)
                                throws Exception {
                            ch.pipeline().addLast(
                                    new EchoClientHandler());
                        }
                    });
            ChannelFuture f = b.connect().sync();
            f.channel().closeFuture().sync();
        } finally {
            group.shutdownGracefully().sync();
        }
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println(
                    "Usage: " + EchoClient.class.getSimpleName() +
                            " <host> <port>");
            return;
        }
        String host = args[0];
        int port = Integer.parseInt(args[1]);
        new EchoClient(host, port).start();
    }
}
```

##### 第三章 Channel && EventLoop && ChannelFuture
> Channel ---- Socket    
> EventLoop ---- 控制流、多线程处理、并发   
> ChannelFuture ---- 异步通知   

###### Channel
- 基本I/O操作（bind、connect、read、write) 
- 预定义Channel EmbeddedChannel、LocalServerChannel、NioDatagramChannel、NioSctpChannel、NioSocketChannel
###### EventLoop
- 一个 EventLoopGroup 包含一个或者多个 EventLoop；
-  一个 EventLoop 在它的生命周期内只和一个 Thread 绑定；
- 所有由 EventLoop 处理的 I/O 事件都将在它专有的 Thread 上被处理；
- 一个 Channel 在它的生命周期内只注册于一个 EventLoop；
- 一个 EventLoop 可能会被分配给一个或多个 Channel。

