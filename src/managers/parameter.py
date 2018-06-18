import boto3
from botocore.exceptions import ClientError

class ParameterNotFound(Exception):
    pass

class ParameterManager():
    def __init__(self):
        self.ssm = boto3.client('ssm')

    def get(self, path: str, decryption: bool = True):
        try:
            response = self.ssm.get_parameter(
                Name=path,
                WithDecryption=decryption
            )
            return response["Parameter"]["Value"]
        except ClientError as e:
            if e.response['Error']['Code'] == "ParameterNotFound":
                raise ParameterNotFound(f"Could not find the following parameter: {path}")

    def get_multiple(self, path: str, decryption: bool = True) -> dict:
        response = self.ssm.get_parameters_by_path(
            Path=path,
            Recursive=False,
            WithDecryption=decryption
        )
        values = {}
        for p in response["Parameters"]:
            name = p["Name"].split(path)[-1]
            values[name] = p["Value"]
        return values
    
    def store(self, path: str, value: str):
        self.ssm.put_parameter(
            Name=path,
            Value=value,
            Type='SecureString',
            Overwrite=True,
        )
    
    def exists(self, path: str, decryption: bool = True) -> bool:
        try:
            self.ssm.get_parameter(
                Name=path,
                WithDecryption=decryption
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "ParameterNotFound":
                return False

