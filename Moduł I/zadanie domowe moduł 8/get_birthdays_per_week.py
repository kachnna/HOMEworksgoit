import datetime

def get_birthdays_per_week(list_users):

    today = datetime.date.today()
    print(f"Today is {today}.")

    current_weekday = today.weekday()
    days_until_monday = current_weekday % 7
    start_of_week = today - datetime.timedelta(days=days_until_monday)
    end_of_week = start_of_week + datetime.timedelta(days=4)
    saturday = start_of_week - datetime.timedelta(days=1)
    sunday = start_of_week - datetime.timedelta(days=2)
    print(f"Checking who you need to wish a birthday this week ({start_of_week} - {end_of_week}) at work.")
    print(f"Also checking if someone had a birthday over the weekend {saturday} and {sunday}.")

    birthdays_by_day = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }
    for user in list_users:
        birthday = user.get('birthday')
        birthday = birthday.replace(year=today.year)
        if start_of_week <= birthday <= end_of_week:
            day_of_week = birthday.strftime("%A")
            birthdays_by_day[day_of_week].append(user['name'])
        elif saturday == birthday:
            birthdays_by_day['Monday'].append(user['name'])
        elif sunday == birthday:
            birthdays_by_day['Monday'].append(user['name'])

    if not any(birthdays_by_day.values()):
        print(f"No colleagues have upcoming birthdays this week or had a previous weekend.")
    else:
        wishes = []
        for day, users in birthdays_by_day.items():
            if len(users) >= 2:
                info = day + ': ' + ', '.join(users)
                wishes.append(info)
            else:
                for user in users:
                    info = day + ': ' + user
                    wishes.append(info)
        print(f'Wish Happy Birthday to your colleague on the following days:')
        for wish in wishes:
            print(wish)

list_users = [
    {"name": "Bill", "birthday": datetime.date(2000, 10, 29)},
    {"name": "Jill", "birthday": datetime.date(1977, 10, 31)},
    {"name": "Kim", "birthday": datetime.date(1987, 11, 3)},
    {"name": "John", "birthday": datetime.date(1992, 11, 3)},
    {"name": "Loki", "birthday": datetime.date(1992, 11, 1)},
    {"name": "Thor", "birthday": datetime.date(1999, 10, 28)},
    {"name": "Freya", "birthday": datetime.date(1988, 10, 30)}
            ]
get_birthdays_per_week(list_users)
