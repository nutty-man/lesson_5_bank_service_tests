SENSITIVE_FIELDS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "cookie",
    "set-cookie",
}


def sanitize(data):
    if isinstance(data, dict):
        return {
            key: "***" if key.lower() in SENSITIVE_FIELDS else sanitize(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [sanitize(item) for item in data]

    return data