import cProfile
import unittest

import recdefs
import parser

class primetest(unittest.TestCase):
    def test_is_prime(self):
        r = recdefs.recdefs()
        self.assertTrue(not r.is_prime(0))
        self.assertTrue(not r.is_prime(1))
        self.assertTrue(    r.is_prime(2))
        self.assertTrue(    r.is_prime(3))
        self.assertTrue(not r.is_prime(4))
        self.assertTrue(    r.is_prime(5))
        self.assertTrue(not r.is_prime(6))
        self.assertTrue(    r.is_prime(7))
        self.assertTrue(not r.is_prime(8))
        self.assertTrue(not r.is_prime(9))
        self.assertTrue(not r.is_prime(10))
        self.assertTrue(    r.is_prime(11))
        self.assertTrue(not r.is_prime(12))
        self.assertTrue(    r.is_prime(13))
        self.assertTrue(not r.is_prime(14))
        self.assertTrue(not r.is_prime(15))
        self.assertTrue(not r.is_prime(16))
        self.assertTrue(    r.is_prime(17))
        self.assertTrue(not r.is_prime(18))
        self.assertTrue(    r.is_prime(19))
        self.assertTrue(not r.is_prime(20))
        self.assertTrue(    r.is_prime(982451653))
        self.assertTrue(not r.is_prime(982451653 + 1))
        self.assertTrue(    r.is_prime(47055833459))
        self.assertTrue(not r.is_prime(47055833459 + 1))

    def test_primeget(self):
        r    = recdefs.recdefs()
        prev = 2
        
        for i in range(0, 500):
            p = r.primeget(i)
            self.assertTrue(r.is_prime(p))
            self.assertTrue(all(not r.is_prime(x)
                                for x in range(prev + 1, p - 1)))
            prev = p

    def test_F_var(self):
        r = recdefs.recdefs()

    def test_F(self):
        r = recdefs.recdefs()
        self.assertTrue(r.F("(a1)") == r.F("( a1 )"))

def parse_test(seq, prod):
    return parser.pctx(seq).parse(prod())

class parsertest(unittest.TestCase):
    def test_parse_var(self):
        self.assertEqual(parse_test("a1", parser.var), "a1")
        self.assertEqual(parse_test("b2", parser.var), "b2")
        self.assertEqual(parse_test("A1", parser.var), "")
        self.assertEqual(parse_test("a0", parser.var), "")
        self.assertEqual(parse_test("z57ZZZ", parser.var), "z57")

    def test_parse_sign1(self):
        self.assertEqual(parse_test("0",  parser.sign1), "0")
        self.assertEqual(parse_test("a1", parser.sign1), "a1")
        self.assertEqual(parse_test("a2", parser.sign1), "")
        self.assertEqual(parse_test("'0", parser.sign1), "'0")
        self.assertEqual(parse_test("''''''0tail", parser.sign1), "''''''0")
        self.assertEqual(parse_test("''''''c1tail", parser.sign1), "''''''c1")
        self.assertEqual(parse_test("''''''c2tail", parser.sign1), "")
        self.assertEqual(parse_test("''@", parser.sign1), "")

    def test_parse_sign(self):
        self.assertEqual(parse_test("0tail", parser.sign),  "0")
        self.assertEqual(parse_test("a1tail", parser.sign), "a1")
        self.assertEqual(parse_test("a2tail", parser.sign), "a2")
        self.assertEqual(parse_test("a0tail", parser.sign), "")
        self.assertEqual(parse_test("'''''k1tail", parser.sign), "'''''k1")
        self.assertEqual(parse_test("tail", parser.sign), "")

    def test_parse_elementary(self):
        self.assertEqual(parse_test("a2(b1)tail", parser.elementary), "a2(b1)")
        self.assertEqual(parse_test("a5(c4)tail", parser.elementary), "a5(c4)")
        self.assertEqual(parse_test("f2(b3)tail", parser.elementary), "")
        self.assertEqual(parse_test("d2(d2)tail", parser.elementary), "")
        self.assertEqual(parse_test("aa(bb)tail", parser.elementary), "")
        self.assertEqual(parse_test("a2(b1?tail", parser.elementary), "")
        self.assertEqual(parse_test("A2(b1)tail", parser.elementary), "")
        self.assertEqual(parse_test("a2.b1)tail", parser.elementary), "")
        self.assertEqual(parse_test("a(2b1)tail", parser.elementary), "")
        self.assertEqual(parse_test("a2()a1tail", parser.elementary), "")
        self.assertEqual(parse_test("()a2a1tail", parser.elementary), "")
        self.assertEqual(parse_test("tail", parser.elementary), "")

    def test_parse_formula(self):
        def f(seq, out = "", dic = None):
            (match, kw) = parser.pctx(seq).parse_kw(parser.formula())
            self.assertEqual(match, out.replace(" ", ""))
            if dic != None:
                self.assertEqual(kw, dic)
        def f_ok(seq):
            f(seq + "tail", seq)

        f_ok("a2(b1)")
        f_ok("(a2(b1))")
        f("()tail")
        f_ok("~(a2(b1))")
        f("~a2(b1)tail")
        f("|")
        f("| 0")
        f("| b5(d4)")
        f("| (b5(d4))")
        f("| (b5(d4)) 0")
        f("| (b5(d4)) ('0)")
        f("| (b5(d4)) a3")
        f("| (b5(d4)) (a3)")
        f("| (b5(d4)) a3(b2)")
        f_ok("| (~(a2(b1))) (~(~(b3(c2))))")
        f("A")
        f("A c")
        f("A c0")
        f("A (c1)")
        f("A (c1) ()")
        f("A (c1) (a3(b2))")
        f_ok("A c1 (a3(b2))")
        f("A c1 a3(b2)")
        f("A c1 ()")
        f("A c1 (0)")
        f_ok("A c5 (| (~(a2(b1))) (~(~(b3(c2)))) )")
        f("A 0 (~(a2(b1)))")
        f("A (~(a2(b1)))")
        f("A (~(a2(b1)) (a2(b1))")
        f_ok("a2(0)")
        f_ok("(b2('''''0))")
        f_ok("((((((c2(''''''''d1)))))))")
        f_ok("Ac3 (Ab2 (c3(b2)))")
        f_ok("Ac3 (Ab2 (| (b2('''g1)) (Ac1 (| (c3(b2)) (b2(''''c1))))))")

class rectest(unittest.TestCase):
    def test_div(self):
        r = recdefs.recdefs()
        self.assertTrue(    r.div(0, 0))
        self.assertTrue(    r.div(0, 1))
        self.assertTrue(    r.div(0, 2))
        self.assertTrue(not r.div(1, 0))
        self.assertTrue(    r.div(1, 1))
        self.assertTrue(not r.div(2, 0))
        self.assertTrue(    r.div(2, 1))
        self.assertTrue(    r.div(2, 2))
        self.assertTrue(not r.div(3, 2))

    def test_Prim(self):
        r = recdefs.recdefs()
        for i in range(0, 100):
            self.assertEqual(r.Prim(i), r.is_prime(i))

    def test_Pr2(self):
        r = recdefs.recdefs()
        for i in range(0, 5):
            p = r.primeget(i)
            self.assertEqual(r.Pr2(0, p), 0)
            self.assertEqual(r.Pr2(1, p), p)
            self.assertEqual(r.Pr2(2, p), 0)

            q = r.primeget(i + 2)
            self.assertEqual(r.Pr2(0, p*q*q), 0)
            self.assertEqual(r.Pr2(1, p*q*q), p)
            self.assertEqual(r.Pr2(2, p*q*q), q)
            self.assertEqual(r.Pr2(3, p*q*q), 0)

    def test_fact(self):
        r = recdefs.recdefs()
        f = 1
        for i in range(1, 20):
            f = i*f
            self.assertEqual(r.fact(i), f)


    def test_Pr(self):
        r = recdefs.recdefs()
        self.assertEqual(r.Pr(0), 0)
        for i in range(0, 10):
            self.assertEqual(r.Pr(i + 1), r.primeget(i))

    def test_Gl(self):
        r = recdefs.recdefs()
        n = r.F("()")
        self.assertEqual(r.Gl(0, n), 0)
        self.assertEqual(r.Gl(1, n), r.Cleft)
        self.assertEqual(r.Gl(2, n), r.Cright)
        n = r.F("")
        self.assertEqual(r.Gl(0, n), 0)
        n = r.F("(a2)")
        self.assertEqual(r.Gl(0, n), 0)
        self.assertEqual(r.Gl(1, n), r.Cleft)
        self.assertEqual(r.Gl(2, n), r.F_var("a", 2))
        self.assertEqual(r.Gl(3, n), r.Cright)

    def test_l(self):
        r = recdefs.recdefs()
        for i in range(0, 2):
            print(i, r.F("(" * i))
            self.assertEqual(r.l(r.F("(" * i)), i)
#        self.assertEqual(r.l(r.F("a2")), 1)
#        self.assertEqual(r.l(r.F(")a2(")), 3)

    def test_con(self):
        r = recdefs.recdefs()
        self.assertEqual(r.con(r.F("("), r.F("(")), r.F("()"))

if __name__ == '__main__':
#    unittest.main()
    cProfile.run("unittest.main()")
