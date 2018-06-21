from dataclasses import dataclass

@dataclass
class Weights:
    old: float
    new: float
    
    def payout_units(self) -> float:
        return round(self.new - self.old, 2)