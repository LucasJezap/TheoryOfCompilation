
class Memory:

    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def has_key(self, name):
        if name in self.dict:
            return True
        if self.parent == None:
            return False
        return self.parent.has_key(name)

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)

    def put(self, name, value):
        if self.parent and self.parent.has_key(name):
            self.parent.put(name, value)
        else:
            self.dict[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None):
        self.stack = []

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        return self.stack.pop()

