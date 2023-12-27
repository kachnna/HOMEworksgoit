from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if query in phone.value:
                        results.append(record)
                        break
        return results


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return f"I'm sorry but there is a KeyError in function {func.__name__} - no '{args[0]}' in our contacts list."
        except ValueError as e:
            return f"Error caught: {e} in function {func.__name__} with values '{args[0]}'. Please enter information properly."
        except IndexError:
            return f"Incomplete command. Please enter the required arguments."
    return wrapper


@input_error
def add_contact(user_input, address_book):
    _, name, phone = user_input.split()
    contact = name.capitalize()
    if contact not in address_book.data:
        record = Record(contact)
        record.add_phone(phone)
        address_book.add_record(record)
        return f"Added {contact} with phone number {phone} to contacts list."
    else:
        address_book.data[contact].add_phone(phone)
        return f"Added phone number {phone} to {contact}'s contact."


@input_error
def remove_contact(user_input, address_book):
    _, name = user_input.split()
    contact = name.capitalize()
    if not contact in address_book.data:
        return f"No {contact} found in the contacts list."
    remove = input(
        "Do you want remove contact or only phone number? Please write 'contact' or 'phone': ")
    if remove.strip().lower() == "contact":
        del address_book.data[contact]
        return f"Removed {contact} from contacts list."
    elif remove.strip().lower() == "phone":
        phones = [phone.value for phone in address_book.data[contact].phones]
        if len(phones) > 1:
            print(f"This is {contact} list of phone numbers: {phones}")
            num = input("Which you wish to remove: ")
            address_book.data[contact].remove_phone(num)
            return f"Removed phone number {num} from {contact}'s contact."
        else:
            address_book.data[contact].remove_phone(
                address_book.data[contact].phones[0].value)
            return f"{contact} has no phone number in contact list."
    else:
        return f"Invalid answer try again."


@input_error
def find_contact(user_input, address_book):
    _, name = user_input.split()
    contact = name.capitalize()
    phones = [phone.value for phone in address_book.data[contact].phones]
    return f"{contact}'s phone number is {phones}."


@input_error
def change_contact(user_input, address_book):
    _, name, phone = user_input.split()
    contact = name.capitalize()
    if contact not in address_book.data:
        return f"No {contact} found in contact list, so I cannot change anything.\nPlease use command 'add ' to add him/her to contacts list"
    else:
        phones = [phone.value for phone in address_book.data[contact].phones]
        if len(phones) > 1:
            print(f"This is {contact} list of phone numbers: {phones}")
            num = input("Which you wish to change: ")
            address_book.data[contact].edit_phone(num, phone)
            return f"Changed {contact}'s phone number {num} to {phone}."
        else:
            address_book.data[contact].edit_phone(
                address_book.data[contact].phones[0].value, phone)
            return f"Changed {contact}'s phone number to {phone}."


@input_error
def display_contacts(address_book):
    if not address_book.data:
        return f"No contacts list found."

    show_list = "\n".join(
        [f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in address_book.data.items()])
    return show_list


def main():
    address_book = AddressBook()

    while True:
        user_input = input("Enter a command: ").strip().lower()

        if user_input == "good bye" or user_input == "close" or user_input == "exit":
            print("Good bye!")
            break
        elif user_input == ".":
            print("Closing the program.")
            break
        elif user_input == "hello":
            print("How can I help you?")
        elif user_input.startswith("add "):
            print(add_contact(user_input, address_book))
        elif user_input.startswith("change "):
            print(change_contact(user_input, address_book))
        elif user_input.startswith("remove "):
            print(remove_contact(user_input, address_book))
        elif user_input.startswith("phone "):
            print(find_contact(user_input, address_book))
        elif user_input == "show all":
            print(display_contacts(address_book))
        else:
            print("Invalid command. Please try again. Use command: 'add ', 'change ', 'phone ', ''remove ' or 'show all'.\n"
                  "If you want to end program write 'good bye', 'close', '.' or 'exit'")


if __name__ == "__main__":
    main()
