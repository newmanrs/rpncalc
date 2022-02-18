import dataclasses
import json


@dataclasses.dataclass
class State:

    stack: list = dataclasses.field(default_factory=list)
    stored_values: dict = dataclasses.field(default_factory=dict)

    def clear_stack(self):
        self.stack.clear()

    def clear_storage(self):
        self.stored_values.clear()

    def make_snapshot(self):
        return dataclasses.asdict(self)

    def load_snapshot(self, snapshot):
        for k, v in snapshot.items():
            setattr(self, k, v)

    def save_to_file(self, filename, indent=2):
        with open(filename, 'w') as f:
            json.dump(self.make_snapshot(), f, indent=indent)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            d = json.load(f)
        self.load_snapshot(d)

    def to_json(self):
        return json.dumps(self.make_snapshot(), indent=None)

    def __len__(self):
        return len(state)


state = State()
