class BasicMultiplier():
    def __init__(self, by: int = 1):
        self.multiply_by = by
    
    def get_amount(self, obj: object) -> float:
        return round(obj.payout_units() * self.multiply_by, 2)