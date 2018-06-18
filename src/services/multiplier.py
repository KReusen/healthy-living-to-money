class BasicRunMultiplier():
    def __init__(self, by: int = 1):
        self.multiply_by = by
    
    def get_amount(self, run: object) -> str:
        return str(round(run.distance * self.multiply_by, 2))