from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.db.repositories.account_repository import AccountRepository


@pytest.fixture
def account_repository(db_session: Session):
    return AccountRepository(db_session)


@pytest.fixture
def created_account(
        created_user: CreateUserResponse,
        create_user_request: CreateUserRequest,
        api_manager: ApiManager
):
    user_credentials = LoginUserRequest(
        username=create_user_request.username,
        password=create_user_request.password
    )

    api_manager.authenticate(user_credentials)

    response = api_manager.user_steps.create_account()

    assert response.status_code == HTTPStatus.CREATED, (
        f'Полученный статус {response.status_code}, '
        f'ожидался {HTTPStatus.CREATED}.'
    )

    return CreateAccountResponse.model_validate(response.json())

@pytest.fixture
def account_transfer_data():
    transfer_data = RandomModelGenerator.generate(AccountTransferRequest)
    return transfer_data


@pytest.fixture
def create_deposit_data():
    deposit_data = RandomModelGenerator.generate(AccountDepositRequest)
    return deposit_data
