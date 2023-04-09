import connect
from models import Users
from random import choice

from faker import Faker

fake = Faker("uk-UA")


def upload_contacts(number_users):
    for i in range(number_users):
        user = Users(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_mode=choice(['sms', 'email'])
        )
        user.save()


if __name__ == '__main__':
    upload_contacts(10)
