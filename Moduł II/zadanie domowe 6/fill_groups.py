from sqlite3 import Error


def generate_data(numbers) -> list:
    fake_groups = []
    for i in range(numbers):
        letter = 'ABCDEFGHIJKLMNOPQRSTUWYZ'
        template_name = f"2022/2023-{letter[i]}"
        fake_groups.append(template_name)
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


