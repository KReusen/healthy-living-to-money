from typing import NamedTuple, Union, Optional, List
from dataclasses import dataclass
from utils.models import get_field_names_from_data_model

@dataclass
class Run:
    id: int
    distance: float
    calories: int
    duration: int
    start_time: str
    burgers_burned: float
    speed_avg: Optional[float] = None
    speed_max: Optional[float] = None
    descent: Optional[int] = None
    ascent: Optional[int] = None
    altitude_max: Optional[int] = None
    altitude_min: Optional[int] = None
    hydration: Optional[float] = None
    heart_rate_avg: Optional[int] = None
    heart_rate_max: Optional[int] = None


    def to_dict(self) -> dict:
        return self.__dict__
    
    def get_id(self) -> Union[str, int]:
        return self.id

    def get_field_names(self) -> List[str]:
        return [key for key in self.__dict__ ]
    
    def payout_units(self) -> float:
        return round(self.distance, 2)
