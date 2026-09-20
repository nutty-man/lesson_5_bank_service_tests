import pytest
from main.api.classes.api_manager import ApiManager
from main.db.repositories.account_repository import AccountRepository
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                            account_repository: AccountRepository):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = account_repository.get_account_by_id(response.id)

        assert account_from_db.id == response.id, (f'Аккаунт не создан, id аккаунта нет в DB,'
                                                   f'полученный id = {response.id}')
        assert account_from_db.balance is not None, (f'Поле баланса отсутствует в БД, '
                                                     f'баланс счёта= {account_from_db.balance}')



