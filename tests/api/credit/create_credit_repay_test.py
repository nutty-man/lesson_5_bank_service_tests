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

from main.db.repositories.account_repository import AccountRepository
from main.db.repositories.credit_repository import CreditRepository
from main.utils.enums.role import Role
from tests.fixtures.account import create_credit_repay_data


@pytest.mark.api
class TestCreateRepayCredit:

    @allure.story("Погашение кредита")
    @allure.title("Успешное Погашение кредита пользователем")
    def test_create_repay_credit(self, api_manager: ApiManager,
                                 created_credit_account,
                                 created_credit,
                                 create_credit_repay_data: CreateCreditRepayRequest,
                                 account_repository: AccountRepository):
        repay_data = create_credit_repay_data.model_copy(
            update={'accountId': created_credit.id,
                    'creditId': created_credit.creditId,
                    'amount': created_credit.amount
                    }
        )

        repay_response = api_manager.user_steps.create_credit_repay(repay_data)

        assert repay_response.status_code == HTTPStatus.OK, \
            (f'Полученный статус= {repay_response.status_code}, '
             f'отличается от 200 ok')

        repay_response = CreateCreditRepayResponse.model_validate(repay_response.json())

        assert repay_response.creditId == repay_data.creditId, \
            (f'ID кредита= {repay_data.creditId},'
             f' отличается от кредита в response= {repay_response.creditId}')

        assert repay_response.amountDeposited == repay_data.amount, \
            (f'Баланс после погашения кредита= {repay_data.amount},'
             f' отличается от суммы выдачи кредита= {repay_response.amountDeposited}')

    @allure.story("Погашение кредита")
    @allure.title("Неверное тело запроса")
    def test_credit_repay_to_account_invalid_body(self, api_manager: ApiManager,
                                                  created_credit_account,
                                                  create_credit_repay_data: CreateCreditRepayRequest,
                                                  create_credit_data: CreateCreditRequest):
        repay_data = create_credit_repay_data.model_copy(
            update={'accountId': 'invalid_id'
                    }
        )

        response = api_manager.user_steps.create_credit_repay(repay_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Ожидался статус {HTTPStatus.BAD_REQUEST}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @pytest.mark.xfail(
        reason="BUG: при попытке погасить кредит неверным пользователем API возвращает 404 вместо 403",
        strict=True
    )
    @allure.story("Погашение кредита")
    @allure.title("Кредит не принадлежит пользователю")
    def test_credit_repay_to_account_forbidden(self, api_manager: ApiManager,
                                               admin_credentials,
                                               create_deposit_data: AccountDepositRequest,
                                               created_credit,
                                               create_credit_repay_data: CreateCreditRepayRequest):
        api_manager.authenticate(admin_credentials)

        user_data = RandomModelGenerator.generate(CreateUserRequest)

        user_data = user_data.model_copy(
            update={"role": Role.CREDIT_SECRET}
        )

        user_credentials = LoginUserRequest(
            username=user_data.username,
            password=user_data.password
        )

        new_user = api_manager.admin_steps.create_user(user_data)

        assert new_user.status_code == HTTPStatus.OK, (
            f'Полученный статус {new_user.status_code}, '
            f'ожидался {HTTPStatus.OK}.'
        )

        api_manager.authenticate(user_credentials)

        account_response = api_manager.user_steps.create_account()

        assert account_response.status_code == HTTPStatus.CREATED, (
            f'Полученный статус {account_response.status_code}, '
            f'ожидался {HTTPStatus.CREATED}.'
        )

        new_account = CreateAccountResponse.model_validate(account_response.json())

        deposit_data = create_deposit_data.model_copy(
            update={
                'accountId': new_account.id
            }
        )

        summa = 0

        while summa < created_credit.amount:
            response = api_manager.user_steps.deposit_to_account(deposit_data)

            assert response.status_code == HTTPStatus.OK, (
                f'Полученный статус {response.status_code}, '
                f'ожидался {HTTPStatus.OK}.'
            )

            summa += deposit_data.amount

        repay_data = create_credit_repay_data.model_copy(
            update={'accountId': new_account.id,
                    'creditId': created_credit.creditId,
                    'amount': created_credit.amount
                    }
        )

        response = api_manager.user_steps.create_credit_repay(repay_data)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Ожидался статус {HTTPStatus.FORBIDDEN}, '
            f'получен {response.status_code}')

    @allure.story("Погашение кредита")
    @allure.title("Кредит не найден")
    def test_no_credit_id(self, api_manager: ApiManager,
                          created_credit,
                          create_credit_repay_data: CreateCreditRepayRequest,
                          credit_repository: CreditRepository):

        while True:
            candidate_id = random.randint(1, 9999)
            credit_from_db = credit_repository.get_credit_by_id(candidate_id)

            if credit_from_db is None:
                break

        repay_data = create_credit_repay_data.model_copy(
            update={'accountId': created_credit.id,
                    'creditId': candidate_id,
                    'amount': created_credit.amount
                    }
        )

        repay_response = api_manager.user_steps.create_credit_repay(repay_data)

        assert repay_response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Полученный статус= {repay_response.status_code}, '
             f'отличается от 404 NOT_FOUND')

        response_body = repay_response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Погашение кредита")
    @allure.title("Недостаточная сумма погашения кредита")
    def test_create_credit_repay_with_insufficient_amount(self,
                                                          api_manager: ApiManager,
                                                          created_credit_account,
                                                          created_credit,
                                                          create_credit_repay_data: CreateCreditRepayRequest):

        repay_data = create_credit_repay_data.model_copy(
            update={'accountId': created_credit.id,
                    'creditId': created_credit.creditId,
                    'amount': created_credit.amount - 1
                    }
        )

        repay_response = api_manager.user_steps.create_credit_repay(repay_data)

        assert repay_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            f'Ожидался статус {HTTPStatus.UNPROCESSABLE_ENTITY}, '
            f'получен {repay_response.status_code}')

        response_body = repay_response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Погашение кредита")
    @allure.title("Сумма погашения кредита превышает остаток долга по кредиту")
    def test_create_credit_repay_amount_exceeds_debt(self,
                                                          api_manager: ApiManager,
                                                          created_credit_account,
                                                          created_credit,
                                                          create_deposit_data: AccountDepositRequest,
                                                          create_credit_repay_data: CreateCreditRepayRequest):
        deposit_data = create_deposit_data.model_copy(
            update={
                'accountId': created_credit.id
            }
        )

        response = api_manager.user_steps.deposit_to_account(deposit_data)

        assert response.status_code == HTTPStatus.OK, (
            f'Полученный статус {response.status_code}, '
            f'ожидался {HTTPStatus.OK}.'
        )

        repay_data = create_credit_repay_data.model_copy(
            update={'accountId': created_credit.id,
                    'creditId': created_credit.creditId,
                    'amount': created_credit.amount + 1
                    }
        )

        repay_response = api_manager.user_steps.create_credit_repay(repay_data)

        assert repay_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            f'Ожидался статус {HTTPStatus.UNPROCESSABLE_ENTITY}, '
            f'получен {repay_response.status_code}')

        response_body = repay_response.json()

        assert "error" in response_body
        assert response_body["error"]
