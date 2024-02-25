from sqlite3 import Error
import random


def generate_data(numbers) -> list:
    components = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Theta',
                  'Math', 'Science', 'Physics', 'Chemistry', 'Biology', 'Literature',
                  'History', 'Geography', 'Art', 'Music', 'Drama', 'Computer',
                  'Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink',
                  'Lions', 'Tigers', 'Bears', 'Wolves', 'Eagles', 'Falcons', 'Owls']

    fake_groups = []
    for _ in range(numbers):
        group_name = ' '.join(random.sample(components, random.randint(2, 3)))
        fake_groups.append(group_name)
    return fake_groups


def prepare_date(groups) -> tuple:
    for_groups = []
    for group in groups:
        for_groups.append((group,))
    return for_groups


def create_data(conn, groups) -> None:
    sql = '''
    INSERT INTO groups(name) VALUES(?);
    '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, groups)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def create_groups(conn, numbers):
    create_data(conn, prepare_date(generate_data(numbers)))


if __name__ == "__main__":
    print(prepare_date(generate_data(3)))
