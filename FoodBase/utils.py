from secrets import token_urlsafe


def generate_token(length=16):
    return token_urlsafe(length)
