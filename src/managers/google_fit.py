import httplib2
import json
import time
import os
import requests
from typing import Optional, List
from oauth2client.client import GoogleCredentials

from managers.parameter import ParameterManager
from exceptions.google_fit import GoogleFitError

from models.body import WeightEntry

class GoogleFitManager():
    def __init__(self):
        self.parameter_manager = ParameterManager()
        self.access_token = None
    
    def authenticate(self):
        if self.access_token is None:
            credentials = self._get_credentials()
            self.access_token = credentials.get("access_token")

    def _get_credentials(self) -> dict:
        """ Authenticates with google fit and returns a dictionary with
        the most recent valid credentials """
        online_credentials = self.parameter_manager.get_multiple('/google_fit/')
        credentials = GoogleCredentials(**online_credentials, token_expiry=None, user_agent=None)

        http = credentials.authorize(httplib2.Http())
        credentials.refresh(http)

        credentials_dict = json.loads(credentials.to_json())
        self.access_token = credentials_dict.get("access_token")
        self._store_credentials_online(credentials_dict)

        return credentials_dict        

    def _store_credentials_online(self, credentials_dict: dict):
        keys_to_store = ["access_token", "client_secret", "client_id", "refresh_token", "token_uri"]
        for key in keys_to_store:
            if key in credentials_dict:
                path = f'/google_fit/{key}'
                value = credentials_dict.get(key)
                self.parameter_manager.store(path, value)
    
    def get_weights(self, min_nanos: int, max_nanos: Optional[int] = None) -> Optional[List[WeightEntry]]:
        if max_nanos is None:
            max_nanos = get_current_nanos()
        
        base_url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/datasets'
        
        # batch requests pe

    def batch_requests(self, base_url: str, min_nanos: int, max_nanos: int, batch_per_n_nanos: int = 8640000000):
        pass


    def build_url(self, base_url: str, min_nanos: int, max_nanos: int) -> str:
        return os.path.join(base_url, f'{min_nanos}-{max_nanos}')

    def make_request(self, url: str):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        r = requests.get(url, headers=headers)
        response = r.json()
        if "error" in response:
            raise GoogleFitError(response)
        return response

    def extract_values(self, response: dict) -> List[dict]:
        point = response.get("point")
        extracted_values = []
        if point:
            for p in point:
                extracted_value = {
                    "startTimeNanos": p.get("startTimeNanos"),
                    "value": p["value"][0]["fpVal"]
                }
                extracted_values.append(extracted_value)
        
        return extracted_values




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