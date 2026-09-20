from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    @staticmethod
    def validate_status(
        response: Response,
        expected_status: int | HTTPStatus
    ) -> None:
        assert response.status_code == int(expected_status), (
            f"Ожидаемый статус: {int(expected_status)}, "
            f"полученный {response.status_code}. Response: {response.text}"
        )
