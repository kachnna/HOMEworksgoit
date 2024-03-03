from datetime import datetime
from random import randint
from connect import session
from models import Grade
from data import SUBJECTS_N, STUDENTS_N


def prepare_data(number) -> list:
    for_data = []

    for i in range(number):
        if i < 0.5 * number:
            created_at = datetime(2022, randint(
                10, 12), randint(1, 28)).date()
        else:
            created_at = datetime(2023, randint(1, 6), randint(1, 28)).date()
        for id_student in range(1, STUDENTS_N + 1):
            for_data.append((randint(1, 5), id_student, randint(
                1, SUBJECTS_N), created_at))
    return for_data


def create_data(data) -> None:
    for grades_fake in data:
        fake_grades = Grade(
            grade=grades_fake[0], student_id=grades_fake[1], subject_id=grades_fake[2], created_at=grades_fake[3])
        session.add(fake_grades)
    session.commit()


def create_grades(number):
    create_data(prepare_data(number))


if __name__ == "__main__":
    print(prepare_data(6))
