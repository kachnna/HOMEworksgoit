from .addressbook import AddressBook


def clossest_match(querry: str, commands):
    """filters commands if they start with querry,
    if no command found querry is shortened by one char from the end
    and function tries again (recursively)"""
    if len(querry) == 0:
        return []
    matched_commands = list(filter(lambda x: x.startswith(querry), commands))
    if len(matched_commands) > 0:
        return matched_commands
    else:
        return clossest_match(querry[:-1], commands)


def command_hint(user_str: str, commands) -> str:
    """return string with hint for user describing
    closest match to the available bot commands"""
    user_str = user_str.strip()
    hint = ""
    hits = clossest_match(user_str, commands)

    if len(hits) > 0:
        hint = f"Did you mean?: {', '.join(hits)}"
    return hint


def main():
    print(
        """
       db        88    ad88                                88  
      d88b       88   d8\"                                  88  
     d8\'`8b      88   88                                   88  
    d8\'  `8b     88 MM88MMM 8b,dPPYba,  ,adPPYba,  ,adPPYb,88  
   d8YaaaaY8b    88   88    88P\'   \"Y8 a8P_____88 a8\"    `Y88  
  d8\"\"\"\"\"\"\"\"8b   88   88    88         8PP\"\"\"\"\"\"\" 8b       88  
 d8\'        `8b  88   88    88         \"8b,   ,aa \"8a,   ,d88  
d8\'          `8b 88   88    88          `\"Ybbd8\"\'  `\"8bbdP\"Y8 

Hello! I am your virtual assistant.
What would you like to do with your Address Book?
Choose one of the commands:
    - hello - let's say hello,
    - find - to find a contact by name,
    - search - to find a contact after entering keyword (except tag and notes),
    - search notes - to find a contact name after entering keyword by searching by tag or notes,
    - show all - to show all of your contacts from address book,
    - show - to display N contacts from Address Book,
    - show notes - to display contact name with tag and notes,
    - add - to add new contact to Address Book,
    - birthday - to display days to birthday of the user,
    - upcoming birthdays - to check upcoming birthdays from your conatct in Address Book
    - edit phone - to change phone of the user,
    - edit email - to change email of the user,
    - edit birthday - to change birthday of the user,
    - edit address - to change address of the user,
    - edit tag - to change tag of the user,
    - edit notes - to change notes of the user,      
    - delete contact - to remove contact from Address Book
    - delete phone - to delete phone of the user,
    - delete email - to delete email of the user,
    - delete birthday - to delete birthday of the user,
    - delete address - to delete address of the user, 
    - delete tag - to delete tag of the user,
    - delete notes - to delete notes of the user,
    - good bye, close, exit or . - to say good bye and close the program.
After entering the command, you will be asked for additional information if needed to complete the command."""
    )
    addressbook = AddressBook()
    addressbook.read_from_file()
    OPERATIONS_MAP = {
        "hello": addressbook.func_hello,
        "find": addressbook.func_find,
        "search": addressbook.func_search,
        "search notes": addressbook.func_search_notes,
        "show all": addressbook.func_show_all,
        "show": addressbook.func_show,
        "show notes": addressbook.func_show_notes,
        "add": addressbook.func_add,
        "birthday": addressbook.func_birthday,
        "upcoming birthdays": addressbook.func_upcoming_birthdays,
        "edit phone": addressbook.func_edit_phone,
        "edit email": addressbook.func_edit_email,
        "edit birthday": addressbook.func_edit_birthday,
        "edit address": addressbook.func_edit_address,
        "edit tag": addressbook.func_edit_tag,
        "edit notes": addressbook.func_edit_notes,
        "delete contact": addressbook.func_delete_contact,
        "delete phone": addressbook.func_delete_phone,
        "delete email": addressbook.func_delete_email,
        "delete birthday": addressbook.func_delete_birthday,
        "delete address": addressbook.func_delete_address,
        "delete tag": addressbook.func_delete_tag,
        "delete notes": addressbook.func_delete_notes,
        "good bye": addressbook.func_exit,
        "close": addressbook.func_exit,
        "exit": addressbook.func_exit,
        ".": addressbook.func_exit,
    }
    while True:
        listen_enterred = input("\nEnter your command here: ")
        listen = listen_enterred.lower().strip()
        if listen in OPERATIONS_MAP:
            if listen == "add":
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                email = input("Enter email: ")
                birthday = input("Enter birthday: ")
                address = input("Enter address: ")
                tag = input("Enter tag: ")
                notes = input("Enter your notes: ")
                OPERATIONS_MAP[listen](
                    name, phone, email, birthday, address, tag, notes
                )
            elif listen in [
                "find",
                "birthday",
                "delete contact",
                "delete phone",
                "delete email",
                "delete birthday",
                "delete address",
                "delete tag",
                "delete notes",
            ]:
                name = input("Enter name: ")
                OPERATIONS_MAP[listen](name)
            elif listen == "upcoming birthdays":
                keyword = input(
                    "Which time frame from today would you like to check? Please input the number of days from now: "
                )
                OPERATIONS_MAP[listen](keyword)
            elif listen in ["search", "search notes"]:
                keyword = input("Enter keyword: ")
                OPERATIONS_MAP[listen](keyword)
            elif listen == "edit phone":
                name = input("Enter name of the contact to edit phone: ")
                new_phone = input("Enter new phone number: ")
                OPERATIONS_MAP[listen](name, new_phone)
            elif listen == "edit email":
                name = input("Enter name of the contact to edit email: ")
                new_email = input("Enter new email: ")
                OPERATIONS_MAP[listen](name, new_email)
            elif listen == "edit birthday":
                name = input("Enter name of the contact to edit birthday: ")
                new_birthday = input("Enter new birthday: ")
                OPERATIONS_MAP[listen](name, new_birthday)
            elif listen == "edit address":
                name = input("Enter name of the contact to edit address: ")
                new_address = input("Enter new address: ")
                OPERATIONS_MAP[listen](name, new_address)
            elif listen == "edit tag":
                name = input("Enter name of the contact to edit tag: ")
                new_tag = input("Enter new tag: ")
                OPERATIONS_MAP[listen](name, new_tag)
            elif listen == "edit notes":
                name = input("Enter name of the contact to edit tag: ")
                new_notes = input("Enter new notes: ")
                OPERATIONS_MAP[listen](name, new_notes)
            elif listen == "show":
                try:
                    number_of_contacts = int(
                        input("Enter number of contacts to display: ")
                    )
                    OPERATIONS_MAP[listen](number_of_contacts)
                except:
                    print("Entered number is not an integer. Please try again.")
            elif listen in ["good bye", "close", "exit", "."]:
                addressbook.save_to_file()
                OPERATIONS_MAP[listen.lower()]()
            else:
                OPERATIONS_MAP[listen.lower()]()
        else:
            hint_for_user = command_hint(listen, OPERATIONS_MAP.keys())
            if hint_for_user:  # not empty string
                print(hint_for_user)
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
