import sys; sys.path.append("src") 
from server import ws_server, app

def run():
    ws_server.start()
    app.run("0.0.0.0", 8082, debug=False)

if __name__ == '__main__':
    run()