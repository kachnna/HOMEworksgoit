import faker
from sqlite3 import Error


def generate_fake_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append(f.name())
    return fake_data


def prepare_date(data) -> tuple:
    for_data = []
    for i in data:
        for_data.append((i,))
    return for_data


def create_data(conn, data) -> None:
    sql = '''
    INSERT INTO lecturers(name) VALUES(?);
    '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, data)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def create_lecturers(conn, numbers):
    create_data(conn, prepare_date(generate_fake_data(numbers)))


if __name__ == "__main__":
    print(prepare_date(generate_fake_data(8)))
