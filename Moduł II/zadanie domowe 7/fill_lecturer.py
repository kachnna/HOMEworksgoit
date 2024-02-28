import faker
from connect import session
from models import Lecturer


def generate_fake_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append(f.name())
    return fake_data


def create_data(data) -> None:
    for lecturers_name in data:
        fake_lecturers = Lecturer(name=lecturers_name)
        session.add(fake_lecturers)
    session.commit()


def create_lecturers(numbers):
    create_data(generate_fake_data(numbers))
