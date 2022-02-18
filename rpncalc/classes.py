import enum
from rpncalc.state import state
from rpncalc.exceptions import StackDepletedError


class StackAccessor:
    def gen_n(self, n):

        if n > len(state.stack):
            msg = (
                f"Empty stack processing {self} trying "
                f"to pop {n} values. Stack: {state.stack}")
            raise StackDepletedError(msg)

        for i in range(n):
            yield state.stack.pop()

    def stack_size(self):
        return len(state.stack)

    def take_n(self, n):
        if n == 1:
            return next(self.gen_n(1))
        else:
            return tuple(self.gen_n(n))

    def take_1(self):
        return self.take_n(1)

    def take_2(self):
        return self.take_n(2)

    def take_3(self):
        return self.take_n(3)

    def take_all(self):
        return self.take_n(len(state.stack))

    def push(self, value):
        # use of += in if statement creates local binding
        # shrug python things
        if isinstance(value, list):
            state.stack += value
        else:
            state.stack.append(value)


@enum.unique
class ActionEnum(StackAccessor, enum.Enum):

    def __init__(self, value, description=None):
        """
        Allow for optional description as optional second parameter
        for commands in the enum values
        """
        self.description = description

    def __new__(cls, *args):
        """
        Override the value of an enum being the full tuple
        on rhs of equals to being the first member only,
        allowing for things like comments or help strings to
        be embedded into different commands.
        """

        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def action(self):
        msg = f"Default action not implemented for {self}"
        raise NotImplementedError(msg)

    def help(self):
        if self.description:
            return f" {self.description}"
        return ""

    def verbose_mode_message(self):
        print(f"Applying {self}")
