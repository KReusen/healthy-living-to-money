import requests
import platform
import uuid, socket

from typing import List

from managers.parameter import ParameterManager
from models.workout import Run, create_workout_from_dict

from utils.models import create_model_from_dict

class ConfigError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class EndomondoService():
    def __init__(self):
        self.parameter_manager = ParameterManager()
        self.config = self._get_config()
        if not all (k in self.config for k in ("email","password")):
            raise ConfigError("""Please put the following paths and their 
            values in the aws parameter store
            
            /endomondo/email
            /endomondo/password
            """)
        self._authenticate()

    def _get_config(self):
        return self.parameter_manager.get_multiple('/endomondo/')

    def _authenticate(self):
        auth_key = self.config.get("auth_key")
        if not auth_key:
            auth_key = self._get_key()
            self.parameter_manager.store('/endomondo/auth_key', auth_key)
    
    def _get_key(self) -> str:
        url = 'https://api.mobile.endomondo.com/mobile/auth'
        # taken from https://github.com/isoteemu/sports-tracker-liberator/blob/master/endomondo/endomondo.py
        params = {
            'os':			platform.system(),
            'model':		platform.python_implementation(),
            'osVersion':	platform.release(),
            'vendor':		'github/kreusen',
            'appVariant':	'endomondo-api',
            'country':		'GB',
            'v':			'2.4',
            'appVersion':	'0.1',
            'deviceId':		str(uuid.uuid5(uuid.NAMESPACE_DNS, socket.gethostname())),
            "action":       "pair",
            "email":        self.config.get("email"),
            "password":     self.config.get("password")
        }
        r = requests.get(url, params=params)
        
        lines = r.text.split("\n")
        if lines[0] != "OK":
            raise AuthenticationError(f"Could not authenticate with Endomondo, Expected 'OK', got '{lines[0]}'")

        for line in lines[1:]:
            key, value = line.split("=")
            if key == "authToken":
                return value
    
    def get_runs(self, maxresults: int = 25) -> List[Run]:
        url = f"https://api.mobile.endomondo.com/mobile/api/workouts?authToken={self.config.get('auth_key')}&maxResults={maxresults}&fields=basic"
        r = requests.get(url)
        response = r.json()

        runs = []
        for workout in response["data"]:
            # only get runs
            if workout["sport"] == 0 and workout["live"] == False:
                run = create_model_from_dict(Run, workout)
                runs.append(run)
        
        return runs
