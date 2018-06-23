import httplib2
import json
from oauth2client.client import GoogleCredentials
from managers.parameter import ParameterManager

# To get the google fit authentication keys for the very first time, run
# scripts/google_fit_init_auth.py

class GoogleFitService():
    def __init__(self):
        self.parameter_manager = ParameterManager()
    
    def get_credentials(self) -> dict:
        """ Authenticates with google fit and returns a dictionary with
        the most recent valid credentials """
        online_credentials = self.parameter_manager.get_multiple('/google_fit/')
        credentials = GoogleCredentials(**online_credentials, token_expiry=None, user_agent=None)

        http = credentials.authorize(httplib2.Http())
        credentials.refresh(http)

        credentials_dict = json.loads(credentials.to_json())
        self.store_credentials(credentials_dict)

        return credentials_dict
    
    def store_credentials(self, credentials_dict: dict):
        keys_to_store = ["access_token", "client_secret", "client_id", "refresh_token", "token_uri"]
        for key in keys_to_store:
            if key in credentials_dict:
                path = f'/google_fit/{key}'
                value = credentials_dict.get(key)
                self.parameter_manager.store(path, value)
        

if __name__ == "__main__":
    google_fit_service = GoogleFitService()
    credentials = google_fit_service.get_credentials()
    print(credentials)