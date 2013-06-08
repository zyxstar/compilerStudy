import unittest
import Regex

class test_Regex(unittest.TestCase):

    def ttest_find_rparen(self):
        pattern = "abc(hd)df"
        i = Regex.find_rParen(pattern, 4)
        self.assertEqual(i, 6)

        pattern = "abc(h(d)d)f"
        i = Regex.find_rParen(pattern, 4)
        self.assertEqual(i, 9)

        pattern = "(ab()ch(d)d)f"
        i = Regex.find_rParen(pattern, 1)
        self.assertEqual(i, 11)

        pattern = "(ab(())()((()))ch(d)d)f"
        i = Regex.find_rParen(pattern, 1)
        self.assertEqual(i, 21)

    def ttest_find_nextGroup(self):
        data = {'a':'a', 'ab':'ab', 'abc':'abc', 'a(':'a', 'ab(':'ab', 'abc(':'abc',
                  'a|':'a', 'ab|':'ab', 'abc|':'abc', 'a*':'a', 'ab*':'a', 'abc*':'ab'}

        for k, v in data.items():
            r = Regex.find_nextGroup(k, 0)
            print k, v, r, k[0:r]
            self.assertEqual(k[0:r], v)

    def ttest_find_allGroups(self):
        fun = Regex.find_allGroups
        print fun('ab*ab|ab*')
        print fun('(a|b)*aa|bb')
        print fun('(ab*ab|ab*)')
        print fun('ab*ab|ab*|ab(ab|ab)|ab')
        print fun('ab*ab|ab*|ab(ab|ab)')
        print fun('(a|b)*abb')
        print fun('((a|b))*(a(b)b)')
        print fun('(1*01*0)*1*')
        print fun('(a|b)*(aa|bb)(a|b)*')
        print fun('ab|(a|b)*')
        print fun('(1*01*0)*|1*')
        print fun('abc*')
        print fun('a*()a(b)')
        print fun('a|ba*')
        print fun('(())|ba*')

    def ttest_deal(self):
        fun = Regex.deal
        data = ['a', 'ab', 'ab|ab', '(a|b)', 'a*', 'ab*', '(a|b)*abb', '(1*01*0)*1*', '(a|b)*(aa|bb)(a|b)*', '(a|b)*aa|bb']
        for i in data:
            Regex.transList = []
            print i, fun(0, i), Regex.transList


    def test_accept(self):
#        pattern='(a|b)*abb'
#        ls=['abb','ababb','vabb','abbabababb','abba']
#        pattern='(a|b)*(aa|bb)(a|b)* '
#        ls=['abb','ababb','aabb','ababa','aababa']   
#        pattern = '(1*01*0)*1*'
#        ls = ['00', '', '10111', '10001', '100100', '0101010', '1010101']
#        pattern = '(a|b)*aa|bb'
#        ls = ['bb', '', 'a', 'aa', 'aaa', 'aaaa', 'b', 'abb', 'bbb', 'bbbb', 'ababa', 'abaab']
        
        pattern = 'abc*'
        ls = ['ab', '', 'aa', 'abc', 'abcc', 'abccc']

        for i in ls:
            print i,Regex.accept(pattern, i)
