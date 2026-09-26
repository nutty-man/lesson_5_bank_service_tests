import json
import logging
import os

from main.utils.logger.mask import sanitize

logger = logging.getLogger(__name__)

def log_request_and_response(response):
    try:
        request = response.request

        green = "\033[32m"
        red = "\033[31m"
        reset = "\033[0m"

        safe_headers = sanitize(dict(request.headers))

        headers = " \\\n".join(
            f"-H '{header}: {value}'"
            for header, value in safe_headers.items()
        )

        full_test_name = (
            f"pytest "
            f"{os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"
        )

        body = ""

        if request.body:
            raw_body = request.body

            if isinstance(raw_body, bytes):
                raw_body = raw_body.decode("utf-8")

            try:
                parsed_body = json.loads(raw_body)
                safe_body = sanitize(parsed_body)
                body = f"-d '{json.dumps(safe_body, ensure_ascii=False)}' \\\n"
            except (json.JSONDecodeError, TypeError):
                body = "-d '<non-json body>' \\\n"

        logger.info(
            "%s%s%s\n"
            "curl -X %s '%s' \\\n"
            "%s \\\n"
            "%s",
            green,
            full_test_name,
            reset,
            request.method,
            request.url,
            headers,
            body,
        )

        response_data = response.text

        try:
            response_data = sanitize(response.json())
        except ValueError:
            pass

        if response.ok:
            logger.info(
                "RESPONSE: status=%s | data=%s",
                response.status_code,
                response_data,
            )
        else:
            logger.info(
                "RESPONSE: status=%s%s%s | data=%s",
                red,
                response.status_code,
                reset,
                response_data,
            )

    except Exception:
        logger.exception("Request/response logging failed")
