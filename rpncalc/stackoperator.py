from rpncalc.classes import ActionEnum
from rpncalc.state import state


class StackOperator(ActionEnum):
    clear_stack = 'clear', "Clear entire stack."
    clear_store = 'clear_storage', "Clear stored named variables"
    swap2 = 'swap2', "Swap last two elements"
    reverse_stack = 'reverse', "Reverse stack contents"
    pop_last = 'pop', "Remove and discard last item in stack"

    def action(self):
        o = type(self)
        match self:
            case o.clear_stack:
                state.clear_stack()
            case o.swap2:
                v1, v0 = self.take_2()
                self.push(v1)
                self.push(v0)
            case o.reverse_stack:
                state.stack.reverse()
            case o.pop_last:
                self.take_1()
            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
