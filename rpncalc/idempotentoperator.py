import sys

from rpncalc.classes import ActionEnum
from rpncalc.state import state


class IdempotentOperator(ActionEnum):
    print_stack = 'print', "Prints the stack"
    print_stack_or_value = 'print_sv', \
        "Prints the whole stack, or a single value if" \
        " the stack contains only said value"
    print_stored_named = 'print_store', \
        "Prints the names and values of all stored constants"
    print_state = 'print_state', \
        "Print all calculator state including stack and storage"
    quit = 'quit'
    exit = 'exit'

    def action(self):
        stack = state.stack
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
                print(f"Stored Values {state.stored_values}")
            case o.print_state:
                print(state)
            case o.quit:
                sys.exit(0)
            case o.exit:
                sys.exit(0)

            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)

    def verbose_mode_message(self):
        pass
