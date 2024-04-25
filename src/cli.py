from enum import Enum

from booter import Booter
from utils.args import args

booter = Booter()

class CommandKind(Enum):
    Start = "start"
    Stop = "stop"
    Exit = "exit"

def check_cmd(text: str) -> CommandKind:
    try:
        return CommandKind(text)
    except:
        return None

def main():
    if args.auto:
        booter.start()

    while True:
        try:
            cmd = check_cmd(input("> "))

            if cmd == None:
                print("unknown command")
                continue

            if cmd is CommandKind.Start:
                booter.start()
            elif cmd is CommandKind.Stop:
                booter.stop()
            elif cmd is CommandKind.Exit:
                return
        except Exception as e:
            print("error: ", repr(e))

if __name__ == '__main__':
    main()
        
        
        

        
        
    
    