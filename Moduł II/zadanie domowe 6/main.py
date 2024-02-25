import sqlite3
from tabulate import tabulate
from connect import create_connection
from data import database, GROUPS_N, GRADES_N, STUDENTS_N, SUBJECTS, LECTURERS_N, QUERYS
from fill_grades import create_grades
from fill_groups import create_groups
from fill_lecturer import create_lecturers
from fill_subjects import create_subjects
from fill_students import create_students


def create_db(conn):
    with open('school.sql', 'r') as f:
        sql = f.read()
    with sqlite3.connect(database) as con:
        cur = con.cursor()
        cur.executescript(sql)


def insert_data_to_db(conn):
    create_groups(conn, GROUPS_N)
    create_students(conn, STUDENTS_N)
    create_lecturers(conn, LECTURERS_N)
    create_subjects(conn, SUBJECTS)
    create_grades(conn, GRADES_N)


def get_query(conn, sql_query):
    with open(sql_query, 'r') as q:
        query = q.read()
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()


if __name__ == "__main__":
    with create_connection(database) as conn:
        if conn is not None:
            create_db(conn)
            print(f"I have connection with file {database}.")
            insert_data_to_db(conn)
            print(f"Inserted data into the {database}.")
        else:
            print("I cannot create the database connection.")
        print("""
                    Query 1: 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów.
                    Query 2: Uczeń z najwyższą średnią ocen z wybranego przedmiotu.
                    Query 3: Średnia ocen w grupach dla wybranego przedmiotu.
                    Query 4: Średnia ocen dla wszystkich grup, uwzględniając wszystkie oceny.
                    Query 5: Przedmioty, które prowadzi wybrany wykładowca.
                    Query 6: Lista uczniów w wybranej grupie.
                    Query 7: Oceny uczniów w wybranej grupie z określonego przedmiotu.
                    Query 8: Średnia ocen wystawionych przez wykładowcę z danego przedmiotu.
                    Query 9: Lista kursów, na które uczęszcza uczeń.
                    Query 10: Lista kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia.
                    """)
        while (True):
            choice = input("Choose number of guery: ")
            if choice in QUERYS.keys():
                print(f"\n{QUERYS[choice][1]}\n")
                results = get_query(conn, QUERYS[choice][0])
                if results:
                    print(tabulate(results, tablefmt="grid"))
                else:
                    print("No results.")
            else:
                print(
                    "\nYou have entered an incorrect inquiry number. Enter a value from 1 to 10.")
