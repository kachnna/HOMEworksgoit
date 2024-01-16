from abc import abstractmethod, ABC
from datetime import datetime


class ContactNotFound(Exception):
    pass


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ContactNotFound as e:
            print("\nSorry, but I couldn't find any contacts in the Address book.")
    return wrapper


def check_value(value):
    if value is None:
        return ""
    return value


def month_sort_key(date_str):
    date = datetime.strptime(date_str, "%d %B (%A)")
    current_month = datetime.now().month
    return (date.month - current_month) % 12


class AbstractView(ABC):
    @abstractmethod
    def display(self, data):
        pass


class ViewContacts(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<40}|"
            separator = ("{:<163}".format("-" * 143))
            print(separator)
            print(pattern.format("Id", "Name", "Phone",
                  "Email", "Birthday", "Address"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.phone.value),
                    check_value(obj.email.value),
                    check_value(obj.birthday.value),
                    check_value(obj.address.value),
                ))
            print(separator)
        else:
            raise ContactNotFound


class ViewNotes(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern = "|{:<20}|{:^20}|{:<133}"
            separator = ("{:<176}".format("-" * 176))
            print(separator)
            print(pattern.format("Name", "Tag", "Notes"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern.format(
                    check_value(obj.name.value),
                    check_value(obj.tag.value),
                    check_value(obj.notes.value),
                ))
            print(separator)
        else:
            raise ContactNotFound


class ViewContact(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_contacts = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            pattern_tag_notes = "|{:^10}|{:<150}|"
            separator = ("{:^163}".format("-" * 163))
            print(separator)
            print(pattern_contacts.format("Id", "Name",
                  "Phone", "Email", "Birthday", "Address"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern_contacts.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.phone.value),
                    check_value(obj.email.value),
                    check_value(obj.birthday.value),
                    check_value(obj.address.value),
                ))
                print(separator)
                print("\n{:^163}".format("-" * 163))
                print(pattern_tag_notes.format(
                    "Tag", check_value(obj.tag.value)))
                print(separator)
                print(pattern_tag_notes.format(
                    "Notes", check_value(obj.notes.value)))
                print(separator)
        else:
            raise ContactNotFound


class ViewTodayBirthday(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            print("{:^90}".format("*" * 90))
            print("{:^30}|{:^30}|{:^30}".format("Name", "Phone", "Email"))
            print("{:^90}".format("*" * 90))
            for day, users in sorted(data.items(), key=lambda x: x[0]):
                for user_info in users:
                    print("{:^30}|{:^30}|{:^30}".format(*user_info))
                    print("*" * 90)


class ViewUpcomingBirthdays(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            print("{:^120}".format("-" * 120))
            print(
                "{:^30}|{:^30}|{:^30}|{:^30}".format(
                    "Birthday", "Name", "Phone", "Email"
                )
            )
            print("{:^120}".format("-" * 120))
            for day, users in sorted(
                data.items(), key=lambda x: month_sort_key(x[0])
            ):
                for user_info in users:
                    print("{:^30}|{:^30}|{:^30}|{:^30}".format(day, *user_info))
                    print("-" * 120)


class ViewContactBirthday(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:^17}|"
            separator = ("{:^120}".format("-" * 120))
            print(separator)
            print(pattern.format("Id", "Name ^", "Phone",
                  "Email", "Birthday", "Days to Birthday"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: getattr(x[1][0], 'name', x[1][0])):
                print(pattern.format(
                    id,
                    check_value(getattr(obj[0], 'name', obj[0]).value),
                    check_value(getattr(obj[0], 'phone', obj[0]).value),
                    check_value(getattr(obj[0], 'email', obj[0]).value),
                    check_value(getattr(obj[0], 'birthday', obj[0]).value),
                    check_value(obj[1]),
                ))
            print(separator)
        else:
            raise ContactNotFound


def display_contacts(view: AbstractView, data) -> None:
    view.display(data)
