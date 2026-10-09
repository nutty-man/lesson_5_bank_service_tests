from collections.abc import Callable
from http import HTTPStatus

import pytest
import random
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.context.transaction_history_context import TransactionHistoryContext
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.db.repositories.account_repository import AccountRepository
from main.utils.calc_utils.utils import get_candidate_id


@pytest.fixture
def prepared_transaction_history(
    api_manager: ApiManager,
    created_account: CreateAccountResponse,
    create_deposit_data: AccountDepositRequest,
    account_transfer_data: AccountTransferRequest,
) -> TransactionHistoryContext:

    deposit_data = create_deposit_data.model_copy(
        update={"accountId": created_account.id}
    )

    api_manager.user_steps.deposit_to_account_validated(deposit_data)

    second_account = api_manager.user_steps.create_account_validated()

    data = account_transfer_data.model_copy(
        update={"fromAccountId": created_account.id,
                "toAccountId": second_account.id,
                "amount": random.uniform(500, deposit_data.amount - 1)}
    )

    api_manager.user_steps.transfer_to_account_validated(data)

    return TransactionHistoryContext(
        account=created_account,
        expected_balance=deposit_data.amount - data.amount,
    )

@pytest.fixture
def nonexistent_account_id(account_repository: AccountRepository):
    def generate(min_id: int, max_id: int) -> int:
        return get_candidate_id(
            find_by_id=account_repository.get_account_by_id,
            min_id=min_id,
            max_id=max_id,
        )

    return generate

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

    return api_manager.user_steps.create_account_validated()

@pytest.fixture
def account_transfer_data():
    transfer_data = RandomModelGenerator.generate(AccountTransferRequest)
    return transfer_data


@pytest.fixture
def create_deposit_data():
    deposit_data = RandomModelGenerator.generate(AccountDepositRequest)
    return deposit_data

@pytest.fixture
def create_credit_data():
    credit_data = RandomModelGenerator.generate(CreateCreditRequest)
    return credit_data

@pytest.fixture
def create_credit_repay_data():
    credit_repay_data = RandomModelGenerator.generate(CreateCreditRepayRequest)
    return credit_repay_data

@pytest.fixture
def deposit_data_factory(
    create_deposit_data: AccountDepositRequest,
) -> Callable[[int | str], AccountDepositRequest]:
    def build(account_id: int | str) -> AccountDepositRequest:
        return create_deposit_data.model_copy(
            update={"accountId": account_id}
        )
    return build

@pytest.fixture
def transfer_data_factory(
    account_transfer_data: AccountTransferRequest,
) -> Callable[..., AccountTransferRequest]:

    def build(**updates) -> AccountTransferRequest:
        return account_transfer_data.model_copy(update=updates)

    return build

@pytest.fixture
def user_with_two_accounts(
    api_manager: ApiManager,
    created_user,
    create_user_request: CreateUserRequest,
) -> tuple[CreateAccountResponse, CreateAccountResponse]:
    credentials = LoginUserRequest(
        username=create_user_request.username,
        password=create_user_request.password,
    )

    api_manager.authenticate(credentials)

    first_account = api_manager.user_steps.create_account_validated()
    second_account = api_manager.user_steps.create_account_validated()

    return first_account, second_account

@pytest.fixture
def funded_accounts(
    api_manager: ApiManager,
    user_with_two_accounts: tuple[
        CreateAccountResponse, CreateAccountResponse
    ],
    deposit_data_factory: Callable[[int | str], AccountDepositRequest],
) -> tuple[CreateAccountResponse, CreateAccountResponse, float]:

    first_account, second_account = user_with_two_accounts

    deposit_data = deposit_data_factory(first_account.id)
    api_manager.user_steps.deposit_to_account_validated(deposit_data)

    return first_account, second_account, deposit_data.amount
