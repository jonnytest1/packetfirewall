from queue import Queue
import select
import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _Getch()


def stdin_has_content(timeout: float) -> bool:
    assert timeout >= 0

    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    return bool(rlist)




def input_loop(queue,evt_quque:Queue):
    while True:
        char=getch()
        queue.put(char) 

        if(not evt_quque.empty()):
            evt=evt_quque.get()
            if(evt=="QUIT"):
                return