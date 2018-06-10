from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType

from services.parameter import ParameterService
from services.secret import SecretService

class BunqManager():
    def __init__(self):
        self.parameter_service = ParameterService()
        self.secret_service = SecretService()

        if not self.secret_service.secret_exists("bunq"):
            self.create_api_context()
    
    def create_api_context(self):
        api_key = self.parameter_service.get('/bunq/api_key')
        api_context = ApiContext(
            ApiEnvironmentType.PRODUCTION, 
            api_key,
            'runs-to-gadgetfund'
        )
        self.secret_service.store("bunq", api_context.to_json())
        