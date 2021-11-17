import sys
from rpncalc import storedvalues
from rpncalc.util import ActionEnum, stack


class IdempotentOperator(ActionEnum):
    print_stack = 'print'
    print_stack_or_value = 'print_sv'
    print_stored_named = 'print_store'
    quit = 'quit'

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
            case o.quit:
                print("Quitting")
                sys.exit(0)

            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
