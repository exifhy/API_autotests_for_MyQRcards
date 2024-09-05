from dataclasses import dataclass


@dataclass
class User:
    name: str = None
    surname: str = None
    email: str = None
    phone: str = None
