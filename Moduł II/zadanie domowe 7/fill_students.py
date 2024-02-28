import faker
from random import randint
from connect import session
from models import Student
from data import GROUPS_N


def generate_fake_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append(f.name())
    return fake_data


def create_data(data) -> None:
    for students in data:
        fake_students = Student(name=students[0], group_id=students[1])
        session.add(fake_students)
    session.commit()


def create_students(numbers):
    create_data(generate_fake_data(numbers))
