# coding=utf-8
# 手写pascal扫描器的有穷自动机，与NFA不同的是，它能记住每个终态是什么，此时对应的token是什么
from itertools import chain

keywords = ['int', 'string']
alphaLowers = [chr(i) for i in range(ord('a'), ord('z') + 1)]
alphaUppers = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
numberChars = [chr(i) for i in range(ord('0'), ord('9') + 1)]

startSwitch = [
             (' \t\n\r', None),
             ('[', 'got_lbrac'),
             (']', 'got_rbrac'),
             (',', 'got_comma'),
             ('(', 'saw_lparen'),
             ('.', 'saw_dot'),
             ('<', 'saw_lthan'),
             (list(chain(alphaLowers, alphaUppers)), 'in_ident'),
             (numberChars, 'in_int')
             ]

class OutPara(object):
    def __init__(self, val):
        self.val = val

def case_scanner(statement, outIndex):
    state = 'start'
    currentToken = []
    while 1:
        input_char = statement[outIndex.val]
        if state == 'start':
            currentToken = []
            error = True
            for item in startSwitch:
                if input_char in list(item[0]):
                    if item[1]: state = item[1]
                    error = False
                    break
            if error:raise 'error'
        elif state == 'saw_lparen':
            if input_char == '*':state = 'in_comment'
            else: return 'lparen'
        elif state == 'in_comment':
            if input_char == '*':state = 'leaving_comment'
            else: pass
        elif state == 'leaving_comment':
            if input_char == ')':state = 'start'
            else: state = 'in_comment'
        elif state == 'saw_dot':
            if input_char == '.':state = 'got_dotdot'
            else: return 'dot'
        elif state == 'saw_lthan':
            if input_char == '=':state = 'got_le'
            else: return 'lt'
        elif state == 'in_ident':
            if input_char in chain(alphaLowers, alphaUppers, numberChars, '_'):pass
            else:
                token = ''.join(currentToken)
                if token in keywords: return ('keyword', token)
                else: return ('id', token)
        elif state == 'in_int':
            if input_char in numberChars:pass
            elif input_char == '.':state = 'saw_real_dot'
            elif input_char in chain(alphaLowers, alphaUppers, '_'):raise 'error'
            else:return ('intconst', ''.join(currentToken))
        elif state == 'saw_real_dot':
            if input_char in numberChars:pass
            elif input_char in chain(alphaLowers, alphaUppers, '_'):raise 'error'
            else:return ('real_dot', ''.join(currentToken))
        elif state == 'got_lbrac':return 'lbrac'
        elif state == 'got_rbrac':return 'rbrac'
        elif state == 'got_comma':return 'comma'
        elif state == 'got_dotdot':return 'dotdot'
        elif state == 'got_le':return 'le'

        currentToken.append(input_char)
        outIndex.val += 1
        if outIndex.val == len(statement):break

def case_scanner_work(statement):
    outIndex = OutPara(0)
    symbols = []
    while outIndex.val != len(statement):
        symbols.append(case_scanner(statement, outIndex))
    return symbols


if __name__ == '__main__':
    statement = "123 [first] < 12.3 int (32 string a..b "
    print case_scanner_work(statement)



