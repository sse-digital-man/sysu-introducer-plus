from enum import Enum

from booter import Booter

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
    while True:
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
        

if __name__ == '__main__':
    main()
        
        
        

        
        
    
    