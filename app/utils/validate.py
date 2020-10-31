import re

valid_email_format = re.compile("^[a-zA-Z0-9+-_.]+@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$")


def validate_email(email: str) -> bool:
    return bool(valid_email_format.match(email))
