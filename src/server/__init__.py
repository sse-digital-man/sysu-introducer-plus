from module.interface.manager import manager
from ws import WSServer

ws_server = WSServer()

manager.load_modules()
manager.set_log_callback(lambda log: ws_server.send(log.to_json()))