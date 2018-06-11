from typing import NamedTuple, Union

class Run(NamedTuple):
    id: int
    altitude_max: int
    heart_rate_avg: int
    heart_rate_max: int
    distance: float
    speed_avg: float
    speed_max: float
    calories: int
    duration: int
    altitude_min: int
    start_time: str
    descent: int
    ascent: int
    hydration: float
    burgers_burned: float


    def to_dict(self) -> dict:
        return self._asdict()
    
    def get_id(self) -> Union[str, int]:
        return self.id
    
    def get_rounded_distance(self) -> float:
        return round(self.distance, 2)


def create_workout_from_dict(workout_model: object, d: dict) -> object:
    allowed_keys = workout_model._fields
    safe_dict = {}
    for key, value in d.items():
        if key in allowed_keys:
            safe_dict[key] = value
    return workout_model(**safe_dict)