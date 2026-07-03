from dataclasses import dataclass


@dataclass
class User:
    name: str = None
    surname: str = None
    email: str = None
    phone: str = None
    username: str = None


@dataclass
class Company:
    name: str = None
    email: str = None
    phone: str = None


@dataclass
class Contract:
    name: str = None
    new_name: str = None
    date_from: str = None
    date_yesterday: str = None
    description: str = None
    new_description: str = None
    conditions: str = None
    new_conditions: str = None
