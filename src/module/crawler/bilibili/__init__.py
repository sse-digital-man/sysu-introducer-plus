import asyncio

from http.cookies import SimpleCookie
from aiohttp import ClientSession

from ..interface import CrawlerInterface

from .blivedm.blivedm import BaseHandler, BLiveClient
from .blivedm.blivedm.models.web import DanmakuMessage


class Handler(BaseHandler):
    def __init__(self, receive_callback):
        # super().__init__(ignored_unknown_cmd=True)
        self.receive_callback = receive_callback

    def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage):
        self.receive_callback(message.msg)


class BilibiliCrawler(CrawlerInterface):
    def __init__(self):
        super().__init__()

        self.__client: BLiveClient = None
        self.__room_id: int = 0

        self.__loop = None

    def load_config(self):
        info = self._read_config()

        self.__room_id = info["roomId"]

    def __start_client(self):
        async def start_client():
            session = await self.__init_session()
            self.__client = BLiveClient(self.__room_id, session=session)
            # Notice: 不能直接在 __init__ 中初始化 session
            self.__client.set_handler(Handler(self._receive_callback))
            self.__client.start()

            await self.__client.join()
            await session.close()

        self.__loop = asyncio.new_event_loop()
        self.__loop.run_until_complete(start_client())

    @staticmethod
    async def __init_session() -> ClientSession:
        # 这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0
        SESSDATA = ""

        cookies = SimpleCookie()
        cookies["SESSDATA"] = SESSDATA
        cookies["SESSDATA"]["domain"] = "bilibili.com"

        session = ClientSession()
        session.cookie_jar.update_cookies(cookies)

        return session

    def handle_starting(self):
        self._make_thread(self.__start_client)

    def handle_stopping(self):
        # 控制客户端关闭
        self.__client.stop()
