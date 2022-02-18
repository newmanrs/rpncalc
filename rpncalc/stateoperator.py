from rpncalc.classes import ActionEnum
from rpncalc.state import state


class StateOperator(ActionEnum):
    clear_stack = 'clear', "Clear entire stack."
    clear_store = 'clear_storage', "Clear stored named variables"
    swap2 = 'swap2', "Swap last two elements"
    reverse_stack = 'reverse', "Reverse stack contents"
    pop_last = 'pop', "Remove and discard last item in stack"
    save = 'save', "Save calculator state to user prompted filename"
    load = 'load', "Load calculator state from user prompted filename"

    def action(self):
        o = type(self)
        match self:
            case o.clear_stack:
                state.clear_stack()
            case o.clear_store:
                state.clear_storage()
            case o.swap2:
                v1, v0 = self.take_2()
                self.push(v1)
                self.push(v0)
            case o.reverse_stack:
                state.stack.reverse()
            case o.pop_last:
                self.take_1()
            case o.save:
                filename = input("Enter filename to save to:\n")
                state.save_to_file(filename)
            case o.load:
                filename = input("Enter filename to load from:\n")
                state.load_from_file(filename)
            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
