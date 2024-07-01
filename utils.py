import builtins

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

def round_down(f, digits=0):
    return float(str(f)[:str(f).index('.')+digits+1])

def char_after_digits(s): #used for handling ECL sub names
    has_number = False
    for char in s:
        if char.isdigit():
            has_number = True
        elif has_number:
            return True
    return False

_std_term_colors = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']
_custom_term_colors = {'orange':209}
def color(txt = None, c = 'white'):
    if isinstance(c, str):
        color_name = c.lower().strip()
        ansi_code = None

        if color_name in _std_term_colors:
            ansi_code = f"\33[3{_std_term_colors.index(color_name)}m"
        elif color_name in _custom_term_colors:
            ansi_code = f"\33[38:5:{_custom_term_colors[color_name]}m"

        if ansi_code:
            return ansi_code + ((str(txt) + "\033[39m") if txt else "")

    print(color("Warning:", 'red'), f"Using invalid terminal color '{c}'.")
    return txt

def bright(txt = None):
    if txt:
        return f"\33[1m{str(txt)}\033[22m"
    else:
        return "\33[1m"

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

separator = bright("\n================================") + clear()
bp = bright(color("•", 'yellow'))
sub_bp = darker('└─') + bp

def print_status(txt):
    print(blink("\n"+str(txt)+"\033[F\033[K"), end='')

_py_print = print
_status = ''
def _status_print(*args, **kwargs):
    clear_args = []
    for arg in args:
        clear_args.append(str(arg).replace('\n', '\033[K\n'))

    _py_print(*clear_args, clear(), **kwargs)
    _py_print("\n"+_status+"\033[K\033[F\033[K", end='\r')

def set_status(txt):
    global _status
    _status = blink(txt)
    print(end='')

def get_status():
    return _status

def status_start():
    builtins.print = _status_print 
    print("\033[?25l", end='') #hides cursor

def status_stop():
    builtins.print = _py_print
    print("\033[E\033[K\033[F\033[?25h", end='')