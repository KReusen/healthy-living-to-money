from typing import NamedTuple, Union

class Run(NamedTuple):
    run_id: int
    distance: float

    def to_dict(self) -> dict:
        return self._asdict()
    
    def get_id(self) -> Union[str, int]:
        return self.run_id