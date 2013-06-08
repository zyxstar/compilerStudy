# coding=utf-8
# maybe use expression evaluation in the future
# '-1' is epsilon symbol

transList = []

def concat(startState, symList):
    transList.append((startState, '-1', startState + 1))
    index = 1
    for sym in symList:
        transList.append((startState + index, sym, startState + index + 1))
        index += 1
    transList.append((startState + index, '-1', startState + index + 1))
    return startState + index + 1

def alternation(startState, sym1, sym2):
    transList.append((startState, '-1', startState + 1))
    transList.append((startState + 1, '-1', startState + 2))
    if len(sym1) == 1:
        transList.append((startState + 2, sym1, startState + 3))
        endState1 = startState + 3
    else:
        endState1 = deal(startState + 2, sym1)

    transList.append((startState + 1, '-1', endState1 + 1))
    if len(sym2) == 1:
        transList.append((endState1 + 1, sym2, endState1 + 2))
        endState2 = endState1 + 2
    else:
        endState2 = deal(endState1 + 1, sym2)

    transList.append((endState1, '-1', endState2 + 1))
    transList.append((endState2, '-1', endState2 + 1))
    return endState2 + 1

def kleene(startState, sym):
    transList.append((startState, '-1', startState + 1))
    transList.append((startState + 1, '-1', startState + 2))

    if len(sym) == 1:
        transList.append((startState + 2, sym, startState + 3))
        endState = startState + 3
    else:
        endState = deal(startState + 2, sym)

    transList.append((endState, '-1', startState + 2))
    transList.append((endState, '-1', endState + 1))
    transList.append((startState + 1, '-1', endState + 1))
    return endState + 1

def find_rParen(pattern, index):#查找匹配右括号
    """find match ')' """
    leftCnt = 1#左括号计数
    while 1:
        if index >= len(pattern):raise "pattern's parenthesis do not match"
        c = pattern[index]
        if c == '(':
            leftCnt += 1
        elif c == ')':
            leftCnt -= 1
            if leftCnt == 0: return index
        index += 1

def find_nextGroup(pattern, index):
    start = index
    while 1:
        if index == len(pattern):return index
        c = pattern[index]
        if c == '(' or c == '|':
            return index
        elif c == ')':raise "pattern's parenthesis do not match"
        elif c == '*':#对于*,左结合,优先
            if index - start == 1:return index
            else: return index - 1
        index += 1

def find_rOrExp(pattern, index):#查找"或"的右侧表达式
    leftCnt = 0
    while 1:
        if index == len(pattern):return index
        c = pattern[index]
        if c == '(':
            leftCnt += 1
        elif c == ')':
            leftCnt -= 1
        if c == '|' and leftCnt == 0:
            return index
        index += 1

def find_allGroups(pattern):#如果直接存在or表达式,则只分两组,?|??|??? => (?|??)|(???) 利用交换律
    index = 0
    groups = []
    while 1:
        if index == len(pattern):break
        c = pattern[index]
        if c == '(':
            r = find_rParen(pattern, index + 1)
            sym = pattern[index:r + 1]
            if len(sym):
                groups.append(sym)
            index = r + 1
        elif c == ')':raise "pattern's parenthesis do not match"
        elif c == '*':
            groups.append(c)
            index += 1
        elif c == '|':
            s = ''
            for g in groups:
                s += g
            groups = []
            groups.append(s)
            groups.append(c)
            r = find_rOrExp(pattern, index + 1)
            groups.append(pattern[index + 1:r])
            index = r
        else:
            r = find_nextGroup(pattern, index)
            groups.append(pattern[index:r])
            index = r

    if len(groups) == 1 and groups[0][0] == '(':#脱括号
        return find_allGroups(groups[0][1:-1])
    return groups

def is_atom(pattern):
    for s in pattern:
        if s in ('*', '|', '(', ')'):
            return False
    return True

def deal(startState, pattern):
    #如果已是普通字符直接连接
    if is_atom(pattern):
        return concat(startState, pattern)

    stateIndex = startState + 100

    #处理或
    groups = find_allGroups(pattern)
    ret1 = []
    index = 0
    while 1:
        if index == len(groups):break
        sym = groups[index]
        if sym == '|':
            stateIndex += 100
            endState = alternation(stateIndex, ret1.pop(), groups[index + 1])
            ret1.append((stateIndex, endState))
            index += 2
        else:
            ret1.append(sym)
            index += 1

    #处理重复
    ret2 = []
    for sym in ret1:
        if sym == '*':
            stateIndex += 100
            endState = kleene(stateIndex, ret2.pop())
            ret2.append((stateIndex, endState))
        else:
            ret2.append(sym)

    #处理其他普通字符元素
    index = 0
    while 1:
        if index == len(ret2):break
        sym = ret2[index]
        if type(sym) == type(''):
            stateIndex += 100
            if is_atom(sym):
                endState = concat(stateIndex, sym)
            else:
                endState = deal(stateIndex, sym)
            ret2[index] = (stateIndex, endState)
        index += 1

    #将数组中元素首尾相连
    transList.append((startState, '-1', ret2[0][0]))
    index = 1
    while 1:
        if index == len(ret2):break
        transList.append((ret2[index - 1][1], '-1', ret2[index][0]))
        index += 1

    return ret2[index - 1][1]#返回终状态

def accept(pattern, string):
    global transList
    transList = []
    states = []
    dic = {}
    def trans(t):
        start = t[0]
        sym = t[1]
        end = t[2]
        states.append(start)
        states.append(end)
        if dic.has_key(start):
            _dic = dic[start]
            if _dic.has_key(sym):
                _dic[sym].append(end)
            else:
                _dic[sym] = [end, ]
        else:
            dic[start] = {sym:[end, ]}

    import NFA
    NFA.startstates = (0,)
    syms = set(pattern).difference('()*|')
    syms.add('-1')
    NFA.symbols = tuple(syms)
    endState = deal(0, pattern)
    NFA.acceptstates = (endState,)
    for t in transList:
        trans(t)
    NFA.states = set(states)
    NFA.trans = dic
    return NFA.accept(string)




