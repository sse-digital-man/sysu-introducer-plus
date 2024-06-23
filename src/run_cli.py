import sys
from cli import CliApp

sys.path.append("src")


def main():
    app = CliApp()
    app.handle()


if __name__ == "__main__":
    main()
