from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.schemas.dto.response.credit.create_credit_response import CreateCreditResponse
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.db.repositories.credit_repository import CreditRepository


@pytest.fixture
def credit_repository(db_session: Session):
    return CreditRepository(db_session)


@pytest.fixture
def created_credit_account(
        created_credit_user: CreateUserResponse,
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

    account = CreateAccountResponse.model_validate(response.json())

    assert account.balance == 0

    return account


@pytest.fixture
def created_credit(api_manager: ApiManager,
                   created_credit_account,
                   create_credit_data: CreateCreditRequest):
    data = create_credit_data.model_copy(
        update={"accountId": created_credit_account.id}
    )

    response = api_manager.user_steps.create_credit(data)

    assert response.status_code == HTTPStatus.CREATED, \
        (f'Полученный статус= {response.status_code}, '
         f'отличается от 201 created')

    response = CreateCreditResponse.model_validate(response.json())

    return response
