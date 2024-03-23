import sys; sys.path.append("./src")

from server import app

if __name__ == '__main__':
    app.run("0.0.0.0", 20247, debug=True)
    