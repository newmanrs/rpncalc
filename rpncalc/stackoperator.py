from rpncalc.util import ActionEnum, stack


class StackOperator(ActionEnum):
    clear = 'clear'
    swap2 = 'swap2'
    reverse = 'reverse'
    pop_last = 'pop'

    def action(self):
        o = type(self)
        match self:
            case o.clear:
                stack.clear()
            case o.swap2:
                v1, v0 = self.take_2()
                self.push(v1)
                self.push(v0)
            case o.reverse:
                stack.reverse()
            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
