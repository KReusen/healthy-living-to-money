from typing import NamedTuple

class Run(NamedTuple):
    run_id: int
    distance: float

    def to_dict(self) -> dict:
        return self._asdict()