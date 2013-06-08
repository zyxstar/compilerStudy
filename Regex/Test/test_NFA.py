import unittest
import NFA

def cfg1():
    #(a|b)*abb   P55  4.4  text/chapter03/section3/index6_bq.htm
    NFA.states = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    NFA.symbols = ('-1', 'a', 'b')
    NFA.trans = {
           '0':{'-1':('1', '7')},
           '1':{'-1':('2', '4')},
           '2':{'a':('3',)},
           '3':{'-1':('6',)},
           '4':{'b':('5',)},
           '5':{'-1':('6',)},
           '6':{'-1':('1', '7')},
           '7':{'a':('8',)},
           '8':{'b':('9',)},
           '9':{'b':('10',)},
           }
    NFA.startstates = ('0',)
    NFA.acceptstates = ('10',)

def cfg2():
    #(a|b)*(aa|bb)(a|b)*     text/chapter03/section3/index8_bq.htm
    NFA.states = ('0', '1', '2', '3', '4', '5', '6', '7')
    NFA.symbols = ('-1', 'a', 'b')
    NFA.trans = {
           '0':{'-1':('1',)},
           '1':{'-1':('2'), 'a':('1',), 'b':('1',)},
           '2':{'a':('3',), 'b':('4',)},
           '3':{'a':('5',)},
           '4':{'b':('5',)},
           '5':{'-1':('6',)},
           '6':{'-1':('7',), 'a':('6',), 'b':('6',)},
           }
    NFA.startstates = ('0',)
    NFA.acceptstates = ('7',)

def cfg3():
    #include none translation
    NFA.states = ('0', '1', '2', '3', '4', '5', '6', '7')
    NFA.symbols = ('-1', 'a', 'b')
    NFA.trans = {
           '0':{'a':('1',)},
           '1':{'a':('1',), 'b':('1', '2')},
           '2':{'a':('3',), 'b':('2',)},
           '3':{'a':('5',)},
           '4':{'b':('5',)},
           '5':{'-1':('6',)},
           '6':{'-1':('7',), 'a':('6',), 'b':('6',)},
           }
    NFA.startstates = ('0',)
    NFA.acceptstates = ('7',)

def cfg4():
    #(1*01*0)*1*  nesting*
    NFA.states = tuple(range(1, 15))
    NFA.symbols = ('-1', '1', '0')
    NFA.trans = {
           1:{'-1':(2, 11)},
           2:{'-1':(3, 5)},
           3:{'1':(4,)},
           4:{'-1':(3, 5)},
           5:{'0':(6,)},
           6:{'-1':(7, 9)},
           7:{'1':(8,)},
           8:{'-1':(7, 9)},
           9:{'0':(10,)},
           10:{'-1':(2, 11)},
           11:{'-1':(12, 14)},
           12:{'1':(13,)},
           13:{'-1':(12, 14)},
           }
    NFA.startstates = (1,)
    NFA.acceptstates = (14,)

class test_NFA(unittest.TestCase):
    def ttest_e_closure(self):
        cfg1()
        print NFA.e_closure(('5', '10'))
        print NFA.e_closure(NFA.startstates)

    def ttest_move(self):
        cfg1()
        print NFA.move(('1', '2', '4', '5', '6', '7', '9'), 'b')

    def ttest_NFA_2_DFA(self):
        cfg1()
        print NFA.DFA_rename(NFA.NFA_2_DFA())
        cfg2()
        print NFA.DFA_rename(NFA.NFA_2_DFA())

    def ttest_DFA_min(self):
        cfg1()
        #P58 4.8
        dic = {'1':{'a':'6', 'b':'3', 'final':False},
             '2':{'a':'7', 'b':'3', 'final':False},
             '3':{'a':'1', 'b':'5', 'final':False},
             '4':{'a':'4', 'b':'6', 'final':False},
             '5':{'a':'7', 'b':'3', 'final':True},
             '6':{'a':'4', 'b':'1', 'final':True},
             '7':{'a':'4', 'b':'2', 'final':True},
             }
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

        cfg1()
        dic = NFA.DFA_rename(NFA.NFA_2_DFA())
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

        cfg2()
        dic = NFA.DFA_rename(NFA.NFA_2_DFA())
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

    def ttest_do1(self):
        #l(l|d)*
        NFA.states = ('S', 'A', 'Z')
        NFA.symbols = ('-1', 'l', 'd')
        NFA.trans = {
               'S':{'l':('A',)},
               'A':{'-1':('Z',), 'd':('A',), 'l':('A',)},
               }
        NFA.startstates = ('S',)
        NFA.acceptstates = ('Z',)

        dfa = NFA.NFA_2_DFA()
        dic = NFA.DFA_rename(dfa)
        print dfa
        print dic
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

    def ttest_do2(self):
        #cfg1()
        #cfg2()
        cfg3()
        dfa = NFA.NFA_2_DFA()
        dic = NFA.DFA_rename(dfa)
        print dfa
        print dic
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

    def ttest_do3(self):
        #(a|b)*abb
        NFA.states = ('x', '1', '2', '3', '4', 'y')
        NFA.symbols = ('-1', 'a', 'b')
        NFA.trans = {
               'x':{'-1':('1',)},
               '1':{'-1':('2',), 'a':('1',), 'b':('1',)},
               '2':{'a':('3',)},
               '3':{'b':('4',)},
               '4':{'b':('y',)},
               }
        NFA.startstates = ('x',)
        NFA.acceptstates = ('y',)

        dfa = NFA.NFA_2_DFA()
        dic = NFA.DFA_rename(dfa)
        print dfa
        print dic
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

    def ttest_do4(self):
        cfg4()

        dfa = NFA.NFA_2_DFA()
        dic = NFA.DFA_rename(dfa)
        print dfa
        print dic
        print NFA.DFA_min_descript(dic)
        print NFA.DFA_min(dic)

    def test_accept(self):
#        cfg1()
#        ls=['abb','ababb','vabb','abbabababb','abba']
#        cfg2()
#        ls=['abb','ababb','aabb','ababa','aababa']   
        cfg4()
        ls = ['00', '', '10111', '10001', '100100', '0101010', '1010101']
        for i in ls:
            print i, NFA.accept(i)
