import sys



### shell ###

def clear_screen():
    sys.stdout.write('\033[2J\033[1;1H')
    sys.stdout.flush()


def read_prompt():
    sys.stdout.write('\033[35;1m')
    sys.stdout.write('> ')
    sys.stdout.flush()
    line = sys.stdin.readline()
    sys.stdout.write('\033[0m')
    if not line:
        sys.exit(1)
    if len(line) > 1024:
        sys.exit(1)
    return line.strip()


def read_number():
    n = False
    while not n:
        s = read_prompt()
        try:
            n = int(s) # Kann einen Fehler ergeben
        except:
            print("Not a number")
    return n


def hit_enter():
    sys.stdout.write('\033[35;1m')
    sys.stdout.write('\n[hit enter to continue]\n> ')
    sys.stdout.flush()
    sys.stdin.readline()
    sys.stdout.write('\033[0m')



### general ###

def invert_dict(d):
    return dict([(v, k) for k, v in d.items()])
