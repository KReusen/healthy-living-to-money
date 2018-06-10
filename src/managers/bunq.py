from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType

from services.parameter import ParameterService

class BunqManager():
    def __init__(self):
        self.parameter_service = ParameterService()

        if self.parameter_service.exists("/bunq/api_context"):
            self.api_context = self._get_api_context_from_aws()
        else:
            self.api_context = self._create_api_context()
        
    def _get_api_context_from_aws(self):
        json_string = self.parameter_service.get("/bunq/api_context")
        return ApiContext.from_json(json_string)

    def _create_api_context(self) -> ApiContext:
        api_key = self.parameter_service.get('/bunq/api_key')
        api_context = ApiContext(
            ApiEnvironmentType.PRODUCTION, 
            api_key,
            'runs-to-gadgetfund'
        )
        self.parameter_service.store("/bunq/api_context", api_context.to_json())
        return api_context