from enum import Enum, unique
from . import storedvalues
from rpncalc.util import stack

@unique
class IdempotentOperator(Enum):
    print_stack = 'print'
    print_stack_or_value = 'print_sv'
    print_stored_named = 'print_store'

    def action(self):
        o = type(self)
        match self:
            case o.print_stack:
                print(f"Stack: {stack}")
            case o.print_stack_or_value:
                if len(stack) == 1:
                    print(f"{stack[0]}")
                else:
                    print(f"Stack: {stack}")
            case o.print_stored_named:
                print(f"Stored Values {storedvalues.storage}")

            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
