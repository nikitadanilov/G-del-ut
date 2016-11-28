import parser

"""
http://www.csee.wvu.edu/~xinl/library/papers/math/Godel.pdf
"""

class recdefs:
    C0     =  1
    Cf     =  3
    Cneg   =  5
    Cor    =  7
    Call   =  9
    Cleft  = 11
    Cright = 13

    F_basic = {
        "0" : C0,
        "'" : Cf, # use "'" instead of "f" to avoid clashes with variables
        "~" : Cneg,
        "|" : Cor,
        "A" : Call,
        "(" : Cleft,
        ")" : Cright
    }

    def F_var(self, var, typ):
        assert(typ > 0)
        assert(len(var) == 1)
        assert(self.primeget(5) == 13)
        return pow(self.primeget(5 + 1 + ord(var) - ord("a")), typ)

    # Φ function. Called F, because some python tools have problems with
    # non-ascii method names (e.g., cProfile).
    def F(self, seq):
        idx    = 0
        result = 1
        seq = seq.replace(" ", "") # remove spaces
        while seq != "":
            ch  = seq[0]
            if ch in self.F_basic:
                n   = self.F_basic[ch]
                seq = seq[1:]
            else: # variable
                assert parser.is_var(ch)
                ctx = parser.pctx(seq)
                (_, kw) = ctx.parse_kw(parser.var())
                seq = ctx.seq
                n = self.F_var(ch, kw["typ"])
            result *= pow(self.primeget(idx), n)
            idx += 1
        return result

    def exists(self, limit, fun):
        return any(fun(x) for x in range(0, limit))

    def forall(self, limit, fun):
        return all(fun(x) for x in range(0, limit))

    def rec(self, init, h):
        def f(n):
            r = init
            for i in range(1, n + 1):
                r = h(i, r)
            return r
        return f

    # ε-functional. Called e, because some python tools have problems with
    # non-ascii method names (e.g., cProfile).
    def e(self, limit, F):
        return next(filter(F, range(0, limit)), 0)

    def div(self, x, y):
        if y != 0:
            return x % y == 0
        else:
            return x == 0
#        return self.exists(x + 1, lambda z: x == y * z)

    def Prim(self, x):
        return not self.exists(x + 1, lambda z: z != 1 and z != x and
                               self.div(x, z)) and x > 1

    def Pr2(self, n, x):
        return self.rec(0, lambda n, p: self.e(x + 1, lambda y: self.Prim(y) and
                                               self.div(x, y) and y > p))(n)

    def fact(self, n):
        return self.rec(1, lambda x, p: x * p)(n)

    def Pr(self, n):
        return self.rec(0, lambda x, p: self.e(self.fact(p) + 2,
                                    lambda y: self.Prim(y) and y > p))(n)

    def Gl(self, n, x):
        k = self.Pr2(n, x) # Avoid recalculation of Pr2(n, x).
        return self.e(x + 1,
                      # Another lambda to avoid recalculation of pow(k, y).
                      lambda y: (lambda p: self.div(x, p) and
                                 not self.div(x, p * k))(pow(k, y)))

    def l(self, x):
        return self.e(x + 1,
                      lambda y: self.Pr2(y, x) > 0 and self.Pr2(y + 1, x) == 0)

    def con(self, x, y):
        lx = self.l(x)
        ly = self.l(y)
        return self.e(pow(self.Pr(lx + ly), x + y),
                      lambda z:
                      self.forall(lx + 1, lambda n:
                                  self.Gl(n, z) == self.Gl(n, x)) and
                      self.forall(ly + 1, lambda n: n > 0 and
                                  self.Gl(n + lx, z) == self.Gl(n, y)))

    def primeget(self, n):
        if n == 0:
            p = 2
        else:
            p = 3
            while n > 1:
                p += 2
                while not self.is_prime(p):
                    p += 2
                n -= 1
        assert(self.is_prime(p))
        return p

    def is_prime(self, n):
        assert(n >= 0)
        if n < 2: 
            return False
        if n % 2 == 0:             
            return n == 2
        k = 3
        while k*k <= n:
            if n % k == 0:
                return False
            k += 2
        return True
