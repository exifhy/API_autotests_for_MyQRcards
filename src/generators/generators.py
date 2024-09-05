from faker import Faker
from src.data.data import User
from random import randint


fake_ru = Faker('ru_Ru')
fake_en = Faker('en_US')


def generated_user():

    yield User(
        name=fake_ru.first_name_male(),
        surname=fake_ru.last_name_male(),
        email=fake_en.email(domain='autotest.org'),
        phone=f'+7{randint(1000000000, 7999999999)}'
    )
