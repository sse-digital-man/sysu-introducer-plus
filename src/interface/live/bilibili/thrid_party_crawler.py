import asyncio

from http.cookies import SimpleCookie
from aiohttp import ClientSession

from threading import Thread


from ..crawler import CrawlerInterface
from .blivedm import BLiveClient, BaseHandler
from .blivedm.models.web import DanmakuMessage


# Blivedm 的处理对象，配置爬虫的回调函数
class Handler(BaseHandler):
    def __init__(self, receive_callback):
        super().__init__(ignored_unknown_cmd=True)
        self.receive_callback = receive_callback

    def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage):
        self.receive_callback(message.msg)

class ThirdPartyBiliBiliCrawler(CrawlerInterface):
    def __init__(self, receive_callback):
        self.client: BLiveClient = None
        self.session: ClientSession = None

        self.crawler_thread = None

        
        self.receive_callback = receive_callback

    def start(self):
        # 再重新启动时，仍会重新创建线程
        self.crawler_thread = Thread(target=self.__start_client)
        self.crawler_thread.start()


    def stop(self):
        # 由于爬虫程序在 crawler_thread 中运行，所以不能直接在此处停止运行
        ''' Notice: 停止逻辑
            此处并不是调用 client 中 stop 方法，而是 close 方法
            直接将此处会话关闭

            1. 先调用 stop，让以下 start_client 中 join 函数继续运行
            2. 此后就可以调用 close_client 函数处理关闭逻辑

            由于开启和关闭会话都是异步操作，所以需要在 async 函数中运行
        '''
        self.client.stop()
        self.crawler_thread.join()
        
        
    def __start_client(self):

        async def start_client():
            self.session = await ThirdPartyBiliBiliCrawler.__init_session()
            self.client = BLiveClient(CrawlerInterface._room_id, session=self.session)

            # Notice: 不能直接在 __init__ 中初始化 session
            self.client.set_handler(Handler(self.receive_callback))
            self.client.set_room_id(self._room_id)

            self.client.start()
            await self.client.join();
        
        async def close_client():
            await self.session.close()
            await self.client.close()
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        loop.run_until_complete(start_client())
        loop.run_until_complete(close_client())


    @staticmethod
    async def __init_session() -> ClientSession:
        # 这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0
        SESSDATA = ''

        cookies = SimpleCookie()
        cookies['SESSDATA'] = SESSDATA
        cookies['SESSDATA']['domain'] = "bilibili.com"

        session = ClientSession()
        session.cookie_jar.update_cookies(cookies)

        return session
    