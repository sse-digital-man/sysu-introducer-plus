from http.cookies import SimpleCookie
from aiohttp import ClientSession

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
        self.session = self.__init_session()
        self.client = BLiveClient(CrawlerInterface.room_id, session=self.session)
        self.client.set_handler(Handler(receive_callback));
    
    # Notice: 这里需要使用异步的方式进行启动
    async def start(self):
        self.client.start()
        await self.client.join()

    def stop(self):
        self.client.stop()

    @staticmethod
    def __init_session() -> ClientSession:
        # 这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0
        SESSDATA = ''

        cookies = SimpleCookie()
        cookies['SESSDATA'] = SESSDATA
        cookies['SESSDATA']['domain'] = "bilibili.com"

        session = ClientSession()
        session.cookie_jar.update_cookies(cookies)

        return session