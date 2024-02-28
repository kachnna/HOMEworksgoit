from random import randint
from connect import session
from models import Subject
from data import LECTURERS_N, SUBJECTS


def prepare_data(subjects: list) -> list:
    for_data = []
    for i in range(len(subjects)):
        for_data.append((subjects[i], randint(1, LECTURERS_N)))
    return for_data


def create_data(data) -> None:
    for subjects in data:
        fake_subject = Subject(name=subjects[0], lecturer_id=subjects[1])
        session.add(fake_subject)
    session.commit()


def create_subjects(subjects):
    create_data(prepare_data(subjects))


if __name__ == "__main__":
    print(prepare_data(SUBJECTS))
