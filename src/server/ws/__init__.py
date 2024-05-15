from threading import Thread
import asyncio
import websockets

# refs: https://blog.csdn.net/m0_61560439/article/details/130569160


class WSServer:
    def __init__(self, host: str = "0.0.0.0", port: str = "8083"):
        self.__host = host
        self.__port = port

        # 线程运行相关
        self.__thread = Thread(target=self.__handle_connect)
        self.__is_running = False
        self.__delay = 0.01

        # 存储连接的子线程
        self.__clients = set()

        # 消息队列: 暂存发送的消息
        self.__message_queue = []

    def start(self):
        # 如果线程存活 则不能继续使用
        if self.__thread.is_alive():
            return

        self.__is_running = True
        self.__thread.start()

    def stop(self):
        self.__is_running = False

    def send(self, message):
        self.__message_queue.append(message)

    # 处理连接
    def __handle_connect(self):
        # 将客户端连接存储起来
        async def register(websocket):
            self.__clients.add(websocket)

            try:
                await websocket.wait_closed()
            finally:
                self.__clients.remove(websocket)

        # 建立 WebSocket 连接
        async def connect():
            async with websockets.serve(register, self.__host, self.__port):
                await self.__handle_send()

        # 创建线程循环原因
        # https://blog.csdn.net/sinat_41292836/article/details/106567468
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        event_loop.run_until_complete(connect())
        # asyncio.run(connect())

    # 处理发送
    async def __handle_send(self):
        while self.__is_running:
            if len(self.__message_queue) > 0:
                message = self.__message_queue.pop(0)
                websockets.broadcast(self.__clients, message)

            await asyncio.sleep(self.__delay)


# 测试
if __name__ == "__main__":
    server = WSServer()
    server.start()

    while True:
        text = input("> ")

        if text == "stop":
            server.stop()
            break

        server.send(text)
