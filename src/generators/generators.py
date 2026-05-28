from dataclasses import dataclass
from faker import Faker


fake = Faker("ru_RU")


@dataclass
class GeneratedUser:
    email: str
    phone: str
    username: str


def generated_user():
    while True:
        yield GeneratedUser(
            email=fake.email(),
            phone=fake.phone_number(),
            username=fake.user_name(),
        )
