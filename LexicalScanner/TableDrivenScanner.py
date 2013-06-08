from itertools import chain

keywords = ['int', 'string']
alphaLowers = [chr(i) for i in range(ord('a'), ord('z') + 1)]
alphaUppers = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
numberChars = [chr(i) for i in range(ord('0'), ord('9') + 1)]


class Action_Rec(object):
    def __init__(self):
        self.action = None
        self.new_state = None
        self.token_found = None

def get_char(ch):
    if ch in chain(alphaLowers, alphaUppers):return 'letter'
    elif ch in numberChars:return 'digit'
    elif ch in ' \t':return 'space'
    elif ch == '\r\n':return 'newline'
    elif ch in '/*()+-:=.': return ch
    else:return 'other'


def tableDriven_scanner(statement):
    state = ["start", "saw_lparen", "in_comment", "leaving_comment", "saw_dot",
             "saw_lthan", "in_ident", "in_int", "saw_real_dot", "got_lbrac",
             "got_rbrac", "got_comma", "got_dotdot", "got_le"]

    token = []
    scan_tab = []# array of Action_Rec
    token_tab = []

    index = 0

    tok = None
    cur_char = None
    remembered_chars = []
    while 1:
        cur_state = "start"
        image = ""
        remembered_state = None
        while 1:
            cur_char = get_char(statement[index])
            key = (cur_char, cur_state)
            action = scan_tab[key].action
            if action == 'move':
                if token_tab[cur_state]:
                    remembered_state = cur_state
                    remembered_chars = []
                remembered_chars.append(statement[index])
                cur_state = scan_tab[key].new_state
            elif action == 'recognize':
                tok = token_tab[cur_state]
                index -= 1
                break
            else:
                if remembered_state != 0:pass


