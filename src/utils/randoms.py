import random
import string


def rand_word(prefix: str, n: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return f"{prefix}_{''.join(random.choice(alphabet) for _ in range(n))}"


def rand_email(domain: str = "tt.tt") -> str:
    return f"{rand_word('at', 10)}@{domain}"


def rand_phone_ru8() -> str:
    return "8" + "".join(random.choice(string.digits) for _ in range(10))


def rand_name(prefix: str = "AT") -> str:
    return rand_word(prefix, 6)


def rand_hex_color() -> str:
    return "".join(random.choice("0123456789abcdef") for _ in range(6))
