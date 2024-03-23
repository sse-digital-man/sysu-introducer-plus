import sys; sys.path.append("./src")

from core.msg_queue.fifo_queue import FIFOQueue

def main():
    queue = FIFOQueue()

    data = [3, 1, 4, 1, 5]

    for n in data:
        queue.push(n)

    while not queue.empty():
        print(queue.pop())

if __name__ == '__main__':
    main()