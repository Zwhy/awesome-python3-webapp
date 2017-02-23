__author__='Zwhy'

'''
web application骨架
'''
import logging;
#设置日志等级，默认为WARNING,只有指定级别或者更高级的才会被追踪记录
#logging的作用就是输出一些信息，比如下面的server started at http://127.0.0.1:9000...
#python3 app.py之后可以在命令行重看到这条信息，logging输出的信息可以帮助我们理解程序执行的流程，对后期除错也非常有帮助
#logging.basicConfig配置需要输出的信息等级，INFO指的是普通信息，INFO以及INFO以上的比如说WARNING警告信息也会被输出
logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

#定义处理http访问请求的方法
def index(request):
    #必须用content_type，不然打开返回文件是".*"。没有扩展名，浏览器没法正常解读。
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html', charset='UTF-8')
#初始化
@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)#创建web应用
    app.router.add_route('GET','/',index)#将浏览器通过GET方式传过来的对根目录的请求转发给index函数处理。
    #调用子协程，创建一个TCP服务器，绑定到“127.0.0.1：9000” socket。并返回一个服务器对象。
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop() #loop是一个消息循环对象
loop.run_until_complete(init(loop)) #在消息循环重复执行协程
loop.run_forever()
