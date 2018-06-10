import boto3

class ParameterService():
    def __init__(self):
        self.ssm = boto3.client('ssm')

    def get(self, path: str, decryption: bool = True):
        response = self.ssm.get_parameter(
            Name=path,
            WithDecryption=decryption
        )
        return response["Parameter"]["Value"]

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

