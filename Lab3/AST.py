from dataclasses import dataclass

class Node:
    pass

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
    negative: Node = Block([])

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
class Error(Node):
    msg: str
      