
states = ()
symbols = ()
trans = {}
startstate = None
acceptstates = ()

def accept(string):
    state = startstate
    for c in string:
        if trans[state].has_key(c):
            state = trans[state][c]
        else:return False
    if state in acceptstates:
        return True
    return False



