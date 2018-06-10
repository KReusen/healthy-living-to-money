import os
import rollbar
from typing import List

from services.parameter import ParameterService
from services.secret import SecretService

from managers.endomondo import Endomondo
from managers.s3 import S3Manager
from managers.bunq import BunqManager

from models.run import Run

RUNS_BUCKET_NAME = os.environ.get('RUNS_BUCKET')
PARAMETER_SERVICE = ParameterService()

# rollbar_key = PARAMETER_SERVICE.get('/rollbar/key')
# rollbar.init(rollbar_key, 'runs-to-gadgetfund')

# @rollbar.lambda_function
def handler(event, context):
    s3_manager = S3Manager(RUNS_BUCKET_NAME, 'runs.csv', Run)
    endomondo = Endomondo()
    
    if s3_manager.has_entries_online():
        runs = endomondo.get_runs(5)
        max_id_in_s3 = s3_manager.get_max_int()
    else:
        # runs = endomondo.get_runs(9999)
        runs = endomondo.get_runs(2)
        max_id_in_s3 = 0

    runs_to_upload = [r for r in runs if r.get_id() > max_id_in_s3 ]
    if runs_to_upload:
        bunq_manager = BunqManager()
        payments = create_payment_info_from_runs(runs_to_upload)
        # s3_manager.append(runs_to_upload)

    
def create_payment_info_from_runs(runs: List[Run], multiplier: int = 1):
    pass

if __name__ == "__main__":
    # handler(None, None)
    # bunq_manager = BunqManager()
    secret_service = SecretService()
    secret_string = """{
        "api_key": "31226a89c4bfb22e44a6570bdd3036ac86528364ae5666e2b4be2c98ed524770",
        "environment_type": "PRODUCTION",
        "installation_context": {
            "private_key_client": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDKJ8AlwNVr4n/3\nSMCJTJEm56wzdAf5vuhA+NHqt75BegcJHM3bf8JQlYlpeWEk19Hyz7J3FXVV50Lg\nY744JowSqheGbzDGMmnQSmDS7Qk+AV+xEB/VRY6Zc3hbUXykUnmVCTFPj9G41680\nGg4vpCkdn5T6SDDnqk1vT60N61oB2JIq3i4WfdT6vNcToiaaH9hcEQOwTpwVJyJl\nBKmP6BeK4BnFK4r+8W7c203BgTkRbKnU6mt5uwPW30BvdzvpnLpjtwUksordR03D\nV/YwqpBW0q9hoZkhB+Q+O1tUmofDc6kGAOjjqs6ZgWDQ5AJ8KlrZCZ1LYRkPgt4K\n8pLYFqz9AgMBAAECggEAS+/Go+fdw5rfitpPSMP0OnMIIoPRgyUNRWqyH8NJunrG\nLcweH/fL3E1vwqkPrrFLcjRGy6jJ3Kz0WCnfiGQiddhi4eLepXTGfrGR0Wms8Re/\nBFoUOx7XxBi1+0eO1IMOnMdJOKPDmfWbIK0w6wB1WWVapvF7PWqhj9CUJwhjVRGE\nBqGXWN/rtcP08LjkehUH3BY6MX1R+uY6J7bVZpZ841uDQEbsp6/LPkD6cRutjHyP\nLcucDeTtjrzc5HLmZzo//eii1YrlauG7RH61k5mZkdjz8b/5jeKK95wJu0RcVtRv\nbPs48yftK7E65VWB5iOanA8nx2sW/KCnvvT8ogLhWQKBgQDVk55p4uqMmq9q4jcQ\nGuz1D8soPstzf9WYXj4qgjiVSGWve1nJ42pUzHT2/nGzHWZ/QAdqYlcl+Ys2v+CT\nCwrT0JxmE0zwJCAr/+T57JPZz5NB+5g+3lW39oesD8IjCrYGM1z5K1w4/DZXJltY\nMy5istZ93DspRwZflmXnvXnQwwKBgQDyT1roYoC0RwPudp1Crpog86cQKzM3o3rK\ngA7McrOch2XcUyfeR80zlRuwO6/DbgXWSNIuL6aiHbFse4inZDWw/3Q15ES74JLS\nQExs8feBEBzSbUu5vqEG16yuwZbnwZJfvDavs05veamOvs64WRuS/gVT5qn/l6gl\nB1/P0o2vPwKBgQCp67l0SwoK9aKsqe/fC10NGBStH1CkwscAY7KYBWTZOHFWbRAh\ntKJLdyNzwzpYpAKBKUL9G+J0HxboZz5YHsftf6J+/8oNoOBLwVq+kL+M4j4pl+8n\nzaJrK2QDu8HcOVBanJDS2PGVkOv26FhyUr4L3ncSSZ50F8L1V+YZusDpGwKBgQDi\nAE3kDWvJuarbEdrfxQaQ0XDyzbg5nsr6cLJc0mbgChFhjFXVJtcn01095I2tE8Nx\n9/3BgkRDVLqVWis9JWRGsBzt3viU24NVgw9FVfHpeOPJCJPmrPx361VusbVUd+FU\nVbIT8oOnyavyLdmVa9ciJLdHaA8LC6KS1uvwZIwt9QKBgQCP7PqNKE0RP0CM5c8C\nH2UoVE1qjjr5SPw1vcM6ZpdcDjH/0hIGr0TrkIjoO9g7FyPPT6gFcvUvAXsRAGQv\nW3oA277NwCrL4sXem0o6EWpN68ppn3ORJ0+jAWa8ea8uoUQd30t4prcNm4kyutPB\nEO6uR4UcLUGGCBx8pQlOJPZi4A==\n-----END PRIVATE KEY-----",
            "public_key_client": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyifAJcDVa+J/90jAiUyR\nJuesM3QH+b7oQPjR6re+QXoHCRzN23/CUJWJaXlhJNfR8s+ydxV1VedC4GO+OCaM\nEqoXhm8wxjJp0Epg0u0JPgFfsRAf1UWOmXN4W1F8pFJ5lQkxT4/RuNevNBoOL6Qp\nHZ+U+kgw56pNb0+tDetaAdiSKt4uFn3U+rzXE6Immh/YXBEDsE6cFSciZQSpj+gX\niuAZxSuK/vFu3NtNwYE5EWyp1OprebsD1t9Ab3c76Zy6Y7cFJLKK3UdNw1f2MKqQ\nVtKvYaGZIQfkPjtbVJqHw3OpBgDo46rOmYFg0OQCfCpa2QmdS2EZD4LeCvKS2Bas\n/QIDAQAB\n-----END PUBLIC KEY-----",
            "public_key_server": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAomJ+MluF+AgRKkx9yoyJ\n4pwOQ/f/pUw7lP9ZdeOWNfn+esc1fJkw0Dp3/omLGIjBl0Whe5hp3vJFzWoZsLbV\nMjw8kDm3PjAYTzM3ygcRvBVg1fgXtLmsiSCg4n3GIIqYx4OnUJcGydSm16Tq69o6\nMIRxSTTEJ/YV+c1P61Tb1nP06yPPps/BCFwsiy0DwLM/gvuuGezy66AxnevXwGDq\nykr+1W+x4q1dd4gbSxvWZ+Vm70YJayb9Ayb1rAoVpYyYH3/9hpzN3j4/BV0po2yR\n6yv00BFXhzpyaRhv2JJzMXZrtSz6zVQeSWuHJWEyZWRHw/AC7/OmHW3B8CAS7HS9\nVwIDAQAB\n-----END PUBLIC KEY-----",
            "token": "f2803bb815fefe91c770506355c0d070d4ba7235d165a5af9f889af06a4e5c0f"
        },
        "session_context": {
            "expiry_time": "2018-06-17 23:03:53.310041",
            "token": "ee673cdbc45e125cf1bff208ff3df00398ccce8a3c283bf460213cbd366fc25a",
            "user_id": 352353
        }
    }
    """
    secret_service.store("bunq", secret_string)