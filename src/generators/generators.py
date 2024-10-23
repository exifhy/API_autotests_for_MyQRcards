from faker import Faker
from src.data.data import User, Company, Contract
from random import randint
from datetime import datetime, timedelta


fake_ru = Faker('ru_Ru')
fake_en = Faker('en_US')


def generated_user():

    yield User(
        name=fake_ru.first_name_male(),
        surname=fake_ru.last_name_male(),
        email=fake_en.email(domain='autotest.org'),
        phone=f'+7{randint(1000000000, 7999999999)}',
        username=fake_en.user_name()
    )


def generator_company():

    yield Company(
        name=fake_ru.company(),
        email=fake_en.email(domain='autotest.org'),
        phone=f'+7{randint(1000000000, 7999999999)}'
    )


def generator_contract():

    current_date = datetime.now()
    yesterday = current_date - timedelta(1)

    yield Contract(
        name=f'Договор номер: {randint(1, 999)}',
        new_name=f'Обновленный номер договора: {randint(1000, 9999)}',
        date_from=current_date.strftime("%Y-%m-%dT00:00:00"),
        date_yesterday=yesterday.strftime("%Y-%m-%dT00:00:00"),
        conditions=fake_ru.text(max_nb_chars=80),
        new_conditions=fake_ru.text(max_nb_chars=60),
        description=fake_ru.text(max_nb_chars=40),
        new_description=fake_ru.text(max_nb_chars=50)
    )
