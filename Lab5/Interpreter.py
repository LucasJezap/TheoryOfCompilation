import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
from collections import defaultdict
from TypeChecker import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

bbb = defaultdict(lambda a, b : None)

bbb['+'] = lambda a, b: a + b
bbb['-'] = lambda a, b: a - b
bbb['*'] = lambda a, b: a * b
bbb['/'] = lambda a, b: a / b

bbb['<'] = lambda a, b: a < b
bbb['>'] = lambda a, b: a > b
bbb['=='] = lambda a, b: a == b
bbb['!='] = lambda a, b: a != b
bbb['<='] = lambda a, b: a <= b
bbb['>='] = lambda a, b: a >= b

class Interpreter:
    def __init__(self):
        self.memory = Memory()
        self.stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        self.stack.push(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        self.stack.push(node.value)

    @when(AST.String)
    def visit(self, node):
        self.stack.push(node.value)

    @when(AST.Block)
    def visit(self, node):
        for stmt in node.stmts:
            self.visit(stmt)
    
    @when(AST.FnCall)
    def visit(self, node):
        for arg in node.args:
            self.visit(arg) 

        if node.fn in ['zeros', 'ones']  :
            fill = 0 if node.fn == 'zeros' else 1
            if len(node.args) == 2:
                n = self.stack.pop()
                m = self.stack.pop()
                self.stack.push(np.array([[fill] * m for i in range(n)]))
            elif len(node.args) == 1:
                n = self.stack.pop()
                self.stack.push(np.array([fill] * n))
        elif node.fn == 'eye':
                n = self.stack.pop()
                self.stack.push(np.array([[1 if j == i else 0 for j in range(n)] for i in range(n)]))

    @when(AST.Transposition)
    def visit(self, node):
        self.visit(node.target)
        M = self.stack.pop()
        self.stack.push(np.transpose(M))

    @when(AST.UnaryMinus)
    def visit(self, node):
        self.visit(node.expr)
        self.stack.push(-self.stack.pop())

    @when(AST.BinExpr)
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)

        r = self.stack.pop()
        l = self.stack.pop()

        op = node.op[1:] if node.op[0] == '.' else node.op

        self.stack.push(bbb[op](l, r))

    @when(AST.Id)
    def visit(self, node):
        self.stack.push(self.memory.get(node.id))

    @when(AST.AssignExpr)
    def visit(self, node):
        if node.type == '=':
            if isinstance(node.id, AST.Ref):
                self.visit(node.id.target)
                target = self.stack.pop()

                self.visit(node.value)
                value = self.stack.pop()

                for idx in node.id.indices:
                    self.visit(idx)
                
                indices = tuple(reversed([self.stack.pop() for _ in node.id.indices]))
                indices = tuple(idx if not isinstance(idx, range) else slice(idx.start, idx.stop) for idx in indices)

                np.ndarray.__setitem__(target, indices, value)
            else:
                self.visit(node.value)
                self.memory.put(node.id.id, self.stack.pop())
        else:
            self.visit(AST.BinExpr(node.line, node.type[:-1], node.id, node.value))
            self.memory.put(node.id.id, self.stack.pop())

    @when(AST.ForLoop)
    def visit(self, node):
        fid = node.id.id
        self.visit(node.range)
        frange = self.stack.pop()
        
        self.push_scope()
        try:
            for fvalue in frange:
                self.memory.put(fid, fvalue)
                try:
                    self.visit(node.stmt)
                except ContinueException:
                    pass
        except BreakException:
            pass
        finally:
            self.pop_scope()

    @when(AST.WhileLoop)
    def visit(self, node):
        self.visit(node.cond)
        cond = self.stack.pop()
        
        self.push_scope()
        try:
            while cond:
                try:
                    self.visit(node.stmt)
                except ContinueException:
                    pass
                self.visit(node.cond)
                cond = self.stack.pop()
        except BreakException:
            pass
        finally:
            self.pop_scope()
    
    @when(AST.Range)
    def visit(self, node):
        self.visit(node.min)
        self.visit(node.max)
        rmax = self.stack.pop()
        rmin = self.stack.pop()
        self.stack.push(range(rmin, rmax + 1))

    @when(AST.IfStmt)
    def visit(self, node):
        self.visit(node.cond)
        cond = self.stack.pop()

        self.visit(node.positive if cond else node.negative)

    @when(AST.Vector)
    def visit(self, node):
        for value in node.values:
            self.visit(value)
        self.stack.push(np.array(list(reversed([self.stack.pop() for value in node.values]))))

    @when(AST.Ref)
    def visit(self, node):
        self.visit(node.target)
        target = self.stack.pop()

        for idx in node.indices:
            self.visit(idx)

        indices = tuple(reversed([self.stack.pop() for _ in node.indices]))
        indices = tuple(idx if not isinstance(idx, range) else slice(idx.start, idx.stop) for idx in indices)

        A = np.ndarray.__getitem__(target, indices)
        self.stack.push(A)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Print)
    def visit(self, node):
        for arg in node.args:
            self.visit(arg)
        
        for arg in reversed([self.stack.pop() for i in range(len(node.args))]):
            sys.stdout.write(str(arg) + ' ')
        print()
    
    def push_scope(self):
        self.memory = Memory(self.memory)
    
    def pop_scope(self):
        self.memory = self.memory.parent