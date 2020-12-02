import AST
from dataclasses import dataclass
from collections import defaultdict

# @dataclass
# class VariableSymbol:
#     name: str
#     type: str


# class SymbolTable(object):

#     def __init__(self, parent, name): # parent scope and symbol table name
#         self.parent = parent
#         self.name = name
#         self.dict = defaultdict(lambda: VariableSymbol('undef', 'any'))
#         self.scopes = []
#         self.current_scope = self

#     def put(self, name, symbol): # put variable symbol or fundef under <name> entry
#         self.dict[name] = symbol

#     def get(self, name): # get variable symbol or fundef from <name> entry
#         if name in self.dict:
#             return self.dict[name]
#         if self.parent == None:
#             return self.dict[name]
#         return self.parent.get(name)
        

#     def getParentScope(self):
#         return self.parent

#     def pushScope(self, name):
#         scope = SymbolTable(self, name)
#         self.scopes.append(scope)
#         return scope

#     def popScope(self):
#         pass

class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def put(self, name, symbol):
        self.dict[name] = symbol
    
    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)