from connect import session
from sqlalchemy import func, select, desc, and_
from models import Student, Subject, Grade, Group


def select_1():
    print("Query 1: 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów.")
    q = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label(
            "Average"), Student.name.label("Name"))
        .join(Student)
        .group_by(Student)
        .order_by(desc("Average"))
        .limit(5)
    ).mappings().all()
    return q


def select_2():
    print("Query 2: Uczeń z najwyższą średnią ocen z wybranego przedmiotu.")
    q = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label(
            "Average"), Student.name.label("Name"))
        .where(Grade.subject_id == 1)
        .join(Student)
        .group_by(Student)
        .order_by(desc("Average"))
    ).first()
    return q


def select_3():
    print("Query 3: Średnia ocen w grupach dla wybranego przedmiotu.")
    q = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label(
            "Average"), Group.name.label("Name"))
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .where(Grade.subject_id == 1)
        .group_by(Group)
        .order_by(desc("Average"))
    ).mappings().all()
    return q


def select_4():
    print("Query 4: Średnia ocen dla wszystkich grup, uwzględniając wszystkie oceny.")
    q = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label(
            "Average"), Group.name.label("Name"))
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .where(Grade.subject_id == 1)
        .group_by(Group)
        .order_by(desc("Average"))
    ).mappings().all()
    return q


def select_5():
    print("Query 5: Przedmioty, które prowadzi wybrany wykładowca.")
    q = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label(
            "Average"), Group.name.label("Name"))
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .group_by(Group)
        .order_by(desc("Average"))
    ).mappings().all()
    return q


def select_6():
    print("Query 6: Lista uczniów w wybranej grupie.")
    q = session.execute(
        select(Student.name.label("Name"))
        .where(Student.group_id == 1)
    ).mappings().all()
    return q


def select_7():
    print("Query 7: Oceny uczniów w wybranej grupie z określonego przedmiotu.")
    q = session.execute(
        select(Grade.grade.label(
            "Assessment"), Student.name.label("Name"))
        .join(Student)
        .where(
            and_(
                Grade.subject_id == 1,
                Student.group_id == 1
            ))
    ).mappings().all()
    return q


def select_8():
    print("Query 8: Średnia ocen wystawionych przez wykładowcę z danego przedmiotu.")
    q = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label(
            "Average"), Subject.name.label("Name"))
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .where(Grade.subject_id.in_(
            select(Subject.id).where(Subject.lecturer_id == 1)
        ))
        .group_by(Grade.subject_id)
        .order_by(desc("Average"))
    ).mappings().all()
    return q


def select_9():
    print("Query 9: Lista kursów, na które uczęszcza uczeń.")
    q = session.execute(
        select(Subject.name.label("Subject"))
        .select_from(Grade)
        .join(Subject)
        .where(Grade.student_id == 1)
        .group_by(Subject)
        .order_by("Subject")
    ).mappings().all()
    return q


def select_10():
    print("Query 10: Lista kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia.")
    q = session.execute(
        select(Subject.name.label("Subject"))
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .where(and_(
            Grade.subject_id.in_(
                select(Subject.id).where(Subject.lecturer_id == 1)
            ),
            Grade.student_id == 1
        ))
        .group_by(Subject)
        .order_by("Subject")
    ).mappings().all()
    return q


QUERYS = {
    "1": [select_1(), "Query 1: 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów."],
    "2": [select_2(), "Query 2: Uczeń z najwyższą średnią ocen z wybranego przedmiotu."],
    "3": [select_3(), "Query 3: Średnia ocen w grupach dla wybranego przedmiotu."],
    "4": [select_4(), "Query 4: Średnia ocen dla wszystkich grup, uwzględniając wszystkie oceny."],
    "5": [select_5(), "Query 5: Przedmioty, które prowadzi wybrany wykładowca."],
    "6": [select_6(), "Query 6: Lista uczniów w wybranej grupie."],
    "7": [select_7(), "Query 7: Oceny uczniów w wybranej grupie z określonego przedmiotu."],
    "8": [select_8(), "Query 8: Średnia ocen wystawionych przez wykładowcę z danego przedmiotu."],
    "9": [select_9(), "Query 9: Lista kursów, na które uczęszcza uczeń."],
    "10": [select_10(), "Query 10: Lista kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia."],
}
