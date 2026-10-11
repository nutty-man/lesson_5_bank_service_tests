from collections.abc import Callable
from http import HTTPStatus

import pytest
import allure
from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.response.credit.create_credit_response import CreateCreditResponse
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestCreateCredit:

    @allure.story("Получение кредита")
    @allure.title("Успешное получение кредита пользователем")
    def test_create_credit(self, api_manager: ApiManager,
                           created_credit_account,
                           credit_data_factory: Callable[..., CreateCreditRequest],
                           account_repository: AccountRepository):
        data = credit_data_factory(accountId=created_credit_account.id)

        response = api_manager.user_steps.create_credit_validated(data)

        assert response.id == created_credit_account.id, \
            (f'ID созданного счёта= {created_credit_account.id},'
             f' отличается от ID счёта в response= {response.id}')

        assert response.amount == data.amount, \
            (f'Баланс после выдачи кредита= {data.amount},'
             f' отличается от суммы выдачи кредита= {response.amount}')

        assert response.termMonths == data.termMonths, \
            (f'Ожидаемый срок кредита: {data.termMonths} мес., '
             f'полученный: {response.termMonths} мес.')

        account_from_db = account_repository.get_account_by_id(created_credit_account.id)

        assert account_from_db.balance == data.amount, \
            (f'Полученный баланс некорректен, ожидался = {data.amount}'
             f' баланс счёта= {account_from_db.balance}')

    @allure.story("Получение кредита")
    @allure.title("Некорректные данные в запросе")
    def test_credit_to_account_invalid_body(self, api_manager: ApiManager,
                                            created_credit_account,
                                            credit_data_factory: Callable[..., CreateCreditRequest]):
        data = credit_data_factory(accountId="invalid_id")

        response = api_manager.user_steps.create_credit(data, HTTPStatus.BAD_REQUEST)

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Получение кредита")
    @allure.title("Нет прав взять кредит")
    def test_credit_to_account_forbidden(
            self,
            api_manager: ApiManager,
            create_credit_data: CreateCreditRequest,
    ):
        api_manager.user_steps.create_credit(
            create_credit_data, HTTPStatus.FORBIDDEN
        )

    @pytest.mark.xfail(
        reason="BUG: при повторной попытке взять активный кредит API возвращает 404 вместо 403",
        strict=True,
    )
    @allure.story("Получение кредита")
    @allure.title("Уже есть активный кредит на этот или другой счет")
    def test_create_credit_with_active_credit(
            self,
            api_manager: ApiManager,
            created_credit: CreateCreditResponse,
            credit_data_factory: Callable[..., CreateCreditRequest],
    ):
        data = credit_data_factory(accountId=created_credit.id)

        response = api_manager.user_steps.create_credit(
            data, HTTPStatus.FORBIDDEN
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Получение кредита")
    @allure.title("Указанный id счета не найден")
    def test_no_account_id_for_credit(
            self,
            api_manager: ApiManager,
            created_credit_account,
            nonexistent_id: Callable[
                [Callable[[int], object | None], int, int], int,],
            account_repository: AccountRepository,
            credit_data_factory: Callable[..., CreateCreditRequest],
    ):
        data = credit_data_factory(
            accountId=nonexistent_id(account_repository.get_account_by_id, 1, 9999)
        )

        response = api_manager.user_steps.create_credit(
            data, HTTPStatus.NOT_FOUND
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @pytest.mark.xfail(
        reason="BUG: при невалидной сумме кредита API возвращает 400 вместо 422",
        strict=True,
    )
    @allure.story("Получение кредита")
    @allure.title("Невалидная сумма по кредиту")
    @pytest.mark.parametrize("amount", [4999, 15001])
    def test_credit_to_account_invalid_amount(
            self,
            api_manager: ApiManager,
            created_credit_account,
            credit_data_factory: Callable[..., CreateCreditRequest],
            amount: int,
    ):
        data = credit_data_factory(
            amount=amount,
            accountId=created_credit_account.id,
        )

        response = api_manager.user_steps.create_credit(
            data, HTTPStatus.UNPROCESSABLE_ENTITY
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]
