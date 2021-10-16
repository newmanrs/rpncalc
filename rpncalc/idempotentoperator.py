from enum import Enum, unique

@unique
class IdempotentOperator(Enum):
    print_stack = 'print'

    def action(self, stack):

        match self.name:
            case 'print_stack':
                print(f"Stack: {stack}")
            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)

