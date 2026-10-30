from http import HTTPStatus

import pytest
import allure

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.response.credit.create_credit_response import CreateCreditResponse
from main.api.specs.request_specs import RequestSpecs
from main.utils.calc_utils.utils import find_credit_by_id


@pytest.mark.api
class TestCreditHistory:

    @allure.story("Получение истории кредитов для указанного счета")
    @allure.title("Успешное получение истории кредитов для указанного счета")
    def test_get_credit_history(self,
                                api_manager: ApiManager,
                                repaid_credit: CreateCreditResponse):
        credit_history = api_manager.user_steps.get_credit_history_validated()

        credit = find_credit_by_id(
            credit_history.credits,
            repaid_credit.creditId,
        )

        assert credit is not None, "Кредит не найден в истории"

        assert credit.amount == repaid_credit.amount, \
            (f'Полученная сумма= {credit.amount} '
             f'не соответствует ожидаемой= {repaid_credit.amount}')
        assert credit.termMonths == repaid_credit.termMonths, \
            (f'Полученный период= {credit.termMonths} '
             f'не соответствует ожидаемому= {repaid_credit.termMonths}')
        assert credit.balance == 0, \
            (f'Баланс не равен 0.0 после погашения кредита, '
             f'полученный баланс= {credit.balance}')
        assert credit.accountId == repaid_credit.id, \
            (f'Полученный accountId= {credit.accountId} '
             f'не соответствует ожидаемому= {repaid_credit.id}')


    @pytest.mark.xfail(
        reason="BUG: при попытке получить историю кредитов"
               " не авторизованным пользователем API возвращает 401 вместо 403",
        strict=True,
    )
    @allure.story("Получение истории кредитов для указанного счета")
    @allure.title("Пользователь не авторизован")
    def test_get_credit_history_unauth(
            self,
            api_manager: ApiManager,
            created_credit: CreateCreditResponse,
    ):
        response = api_manager.user_steps.get_credit_history(
            HTTPStatus.FORBIDDEN,
            headers=RequestSpecs.unauth_headers(),
        )

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"] == HTTPStatus.FORBIDDEN
