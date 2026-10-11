from collections.abc import Callable
from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.schemas.dto.response.credit.create_credit_response import CreateCreditResponse
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.db.repositories.credit_repository import CreditRepository
from main.utils.enums.role import Role


@pytest.fixture
def credit_repository(db_session: Session):
    return CreditRepository(db_session)

@pytest.fixture
def repay_amount(
    request,
    created_credit: CreateCreditResponse,
) -> float:
    return created_credit.amount + request.param

@pytest.fixture
def created_credit_account(
        created_credit_user: CreateUserResponse,
        create_user_request: CreateUserRequest,
        api_manager: ApiManager,
) -> CreateAccountResponse:
    user_credentials = LoginUserRequest(
        username=create_user_request.username,
        password=create_user_request.password,
    )

    api_manager.authenticate(user_credentials)

    return api_manager.user_steps.create_account_validated()


@pytest.fixture
def created_credit(
        api_manager: ApiManager,
        created_credit_account: CreateAccountResponse,
        credit_data_factory: Callable[..., CreateCreditRequest],
) -> CreateCreditResponse:
    data = credit_data_factory(accountId=created_credit_account.id)

    return api_manager.user_steps.create_credit_validated(data)


@pytest.fixture
def credit_data_factory(
        create_credit_data: CreateCreditRequest,
) -> Callable[..., CreateCreditRequest]:
    def build(**updates) -> CreateCreditRequest:
        return create_credit_data.model_copy(update=updates)

    return build


@pytest.fixture
def credit_repay_data_factory(
        create_credit_repay_data: CreateCreditRepayRequest,
) -> Callable[..., CreateCreditRepayRequest]:
    def build(**updates) -> CreateCreditRepayRequest:
        return create_credit_repay_data.model_copy(update=updates)

    return build

@pytest.fixture
def repaid_credit(
    api_manager: ApiManager,
    created_credit: CreateCreditResponse,
    credit_repay_data_factory: Callable[..., CreateCreditRepayRequest],
) -> CreateCreditResponse:
    repay_data = credit_repay_data_factory(
        accountId=created_credit.id,
        creditId=created_credit.creditId,
        amount=created_credit.amount,
    )

    api_manager.user_steps.create_credit_repay_validated(repay_data)

    return created_credit

@pytest.fixture
def create_credit_user_with_second_account(
        api_manager: ApiManager,
        admin_credentials,
        user_factory: Callable[..., CreateUserResponse],
        deposit_data_factory: Callable[[int | str], AccountDepositRequest],
        created_credit: CreateCreditResponse
):

    api_manager.authenticate(admin_credentials)

    user_data = RandomModelGenerator.generate(CreateUserRequest)

    user_factory(
        role=Role.CREDIT_SECRET,
        user_data=user_data,
    )

    credentials = LoginUserRequest(
        username=user_data.username,
        password=user_data.password,
    )

    api_manager.authenticate(credentials)

    account = api_manager.user_steps.create_account_validated()

    deposit_data = deposit_data_factory(account.id)

    deposited_amount = 0

    while deposited_amount < created_credit.amount:
        api_manager.user_steps.deposit_to_account_validated(deposit_data)
        deposited_amount += deposit_data.amount

    return account
