#stack = [1,2,3,4]
storage = dict()

def get_stored_value_class(arg):

    if arg.startswith('store'):
        name   = arg[5:]
        return StoredValueWrite(name)
    elif arg.startswith('_'):
        name   = arg
        return StoredValueRead(name)
    else:
        msg = 'parse failure'
        raise ValueError

class StoredValueWrite:

    def __init__(self, name):
        self.name = name

    def action(self,stack):
        storage[self.name] = stack.pop()

class StoredValueRead:
    def __init__(self, name):
        self.name = name

    def action(self,stack):
        stack.append(storage[self.name])
