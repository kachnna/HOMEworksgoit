import faker
from random import randint
from sqlite3 import Error
from data import GROUPS_N


def generate_fake_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append(f.name())
    return fake_data


def prepare_date(data) -> tuple:
    for_data = []
    for i in data:
        for_data.append((i, randint(1, GROUPS_N)))
    return for_data


def create_data(conn, data) -> None:
    sql = '''
    INSERT INTO students(name, group_id) VALUES(?,?);
    '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, data)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def create_students(conn, numbers):
    create_data(conn, prepare_date(generate_fake_data(numbers)))
