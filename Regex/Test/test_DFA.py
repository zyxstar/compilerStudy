import unittest
import DFA

DFA.states = ('S', 'U', 'V', 'Q')
DFA.symbols = ('a', 'b')
DFA.trans = {
    'S':{'a':'U', 'b':'V'},
    'U':{'a':'Q', 'b':'V'},
    'V':{'a':'U', 'b':'Q'},
    'Q':{'a':'Q', 'b':'Q'}
    }
DFA.startstate = 'S'
DFA.acceptstates = ('Q',)

class test_DFA(unittest.TestCase):
    def test_accept(self):
        ls=['ababa','baab','abba','ababaa','bababa','abcdf']
        for i in ls:
            print i,DFA.accept(i)