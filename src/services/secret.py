
import json
import boto3
from botocore.exceptions import ClientError

class SecretService():
    def __init__(self):
        self.sm = boto3.client('secretsmanager')
    
    def store(self, name: str, data: str):
        if self._secret_exists(name):
            self._put_secret(name, data)
        else:
            self._create_secret(name, data)

    def _put_secret(self, name: str, data: str):
        self.sm.put_secret_value(
            SecretId=name,
            SecretString=data
        )

    def _create_secret(self, name: str, data: str):
        self.sm.create_secret(
            Name=name,
            SecretString=data
        )
    
    def _secret_exists(self, name: str) -> bool:
        try:
            self.sm.get_secret_value(
                SecretId=name
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "ResourceNotFoundException":
                return False
    
    def get(self, name: str) -> str:
        self.sm.get_secret_value(
            SecretId=name
        )
    
    def get_as_dict(self, name: str) -> dict:
        response = self.get(name)
        return json.loads(response)

