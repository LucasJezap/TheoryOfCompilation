import AST
from SymbolTable import Scope
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ArrayT:
    dims: int
    eltype: any
    size: any

    def __hash__(self):
        return hash((self.dims, self.eltype, self.size))

AnyT = 'any'
IntT = 'int'
FloatT = 'float'
StringT = 'string'
RangeT = 'range'
BoolT = 'bool'

aaa = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: AnyT
        ))
)


for op in '+-*/':
    aaa[op][IntT][IntT] = IntT
    aaa[op][IntT][FloatT] = FloatT
    aaa[op][FloatT][IntT] = FloatT
    aaa[op][FloatT][FloatT] = FloatT
aaa['*'][StringT][IntT] = StringT

for op in ['<', '<=', '>', '>=', '!=', '==']:
    aaa[op][IntT][IntT] = BoolT
    aaa[op][IntT][FloatT] = BoolT
    aaa[op][FloatT][FloatT] = BoolT
    aaa[op][FloatT][FloatT] = BoolT

for op in ['==', '!=']:
    aaa[op][StringT][StringT] = BoolT


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.current_scope = Scope()
        self.loop_count = 0
        self.valid = True

    def show_error(self, msg):
        self.valid = False
        print(msg)

    def visit_IntNum(self, node):
        return IntT

    def visit_FloatNum(self, node):
        return FloatT

    def visit_String(self, node):
        return StringT

    def visit_Block(self, node):
        self.current_scope = Scope(self.current_scope)
        self.visit(node.stmts)
        
        return None

    def visit_FnCall(self, node):
        self.visit(node.args)
        if node.fn in ['zeros', 'eye', 'ones']:
            if not 1 <= len(node.args) <= 2:
                self.show_error(f"Line {node.line}: {node.fn} requires 1 or 2 arguments")
            if all(isinstance(arg, AST.IntNum) for arg in node.args):

                if len(node.args) == 2:
                    return ArrayT(2, FloatT, tuple(arg.value for arg in node.args))
                elif len(node.args) == 1:
                    return ArrayT(2, FloatT, (node.args[0].value, node.args[0].value))

                return ArrayT(2, FloatT, tuple(arg.value for arg in node.args))
            return ArrayT(2, FloatT, (None, None))
        return AnyT
    
    def visit_Print(self, node):
        self.visit(node.args)
        return None

    def visit_Transposition(self, node):
        type1 = self.current_scope.get(node.target)
        if not isinstance(type1, ArrayT):
            self.show_error(f"Line {node.line}: Can not transpose {type1}, type mismatch")
            return ArrayT(2, AnyT, (None,None))
        if type1.dims != 2: 
            self.show_error(f"Line {node.line}: Can not transpose {type1}, dimension mismatch")
            return ArrayT(2, type1.eltype, (None,None))
        m, n = type1.size
        return ArrayT(2, type1.eltype, (n, m))
    
    def visit_UnaryMinus(self, node):
        type1 = self.visit(node.expr)
        if type1 not in [FloatT, IntT]: #  or not isinstance(type1, ArrayT)
            self.show_error(f'Line {node.line}: Can not apply unary minus to {type1}')
        return type1

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op    = node.op
        if op[0] == '.':
            op = op[1:]
            if isinstance(type1, ArrayT) and isinstance(type2, ArrayT):
                if type1.size != type2.size:
                    self.show_error(f"Line {node.line}: Size mismatch during .{op}")
                type3 = aaa[op][type1.eltype][type2.eltype]
                if type3 == AnyT:
                    self.show_error(f'Line {node.line}: Can not apply {op} for {type1.eltype} and {type2.eltype}, expression will result in any type')
                return ArrayT(type1.dims, type3, type1.size)
            elif isinstance(type1, ArrayT):
                type3 = aaa[op][type1.eltype][type2]
                if type3 == AnyT:
                    self.show_error(f'Line {node.line}: Can not apply {op} for {type1.eltype} and {type2}, expression will result in any type')
                return ArrayT(type1.dims, type3, type1.size)
            elif isinstance(type2, ArrayT):
                type3 = aaa[op][type1][type2.eltype]
                if type3 == AnyT:
                    self.show_error(f'Line {node.line}: Can not apply {op} for {type1} and {type2.eltype}, expression will result in any type')
                return ArrayT(type2.dims, type3, type2.size)
            else:
                self.show_error(f'Line {node.line}: Cannnot apply {op} for {type1} and {type2}, at least one argument must be array')
                return AnyT
        else:
            type3 = aaa[op][type1][type2]
            if type3 == AnyT:
                self.show_error(f'Line {node.line}: Can not apply {op} for {type1} and {type2}, expression will result in any type')
            return type3

    def visit_Id(self, node):
        type1 = self.current_scope.get(node.id)
        if type1 == None:
            self.show_error(f'Line {node.line}: Variable can not be found in current scope')
            return AnyT
        return type1
    
    def visit_AssignExpr(self, node):
        type1 = self.visit(node.value)
        if isinstance(node.id, AST.Ref):
            type2 = self.current_scope.get(node.id.target.id)
            # if type1 != type2.eltype:
            #     self.show_error(f"Line {node.line}: Ref assigment type mismatch {type2.eltype} and {type1}")
            return type1
        else:
            self.current_scope.put(node.id.id, type1)
        return type1

    def visit_IfStmt(self, node):
        condt = self.visit(node.cond)
        if condt != BoolT:
            self.show_error(f'Line {node.line}: If must have condition resolving to boolean value, but got {condt}')

        self.push_scope()
        self.visit(node.positive)
        self.pop_scope()

        self.push_scope()
        self.visit(node.negative) # default is Block([])
        self.pop_scope()

        return None

    def visit_ForLoop(self, node):
        self.loop_count += 1
        type1 = self.visit(node.range)
        if type1 != 'range':
            self.show_error(f'Line {node.line}: For loop must be iterating over range, but got {type1}')

        self.push_scope()
        self.current_scope.put(node.id.id, IntT)

        self.visit(node.stmt)

        self.pop_scope()
        self.loop_count -= 1
        return None

    def visit_WhileLoop(self, node):
        self.loop_count += 1

        condt = self.visit(node.cond)
        if condt != BoolT:
            self.show_error(f'Line {node.line}: While loop must have condition resolving to boolean value, but got {condt}')

        self.push_scope()
        self.visit(node.stmt)
        self.pop_scope()

        self.loop_count -= 1
        return None

    def visit_Range(self, node):
        if not self.visit(node.min) == self.visit(node.max) == IntT:
            self.show_error(f"Line {node.line}: Range extremas must be integers")
        return RangeT
    
    def visit_Vector(self, node):
        types = list(map(self.visit, node.values))
        eltype = types[0]
        if any(eltype != t for t in types):
            if isinstance(eltype, ArrayT):
                self.show_error(f"Line {node.line}: Inconsistant vector lengths, choosing first length to fit dimension")
                return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
            self.show_error(f'Line {node.line}: Inconsistant vector value types, choosing any as vector base type')
            return ArrayT(1, AnyT, (len(types),))
        if isinstance(eltype, ArrayT):
            return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
        return ArrayT(1, eltype, (len(types),))

    def visit_Break(self, node):
        if self.loop_count == 0:
            self.show_error(f"Line {node.line}: Line {node.line}: Using break outside of loop")
        return None

    def visit_Continue(self, node):
        if self.loop_count == 0:
            self.show_error(f"Line {node.line}: Using continue outside of loop")
        return None
    
    def visit_Ref(self, node):
        targett = self.current_scope.get(node.target.id) if isinstance(node.target, AST.Id) else self.visit(node.target)

        if targett == StringT and len(node.indices) != 1:
            self.show_error(f"Line {node.line}: Indexing string with {len(node.indices)} dimensions")
            return IntT
        if isinstance(targett, ArrayT): 
            if len(node.indices) != targett.dims:
                self.show_error(f"Line {node.line}: Indexing {targett.dims}d array with {len(node.indices)} dimensions")
            
            for idx, m in zip(node.indices, targett.size):
                if isinstance(idx, AST.Range):
                    if not 0 <= idx.min.value <= idx.max.value < m:
                        self.show_error(f"Line {node.line}: Index out of range")
                        return targett.eltype
                else:
                    if not 0 <= idx.value < m:
                        self.show_error(f"Line {node.line}: Index out of range")
                        return targett.eltype

            return targett.eltype
        self.show_error(f"Line {node.line}: {targett} is not indexable")
        return AnyT
    
    def visit_Return(self, node):
        self.visit(node.expr)
        self.show_error(f"Line {node.line}: return stmt without function definition")
        return None

    def push_scope(self):
        self.current_scope = Scope(self.current_scope)
    
    def pop_scope(self):
        self.current_scope = self.current_scope.parent
