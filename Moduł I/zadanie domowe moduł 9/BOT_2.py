
contacts_list = {}


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return print(
                f"I'm sorry but there is a KeyError in function {func.__name__} - no {args[0]} in our contact list.")
        except ValueError as e:
            print(
                f"Error caught: {e} in function {func.__name__} with values {args}. Please enter information properly.")
        except IndexError:
            return print(f"Incomplete command. Please enter the required arguments.")
    return wrapper
# Dodawanie kontaktu


@input_error
def add_contact(name, phone):
    contact = name.capitalize()
    contacts_list[contact] = phone
    return f"Added {contact} with phone number {phone} to contacts list."

# Szukanie osoby i wyświetlenie jej numeru


@input_error
def find_contact(name):
    contact = name.capitalize()
    return f"{contact}'s phone number is {contacts_list[contact]}."


# Zmiana numeru
@input_error
def change_contact(name, new_phone):
    contact = name.capitalize()
    if not contact in contacts_list:
        return f"No {contact} found in contact list, so I cannot change anything.\nPlease use command 'add ' to add him/her to contactsad list"
    else:
        contacts_list[contact] = new_phone
        return f"Changed {contact}'s phone number to {new_phone}."

# Pokazanie całej listy


@input_error
def display_contacts():
    if not contacts_list:
        return "No contacts list found."

    show_list = "\n".join(
        [f"{name}: {phone}" for name, phone in contacts_list.items()])
    return show_list


def main():
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
            parts = user_input.split()
            if len(parts) == 3:
                _, name, phone = parts
                print(add_contact(name, phone))
            else:
                print("Invalid command. Enter command properly: add name phone")
        elif user_input.startswith("change "):
            parts = user_input.split()
            if len(parts) == 3:
                _, name, phone = parts
                print(change_contact(name, phone))
            else:
                print("Invalid command. Enter command properly: change name phone")
        elif user_input.startswith("phone "):
            parts = user_input.split()
            if len(parts) == 2:
                _, name = parts
                print(find_contact(name))
            else:
                print("Invalid command. Enter command properly: phone name")
        elif user_input == "show all":
            print(display_contacts())
        else:
            print("Invalid command. Please try again. Use command: 'add ', 'change ', 'phone ' or 'show all'.\n"
                  "If you want to end program write 'good bye', 'close', '.' or 'exit'")


if __name__ == "__main__":
    main()
