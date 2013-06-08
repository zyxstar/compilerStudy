
states = ()
symbols = ()
trans = {}
startstates = ()
acceptstates = ()

def e_closure(I): # -1 is epsilon symbol
    alreadyDeals = []
    def _helper(item):
        if item in alreadyDeals: return []
        if not item in trans: return [item, ]
        alreadyDeals.append(item)
        ret = [item, ]
        if trans[item].has_key('-1'):
            for i in trans[item]['-1']:
                ret.extend(_helper(i))
        return ret
    ret = []
    for i in I:
        ret.extend(_helper(i))
    return tuple(sorted(list(set(ret))))

def move(I, symbol):
    ret = []
    for i in I:
        if not i in trans: continue
        if trans[i].has_key(symbol):
            ret.extend(trans[i][symbol])
    return tuple(sorted(list(set(ret))))

def NFA_2_DFA():
    def _isFinal(item):
        for i in item:
            if i in acceptstates:
                return True
        return False

    index = 0
    dealList = [e_closure(startstates), ]
    genDict = {}
    while len(dealList):
        dealItem = dealList[0]
        dealList = dealList[1:]
        if dealItem in genDict:continue
        genDict[dealItem] = {}
        genDict[dealItem]['index'] = index
        genDict[dealItem]['final'] = _isFinal(dealItem)
        index += 1
        for sym in symbols:
            if sym == '-1':continue
            temp = e_closure(move(dealItem, sym))
            dealList.append(temp)
            genDict[dealItem][sym] = temp

    return genDict

def DFA_rename(DFAdict):
    dic = {}
    for v in DFAdict.values():
        dic[v['index']] = {'final':v['final']}
        for _k, _v in v.items():
            if _k == 'index' or _k == 'final':continue
            dic[v['index']][_k] = DFAdict[_v]['index']
    return dic

def DFA_min_descript(DFAdict):
    allStates = []
    allStates.append({'states':sorted([k for k, v in DFAdict.items() if not v['final']]), 'final':False})
    allStates.append({'states':sorted([k for k, v in DFAdict.items() if v['final']]), 'final':False})

    def _isMin():
        for states in allStates:
            if not states['final']:return False
        return True

    def _isInSelf(state, sym, states):
        newState = DFAdict[state][sym]
        if newState in states: return True
        return False

    def _findNoFinalStates():
        for states in allStates:
            if not states['final']:return states
        return None

    def _dealSym(index, states, ret):
        if index >= len(symbols):
            if ret:
                ret['final'] = True
                yield ret
                return
            else:
                return
        sym = symbols[index]
        if sym == '-1':
            for i in _dealSym(index + 1, states, ret): yield i
            return
        first = []
        second = []
        for state in states['states']:
            if _isInSelf(state, sym, states['states']):
                first.append(state)
            else:
                second.append(state)

        if len(first):
            first.sort()
            if len(first) == 1:
                yield {'states':first, 'final':True}
            elif len(first) != len(states['states']):
                yield {'states':first, 'final':False}
            else:
                for i in  _dealSym(index + 1, states, {'states':first, 'final':None}):yield i

        if len(second):
            second.sort()
            if len(second) == 1:
                yield {'states':second, 'final':True}
            elif len(second) != len(states['states']):
                yield {'states':second, 'final':False}
            else:
                for i in _dealSym(index + 1, states, {'states':second, 'final':None}):yield i

    while True:
        if _isMin():break
        states = _findNoFinalStates()
        if not states:break
        allStates.remove(states)

        for item in _dealSym(0, states, None):
            allStates.append(item)

    return allStates

def DFA_min(DFAdict):
    def _change(oldState, newState):
        for k, v in DFAdict.items():
            for _k, _v in v.items():
                if _v == oldState and _k != 'final': DFAdict[k][_k] = newState
        DFAdict.pop(oldState)

    descript = DFA_min_descript(DFAdict)
    for item in descript:
        if len(item['states']) > 1:
            for i in item['states'][1:]:
                _change(i, item['states'][0])

    delStates = []#del can't reach final states
    def _isTransToSelf(key, value):
        if value['final']: return False
        for k, v in value.items():
            if k not in symbols: continue
            if v != key:return False
        return True

    for k, v in DFAdict.items():
        if _isTransToSelf(k, v):
            delStates.append(k)
            DFAdict.pop(k)

    for v in DFAdict.values():
        for _k, _v in v.items():
            if _v in delStates: v.pop(_k)

    return DFAdict

def accept(string):
    dfa = DFA_min(DFA_rename(NFA_2_DFA()))
    import DFA
    DFA.states = tuple(dfa.keys())
    ls = list(symbols)
    ls.remove('-1')
    DFA.symbols = tuple(ls)
    DFA.startstate = 0
    DFA.trans = dfa
    ls = []
    for k, v in dfa.items():
        if v['final']:ls.append(k)
    DFA.acceptstates = tuple(ls)
    return DFA.accept(string)
