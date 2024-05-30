import builtins
import signal

def tabulate(x, min_size=10):
    x_str = str(x)
    to_append = min_size - len(x_str)
    return x_str + " "*to_append

def truncate(x, size=10, spaces = 2):
    x_str = str(x)
    if len(x_str) > size:
        return x_str[:size-1] + "…" + " "*spaces

    to_append = size - len(x_str) + spaces
    return x_str + " "*to_append

_term_colors = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']
def color(txt = None, c = 'white'):
    if isinstance(c, str):
        color = c.lower().strip()
        if color in _term_colors:
            if txt:
                return f"\33[3{_term_colors.index(color)}m{str(txt)}\033[39m"
            else:
                return f"\33[3{_term_colors.index(color)}m"
    print_color(f"Warning: Using invalid terminal color '{c}'", 'red')
    return txt

def bright(txt = None):
    if txt:
        return f"\33[1m{str(txt)}\033[22m"
    else:
        return "\33[1m"

separator = bright("\n================================")
bp = bright(color("• ", 'yellow'))

def darker(txt = None):
    if txt:
        return f"\33[2m{str(txt)}\033[22m"
    else:
        return "\33[2m"

def italics(txt = None):
    if txt:
        return f"\33[3m{str(txt)}\33[23m"
    else:
        return "\33[m"

def underline(txt = None):
    if txt:
        return f"\33[4m{str(txt)}\33[24m"
    else:
        return "\33[4m"

def blink(txt = None):
    if txt:
        return f"\33[5m{str(txt)}\33[25m"
    else:
        return "\33[5m"

def clear():
    return "\033[K"

def default():
    return "\33[0m"

def print_status(txt):
    print(blink("\n"+str(txt)+"\033[F\033[K"), end='')

_py_print = print
_status = ''
def _status_print(*args, **kwargs):
    _py_print(*args, clear(), **kwargs)
    _py_print("\n"+blink(_status)+"\033[K\033[F\033[K", end='\r')

def set_status(txt):
    global _status
    _status = txt
    print(end='')

def get_status():
    return _status

def status_start():
    builtins.print = _status_print 
    print("\033[?25l", end='') #hides cursor

def status_stop():
    builtins.print = _py_print
    print("\033[E\033[K\033[F\033[?25h", end='')

_py_sigint_handler = signal.getsignal(signal.SIGINT)
def disable_interrupt(): #doesn't seme to work as expected
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def enable_interrupt():
    signal.signal(signal.SIGINT, _py_sigint_handler)