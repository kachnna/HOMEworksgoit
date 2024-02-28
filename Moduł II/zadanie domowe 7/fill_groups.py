import random
from connect import session
from models import Group

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

def create_data(data) -> None:
    for groups in data:
        fake_groups = Group(name=groups[0])
        session.add(fake_groups)
    session.commit()


def create_groups(numbers):
    create_data(generate_data(numbers))


