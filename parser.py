import unittest

class pctx(object):
    def __init__(self, seq):
        self.seq = seq.replace(" ", "")
        self.dic = { "var" : [], "bound" : [] }

    def parse_kw(self, prod):
        lctx    = pctx(self.seq)
        prod.kw = {}
        self.match = ""
        match = prod.parse(lctx)
        if match != "":
            assert self.seq.startswith(match)
            self.seq   = self.seq[len(match):]
            self.match = match
            self.dic.update(lctx.dic)
        return (match, prod.kw)

    def parse(self, prod):
        (match, _) = self.parse_kw(prod)
        return match

class prod(object):
    pass

class literal(prod):
    def __init__(self, s):
        self.s = s

    def parse(self, ctx):
        if ctx.seq.startswith(self.s):
            return self.s
        else:
            return ""

class typ(prod):
    def parse(self, ctx):
        t = ""
        for ch in ctx.seq:
            if "0" <= ch and ch <= "9":
                t += ch
            else:
                break
        return t

class varhead(prod):
    def parse(self, ctx):
        if ctx.seq != "" and is_var(ctx.seq[0]):
            return ctx.seq[0]
        else:
            return ""

class var(prod):
    def parse(self, ctx):
        vhead = ctx.parse(varhead())
        t     = ctx.parse(typ())
        if vhead != "" and t != "":
            if int(t) > 0:
                self.kw["typ"] = int(t)
                ctx.dic["var"].append(self)
                return vhead + t
        return ""

class sign1(prod):
    def parse(self, ctx):
        result = ""
        while ctx.parse(literal("'")) != "":
            result += "'"
        if ctx.parse(literal("0")) != "":
            self.kw["number"] = True
            return result + "0"
        else:
            (v, kw) = ctx.parse_kw(var())
            if v != "" and kw["typ"] == 1:
                return result + v
        return ""

class sign(prod):
    def parse(self, ctx):
        if ctx.parse(sign1()) != "":
            self.kw["typ"] = 1
            return ctx.match
        else:
            (v, kw) = ctx.parse_kw(var())
            if v != "" and kw["typ"] > 1:
                self.kw = kw
            else:
                return ""
        return ctx.match

class elementary(prod):
    def parse(self, ctx):
        (a, kwa) = ctx.parse_kw(sign())
        l        = ctx.parse(literal("("))
        (b, kwb) = ctx.parse_kw(sign())
        r        = ctx.parse(literal(")"))
        if a != "" and l != "" and b != "" and r != "" and \
           kwa["typ"] == kwb["typ"] + 1:
            return a + "(" + b + ")"
        else:
            return ""

class paren(prod):
    def parse(self, ctx):
        l       = ctx.parse(literal("("))
        (a, kw) = ctx.parse_kw(formula())
        r       = ctx.parse(literal(")"))
        if l != "" and a != "" and r != "":
            self.kw = kw
            return "(" + a + ")"
        else:
            return ""
        
class formula(prod):
    def parse(self, ctx):
        if ctx.parse(elementary()) != "":
            return ctx.match
        # look ahead to avoid infinite recursion
        elif ctx.seq != "" and ctx.seq[0] == "(" and ctx.parse(paren()) != "":
            return ctx.match
        elif ctx.parse(literal("~")) != "" and ctx.parse(paren()) != "":
            return "~" + ctx.match
        elif ctx.parse(literal("|")) != "":
            a = ctx.parse(paren())
            b = ctx.parse(paren())
            if a != "" and b != "":
                return "|" + a + b
        elif ctx.parse(literal("A")) != "":
            vtok = var()
            v = ctx.parse(vtok)
            a = ctx.parse(paren())
            if v != "" and a != "":
                ctx.dic["bound"].append(vtok)
                return "A" + v + a
        return ""


def is_var(ch):
    return "a" <= ch and ch <= "z"


