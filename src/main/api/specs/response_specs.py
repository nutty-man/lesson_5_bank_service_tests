from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    @staticmethod
    def check_status(expected_status: HTTPStatus):
        def confirm(response: Response):
            assert response.status_code == expected_status, (
                f"Ожидался статус {expected_status}, "
                f"получен {response.status_code}"
            )

        return confirm
