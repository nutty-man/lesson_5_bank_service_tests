from http import HTTPStatus

import pytest
import allure

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest
from main.api.schemas.dto.response.credit.credit_history_response import CreditHistoryResponse
from main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
class TestCreditHistory:

    @allure.story("Получение истории кредитов для указанного счета")
    @allure.title("Успешное получение истории кредитов для указанного счета")
    def test_get_credit_history(self, api_manager: ApiManager,
                                created_credit,
                                create_credit_repay_data: CreateCreditRepayRequest):
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

        credit_history = api_manager.user_steps.get_credit_history()
        assert credit_history.status_code == HTTPStatus.OK, \
            (f'Полученный статус= {credit_history.status_code}, '
             f'отличается от 200 ok')

        credit_history = CreditHistoryResponse.model_validate(credit_history.json())

        for credit in credit_history.credits:
            if credit.creditId == created_credit.creditId:
                assert created_credit.amount == credit.amount, \
                    (f'Полученная сумма= {credit.amount} '
                     f'не соответствует ожидаемой= {created_credit.amount}')
                assert created_credit.termMonths == credit.termMonths, \
                    (f'Полученный период= {credit.termMonths} '
                     f'не соответствует ожидаемому= {created_credit.termMonths}')
                assert credit.balance == 0, \
                (f'Баланс не равен 0.0 после погашения кредита, '
                 f'полученный баланс= {credit.balance}')
                assert credit.accountId == created_credit.id, \
                    (f'Полученный accountId= {credit.accountId} '
                     f'не соответствует ожидаемому= {created_credit.id}')
                break
        else:
            raise AssertionError("Кредит не найден в истории")

    @pytest.mark.xfail(
        reason="BUG: при попытке получить историю кредитов"
               " не авторизованным пользователем API возвращает 401 вместо 403",
        strict=True
    )
    @allure.story("Получение истории кредитов для указанного счета")
    @allure.title("Получение истории кредитов для указанного счета. Пользователь не авторизован")
    def test_get_credit_history(self, api_manager: ApiManager,
                                created_credit):
        response = api_manager.user_steps.get_credit_history(headers=RequestSpecs.unauth_headers())

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Ожидался статус {HTTPStatus.FORBIDDEN}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"] == HTTPStatus.FORBIDDEN

