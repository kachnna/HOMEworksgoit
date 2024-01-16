from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle
from abc import abstractmethod, ABC
from pathlib import Path
from .data import TestData
from .record import Record, Tag


class AbstractAddressBook(ABC):

    @abstractmethod
    def read_from_file(self):
        # Read address book data from a file.
        pass

    @abstractmethod
    def save_to_file(self):
        # Save address book data to a file.
        pass

    @abstractmethod
    def add(self, name, phone, email, birthday, address, tag, notes):
        # Add a new contact to the address book.
        pass

    @abstractmethod
    def edit(self, contact, att, new_info):
        # Edit contact information.
        pass

    @abstractmethod
    def delete(self, key):
        # Delete a contact from the address book.
        pass

    @abstractmethod
    def show(self):
        # Show all contacts in the address book.
        pass

    @abstractmethod
    def show_per_page(self, number_of_contacts, new_counting, iterator=None):
        # Show contacts per page.
        pass

    @abstractmethod
    def check_if_contact_exists(self, name):
        # Find contacts by name.
        pass

    @abstractmethod
    def check_if_tag_exists(self, tag):
        # Find notes by tag.
        pass

    @abstractmethod
    def birthday(self, contact_name):
        # days till birthday
        pass

    @abstractmethod
    def func_upcoming_birthdays(self, days_str):
        # Find upcoming birthdays.
        pass


class Contact_not_found(Exception):
    pass


class MyContactsIterator:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.keys = list(dictionary.keys())
        self.index = 0

    def __next__(self):
        if self.index < len(self.keys):
            key = self.keys[self.index]
            value = self.dictionary[key]
            self.index += 1
            yield key, value
        raise StopIteration


@dataclass
class AddressBook(AbstractAddressBook):
    def __init__(self):
        self.counter: int
        self.filename = "contacts.bin"
        self.path = Path("./" + self.filename)

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def read_from_file(self):
        if self.path.is_file() == False:
            test_data = TestData()
            self.contacts = test_data.test_contacts

        else:
            with open(self.filename, "rb") as file:
                self.contacts = pickle.load(file)
        return self.contacts

    def __iter__(self):
        return MyContactsIterator(self.contacts)

    def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)
            except KeyError as e:
                print(
                    f"Username not provided or user not found. Try again.\nError details: {str(e)}\n"
                )
            except IndexError as e:
                print(
                    f"Incorrect data has been entered. Try again.\nError details: {str(e)}\n"
                )
            except ValueError as e:
                print(
                    f"I'm sorry, but I don't understand your request. Try again.\nError details: {str(e)}\n"
                )
            except Contact_not_found as e:
                print(f"Contact not found.")
            # except Exception as e:
            #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

        return wrapper

    @input_error
    def check_entered_values(self, name=None, phone=None, email=None, birthday=None, address=None, tag=None, notes=None):
        try:
            if name.value is None and phone.value is None and email.value is None and birthday.value is None and address.value is None and tag.value is None and notes.value is None:
                return False
            else:
                return True
        except Contact_not_found as e:
            print(f"Contact not found.")

    @input_error
    def check_if_contact_exists(self, name):
        if name is None:
            pass
        results = {}
        contact_name = name if isinstance(name, str) else name.value
        for key, obj in self.contacts.items():
            if isinstance(obj.name, str):
                value = obj.name
            else:
                value = obj.name.value if hasattr(
                    obj.name, 'value') else obj.name
            if contact_name.lower() in value.lower():
                results[key] = obj
        return results

    @input_error
    def check_if_tag_exists(self, tag):
        if Tag is None:
            pass
        results = {}
        contact_tag = tag if isinstance(tag, str) else tag.value
        for key, obj in self.contacts.items():
            if isinstance(obj.tag, str):
                value = obj.tag
            else:
                value = obj.tag.value if hasattr(
                    obj.tag, 'value') else obj.tag
            if contact_tag.lower() in value.lower():
                results[key] = obj
        return results

# SHOW #

    @input_error
    def show(self):
        if not self.contacts:
            print("Address book is empty.")
        else:
            return self.contacts

    @input_error
    def show_per_page(self, number_of_contacts, new_counting, iterator=None):
        if new_counting == True:
            self.counter = 0
            iterator = iter(
                sorted(self.contacts.items(), key=lambda x: x[1].name))
        is_last = False
        contacts_to_display = {}
        if self.counter * number_of_contacts < len(self.contacts):
            for _ in range(number_of_contacts):
                try:
                    key, obj = next(iterator)
                    contacts_to_display[key] = obj
                except StopIteration:
                    break
        self.counter += 1
        if self.counter * number_of_contacts >= len(self.contacts):
            is_last = True
        return self.counter, iterator, contacts_to_display, is_last
# birthdays

    @input_error
    def birthday(self, contact_name):
        results_for_birthday = {}
        for id, obj in contact_name.items():
            results_for_birthday[id] = [
                obj, obj.days_to_birthday(obj.birthday.value)]
        return results_for_birthday

#  upcoming birthdays
    @input_error
    def func_upcoming_birthdays(self, days_str):

        today = datetime.now()
        formatted_date = today.strftime("%d %B %Y")
        days = int(days_str)
        last_day = today + timedelta(days=days)
        formatted_last_day = last_day.strftime("%d %B %Y")
        print(
            f"\nChecking period ({formatted_date} - {formatted_last_day}).\n")

        birthdays_list = {}
        today_birthday = {}

        for id, user_info in self.contacts.items():
            name = user_info.name.value
            birthday_str = user_info.birthday.value
            phone = user_info.phone.value
            email = user_info.email.value
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()

            birthday_this_year = birthday.replace(year=today.year)
            birthday_next_year = birthday.replace(year=today.year + 1)

            if today.date() < birthday_this_year <= last_day.date():
                day_of_week = birthday_this_year.strftime("%d %B (%A)")
                if day_of_week not in birthdays_list:
                    birthdays_list[day_of_week] = []
                birthdays_list[day_of_week].append((name, phone, email))
            elif today.date() < birthday_next_year <= last_day.date():
                day_of_week = birthday_next_year.strftime("%d %B (%A)")
                if day_of_week not in birthdays_list:
                    birthdays_list[day_of_week] = []
                birthdays_list[day_of_week].append((name, phone, email))
            elif today.date() == birthday_this_year:
                day_of_week = birthday_this_year.strftime("%d %B (%A)")
                if day_of_week not in today_birthday:
                    today_birthday[day_of_week] = []
                today_birthday[day_of_week].append((name, phone, email))

        return [today_birthday, birthdays_list]

# add
    @input_error
    def add(self, name, phone, email, birthday, address, tag, notes):
        id = int(self.check_latest_id() + 1)
        new_contact = Record(name.value, phone.value, email.value,
                             birthday.value, address.value, tag.value, notes.value)
        self.contacts[id] = new_contact
        return dict(filter(lambda item: item[0] == id, self.contacts.items()))

# edit
    @input_error
    def edit(self, contact, att, new_info):
        for id, obj in contact.items():
            if att == "name":
                obj.edit_name(new_info)
            elif att == "phone":
                obj.edit_phone(new_info)
            elif att == "email":
                obj.edit_email(new_info)
            elif att == "birthday":
                obj.edit_birthday(new_info)
            elif att == "address":
                obj.edit_address(new_info)
            elif att == "tag":
                obj.edit_tag(new_info)
            elif att == "notes":
                obj.edit_notes(new_info)
            else:
                return f"Unable to edit."

# delete

    @input_error
    def delete(self, key):
        self.contacts.pop(key)

# delete contact information
    @input_error
    def delete_info(self, contact, info_delete):
        for id, obj in contact.items():
            if info_delete == "phone":
                obj.delete_phone()
            elif info_delete == "email":
                obj.delete_email()
            elif info_delete == "birthday":
                obj.delete_birthday()
            elif info_delete == "address":
                obj.delete_address()
            elif info_delete == "tag":
                obj.delete_tag()
            elif info_delete == "notes":
                obj.delete_notes()
            else:
                return f"Unable to delete."
