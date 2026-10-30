from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.specs.request_specs import RequestSpecs


class AuthApi(BaseApi):
    LOGIN_ENDPOINT = "/auth/token/login"

    def login(self,
              credentials: LoginUserRequest,
              response_spec=None,
              response_model=None
              ):
        return self.post(
            endpoint=self.LOGIN_ENDPOINT,
            json_data=credentials.model_dump(mode="json"),
            headers=RequestSpecs.unauth_headers(),
            response_spec=response_spec,
            response_model=response_model,
        )
