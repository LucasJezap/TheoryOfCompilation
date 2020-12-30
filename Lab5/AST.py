from dataclasses import dataclass

@dataclass
class Node:
    line : str

@dataclass
class IntNum(Node):
    value: int

@dataclass
class FloatNum(Node):
    value: float

@dataclass
class String(Node):
    value: str

@dataclass
class Block(Node):
    stmts: list

@dataclass
class FnCall(Node):
    fn: str
    args: list

@dataclass
class Transposition(Node):
    target: Node

@dataclass
class UnaryMinus(Node):
    expr: Node

@dataclass
class BinExpr(Node):
    op: str
    left: Node
    right: Node

@dataclass
class Id(Node):
    id: str

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.id == other
        elif isinstance(other, Id):
            return self.id == other.id 
        return False

@dataclass
class AssignExpr(Node):
    type: str
    id: Id
    value: Node

@dataclass
class ForLoop(Node):
    id: Id
    range: Node
    stmt: Node

@dataclass
class WhileLoop(Node):
    cond: Node
    stmt: Node

@dataclass
class Range(Node):
    min: Node
    max: Node

@dataclass
class IfStmt(Node):
    cond: Node
    positive: Node
    negative: Node = Block('0', [])

@dataclass
class Vector(Node):
    values: list

@dataclass
class Ref(Node):
    target: Node
    indices: list

@dataclass
class Return(Node):
    expr: Node

@dataclass
class Break(Node):
    pass

@dataclass
class Continue(Node):
    pass

@dataclass
class Print(Node):
    args: list

@dataclass
class Error(Node):
    msg: str
      