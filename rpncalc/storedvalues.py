from rpncalc.util import StackAccessor

storage = dict()


def clear_storage():
    storage.clear()


def get_stored_value_class(arg):
    """
    Convert input arg into either a storewrite or store read class
    based on name.  Strings prefixed with store_ are converted to
    write objects.  Strings prefixed with '_' are converted to read
    objects.  I.e. `rpncalc 1 2 3 prod store_x _x` should give 6.
    """
    if arg.startswith('store_'):
        name = arg[5:]
        return StoredValueWrite(name)
    elif arg.startswith('_'):
        name = arg
        return StoredValueRead(name)
    else:
        msg = 'parse failure'
        raise ValueError(msg)


class StoredValueWrite(StackAccessor):

    def __init__(self, name):
        self.name = name

    def action(self):
        storage[self.name] = self.take_1()

    def verbose_mode_message(self):
        print(f"Popping stack into stored value {self.name}")


class StoredValueRead(StackAccessor):
    def __init__(self, name):
        self.name = name

    def action(self):
        try:
            self.push(storage[self.name])
        except KeyError as e:
            k = tuple(storage.keys())
            if len(k) == 0:
                avail = "No stored keys"
            elif len(k) == 1:
                avail = f"Available key is {k[0]}"
            else:
                avail = f"Available keys are {k}"

            msg = f"No stored value '{self.name}'. {avail}."
            raise KeyError(msg) from e

    def verbose_mode_message(self):
        print(f"Pushing stored value {self.name} to stack")
