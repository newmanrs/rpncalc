import dataclasses
from collections import deque
import json


class DequeEncoder(json.JSONEncoder):
    """
    JSON serialize deque as a list
    """
    def default(self, obj):
        if isinstance(obj, deque):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


@dataclasses.dataclass
class CalculatorOptions:
    verbose: bool = False
    interactive: bool = False
    debug: bool = False
    load_file: str = None


@dataclasses.dataclass
class State:

    stack: list = dataclasses.field(default_factory=list)
    stored_values: dict = dataclasses.field(default_factory=dict)
    last_action: object = None
    actions: deque = dataclasses.field(default_factory=deque)
    expression: str = None

    def print_stack_and_stored(self):
        """
        Print stack, and optionally stored values
        """
        msg = f"Stack: {self.stack}"
        if self.stored_values:
            msg += f", Stored Values: {self.stored_values}"
        print(msg)

    def clear_stack(self):
        self.stack.clear()

    def clear_storage(self):
        self.stored_values.clear()

    def make_snapshot(self):
        return dataclasses.asdict(self)

    def load_snapshot(self, snapshot):
        for k, v in snapshot.items():
            # Deque type is serialized as list
            # and needs to be cast back on load
            if isinstance(getattr(self, k), deque):
                v = deque(v)
            setattr(self, k, v)

    def save_to_file(self, filename, indent=2):
        with open(filename, 'w') as f:
            json.dump(self.make_snapshot(), f, cls=DequeEncoder, indent=indent)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            d = json.load(f)
        self.load_snapshot(d)

    def to_json(self):
        return json.dumps(self.make_snapshot(), cls=DequeEncoder, indent=None)

    def __len__(self):
        return len(state)


state = State()
options = CalculatorOptions()
