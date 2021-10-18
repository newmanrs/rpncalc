from enum import Enum, unique
from . import storedvalues


@unique
class IdempotentOperator(Enum):
    print_stack = 'print'
    print_stored_named = 'print_store'

    def action(self, stack):

        o = type(self)
        match self:
            case o.print_stack:
                print(f"Stack: {stack}")
            case o.print_stored_named:
                print(f"Stored Values {storedvalues.storage}")

            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
