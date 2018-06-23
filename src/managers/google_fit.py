import time
import requests

from typing import Optional

class WeightManager():
    def __init__(self, access_token: str):
        self.access_token = access_token
    
    def get_weights(self, min_nanos: int, max_nanos: Optional[int] = None) -> Optional[list]:
        if max_nanos is None:
            max_nanos = get_current_nanos()

        # loop in multiple batches if necessary
        # add seperate request method
        # change google fit service entirely into one manager that authenticates, and then has a weight method and a heartrate method?
        
        

class HeartrateManager:
    pass

def get_current_nanos():
    return int(time.time()) * 1000000000