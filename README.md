# Loglog
采用Python2.7开发的日志系统

工作之余偶然看到网上提供的解决方案，顺便加上自己的一些想法来实现一把，不喜勿喷。

系统原理：日志提供接口远程请求的方式，项目用到了redis的队列，先请求过来的log直接存到了redis，之后系统会使用定时任务的方式将存放至队列的log日志依次循
环取出并分批次批量存到数据库中，日志的搜索使用的全文搜索。

知识点：

    redis : controller.py 下logapi和logloop方法

    数据库全文搜索 : 数据库 logger.sql 及 controller.py 下getsearchlist方法操作

安装方式：

    1、项目下载服务器 例 /home/www/html/Loglog

    2、配置文件.env 配置自己的环境信息

    3、启动项目 python run.py 

    4、打开定时任务 crontab , 添加定时任务 http://{ip}:5000/logloop 默认5000端口 

    5、默认管理员账号 admin ：123456 

    6、远程调用接口 http://{ip}:5000/logapi
    
             传参方式 POST  

             传递参数

             uid string

             method string

             route string

             header string

             query string

             date string (Y-m-d)

             time string (H:i:s)

    6、该项目简单布局，适于学习，也可作为拓展的一个思路二次开发完善。
