from random import randint
from connect import session
from models import Subject
from data import LECTURERS_N


def prepare_date(subjects: list) -> list:
    for_data = []
    for i in range(len(subjects)):
        for_data.append((subjects[i], randint(1, LECTURERS_N)))
    return for_data


def create_data(data) -> None:
    for subjects in data:
        subjects_name, lecturer_id = subjects
        fake_subject = Subject(name=subjects_name, lecturer_id=lecturer_id)
    session.add(fake_subject)
    session.commit()


def create_subjects(subjects):
    create_data(prepare_date(subjects))
