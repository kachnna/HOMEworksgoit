from datetime import datetime
from random import randint
from sqlite3 import Error
from data import SUBJECTS_N, STUDENTS_N


def prepare_date(number) -> tuple:
    for_data = []

    for i in range(number):
        if i < 0.5 * number:
            create_date = datetime(2022, randint(
                10, 12), randint(1, 28)).date()
        else:
            create_date = datetime(2023, randint(1, 6), randint(1, 28)).date()
        for id_student in range(1, STUDENTS_N + 1):
            for_data.append((randint(1, 5), id_student, randint(
                1, SUBJECTS_N), create_date))
    return for_data


def create_data(conn, data) -> None:
    sql = '''
    INSERT INTO grades(grades, student_id, subject_id, created_at) VALUES(?,?,?,?);
    '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, data)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def create_grades(conn, number):
    create_data(conn, prepare_date(number))


