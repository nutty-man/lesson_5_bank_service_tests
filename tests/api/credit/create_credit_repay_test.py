from http import HTTPStatus

import pytest
import allure
import random
from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.schemas.dto.response.credit.create_credit_repay_response import CreateCreditRepayResponse
from collections.abc import Callable

from main.api.schemas.dto.response.credit.create_credit_response import CreateCreditResponse
from main.db.repositories.credit_repository import CreditRepository
from main.utils.enums.role import Role
from tests.fixtures.account import create_credit_repay_data


@pytest.mark.api
class TestCreateRepayCredit:

    @allure.story("Погашение кредита")
    @allure.title("Успешное погашение кредита пользователем")
    def test_create_repay_credit(self, api_manager: ApiManager,
                                 created_credit_account,
                                 created_credit,
                                 credit_repay_data_factory: Callable[..., CreateCreditRepayRequest]):
        repay_data = credit_repay_data_factory(
            accountId=created_credit.id,
            creditId=created_credit.creditId,
            amount=created_credit.amount
        )

        repay_response = api_manager.user_steps.create_credit_repay_validated(repay_data)

        assert repay_response.creditId == repay_data.creditId, \
            (f'ID кредита= {repay_data.creditId},'
             f' отличается от кредита в response= {repay_response.creditId}')

        assert repay_response.amountDeposited == repay_data.amount, \
            (f'Баланс после погашения кредита= {repay_data.amount},'
             f' отличается от суммы выдачи кредита= {repay_response.amountDeposited}')

    @allure.story("Погашение кредита")
    @allure.title("Неверное тело запроса")
    def test_credit_repay_to_account_invalid_body(
            self,
            api_manager: ApiManager,
            created_credit_account,
            credit_repay_data_factory: Callable[..., CreateCreditRepayRequest]):
        repay_data = credit_repay_data_factory(accountId='invalid_id')

        response = api_manager.user_steps.create_credit_repay(repay_data, HTTPStatus.BAD_REQUEST)

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @pytest.mark.xfail(
        reason="BUG: при попытке погасить кредит неверным пользователем API возвращает 404 вместо 403",
        strict=True
    )
    @allure.story("Погашение кредита")
    @allure.title("Кредит не принадлежит пользователю")
    def test_credit_repay_to_account_forbidden(
            self,
            api_manager: ApiManager,
            create_credit_user_with_second_account: CreateAccountResponse,
            created_credit: CreateCreditResponse,
            credit_repay_data_factory: Callable[..., CreateCreditRepayRequest]):
        repay_data = credit_repay_data_factory(
            accountId=create_credit_user_with_second_account.id,
            creditId=created_credit.creditId,
            amount=created_credit.amount,
        )

        response = api_manager.user_steps.create_credit_repay(
            repay_data,
            HTTPStatus.FORBIDDEN,
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Погашение кредита")
    @allure.title("Кредит не найден")
    def test_no_credit_id(self, api_manager: ApiManager,
                          created_credit,
                          nonexistent_id: Callable[
                              [Callable[[int], object | None], int, int], int,],
                          credit_repay_data_factory: Callable[..., CreateCreditRepayRequest],
                          credit_repository: CreditRepository):
        repay_data = credit_repay_data_factory(
            accountId=created_credit.id,
            creditId=nonexistent_id(
                credit_repository.get_credit_by_id,
                1,
                9999,
            ),
            amount=created_credit.amount

        )
        repay_response = api_manager.user_steps.create_credit_repay(repay_data, HTTPStatus.NOT_FOUND)

        response_body = repay_response.json()

        assert "error" in response_body
        assert response_body["error"]

    @pytest.mark.parametrize(
        "repay_amount",
        [
            pytest.param(-1, id="insufficient_amount"),
            pytest.param(1, id="extra_amount"),
        ],
        indirect=True,
    )
    @allure.story("Погашение кредита")
    @allure.title("Некорректная сумма погашения кредита")
    def test_create_credit_repay_invalid_amount(
            self,
            api_manager: ApiManager,
            created_credit: CreateCreditResponse,
            repay_amount: float,
            credit_repay_data_factory: Callable[..., CreateCreditRepayRequest],
    ):
        repay_data = credit_repay_data_factory(
            accountId=created_credit.id,
            creditId=created_credit.creditId,
            amount=repay_amount,
        )

        response = api_manager.user_steps.create_credit_repay(
            repay_data,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]
