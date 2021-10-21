import enum

stack = []


class StackAccessor:
    def gen_n(self, n):
        """
        Generator that pops up to n values from stack.
        Optional actor gives clearer error messages.
        """
        if n > len(stack):
            msg = (
                f"Empty stack processing {self} trying "
                f"to pop {n} values. Stack: {stack}")
            raise IndexError(msg)

        for i in range(n):
            yield stack.pop()

    def stack_size(self):
        return len(stack)

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
        return self.take_n(len(stack))

    def push(self, value):
        global stack
        if isinstance(value,list):
            stack+=value
        else:
            stack.append(value)


@enum.unique
class ActionEnum(StackAccessor, enum.Enum):
    def action(self):
        msg = f"No action method defined in {self}"
        raise NotImplementedError(msg)
