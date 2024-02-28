from tabulate import tabulate
from data import database, GROUPS_N, GRADES_N, STUDENTS_N, SUBJECTS, LECTURERS_N
from my_select import QUERYS
from fill_grades import create_grades
from fill_groups import create_groups
from fill_lecturer import create_lecturers
from fill_subjects import create_subjects
from fill_students import create_students


def insert_data_to_db():
    create_groups(GROUPS_N)
    create_students(STUDENTS_N)
    create_lecturers(LECTURERS_N)
    create_subjects(SUBJECTS)
    create_grades(GRADES_N)


if __name__ == "__main__":
    choice_1 = input(f"Do you want to fill {database} with data? (Y/N)")
    if choice_1.lower() in ['yes', 'true', 'y']:
        insert_data_to_db()
        print(f"Inserted data into the {database}.")

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
    while True:
        choice_2 = input("Choose number of query: ")
        if choice_2 in QUERYS.keys():
            results = QUERYS[choice_2][0]
            if results:
                print(tabulate(results, tablefmt="grid"))
            else:
                print("No results.")
        else:
            print(
                "\nYou have entered an incorrect inquiry number. Enter a value from 1 to 10.")
