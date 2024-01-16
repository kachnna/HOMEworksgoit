from book import inter
from .address_book import AddressBook
from .record import Notes, Name, Phone, Email, Birthday, Address, Tag
from thefuzz import fuzz


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


def command_hint(user_str: str, commands, threshold: int = 0) -> str:
    """return string with hint for user describig
    closest match to the available bot commands"""
    user_str = user_str.strip()
    hint = ""
    # for short string use startwith
    if len(user_str) <= 3:
        hits = clossest_match(user_str, commands)
    else:  # for longer strings use fuzzy string matching
        # calculate similarity scores for each command
        # ratio
        # scores = [fuzz.ratio(user_str, command) for command in commands]
        # partial
        # print(commands)
        scores = [fuzz.partial_ratio(user_str, command)
                  for command in commands]

        # threshold = 0
        scores = list(filter(lambda x: x >= threshold, scores))
        # print(scores)
        # find best score
        best_score = max(scores)
        # print(best_score)
        # find all commands with best scores
        hits = [
            command for score, command in zip(scores, commands) if score == best_score
        ]
        # print(hits)

    if len(hits) > 0:
        hint = f"Did you mean?: {', '.join(hits)}"
    return hint


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
        # except Exception as e:
        #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

    return wrapper

########################    HELP     ######################


def help(object):
    print(
        """Choose one of the commands:
    - hello - let's say hello,
    - find - to find a contact by name,
    - search - to find a contact after entering keyword (except tag and notes),
    - search notes - to find a contact name after entering keyword by searching by tag,
    - show all - to show all of your contacts from address book or show all your notes,
    - show - to display 'n' contacts from Address Book,
    - add - to add new contact to Address Book,
    - birthday - to display days to birthday of the user,
    - upcoming birthdays - to check upcoming birthdays from your conatct in Address Book
    - edit - edit your contacts information      
    - delete - to remove contact from Address Book,
    - good bye, close, exit or . - to say good bye and close the program.
After entering the command, you will be asked for additional information if needed to complete the command.""")

#####################################    HELLO   ###########################


def func_hello(object):
    print("How can I help you?")

#####################################   ADD   ##############################


@input_error
def add_func(obj):
    to_add = True
    print("\nPlease complete the information below. Name is mandatory, but the rest you can skip by clicking Enter.")
    name = Name(input("\nEnter name*: "))
    contact = obj.check_if_contact_exists(name)

    if len(contact) > 0:
        print("\nI've found in the Address Book the contact(s) with the same name:")
        inter.ViewContact().display(contact)
        choice = input("\nWould you like to update the contact? (Y/N): ")
        if choice.lower() in ["y", "yes", "true"]:
            to_add = False
            while True:
                att = input("\nPlease choose which information would you like to change? "
                            "\nName, Phone, Email, Birthday, Address, Tag, or Notes: ").lower().strip()

                if att in ["name", "phone", "email", "birthday", "address", "tag", "notes"]:
                    new_value = input(
                        f"Input new {att} of the contact (press Enter to keep current): ").strip()

                    if new_value:
                        object.edit(contact, att, new_value)
                    else:
                        print(f"Keeping current {att}.")

                    another_change = input(
                        "\nDo you want to make another change? (Y/N): ")
                    if another_change.lower() not in ["y", "yes", "true"]:
                        object.save_to_file()
                        print("Contact editing complete.")
                        break
                else:
                    print("\nInvalid choice. Please choose a valid attribute.")
                    continue
        else:
            print("Contact not confirmed for editing.")

    phone = Phone(input("Enter new phone: "))
    email = Email(input("Enter new email: "))
    birthday = Birthday(input("Enter new birthday: "))
    address = Address(input("Enter new address: "))
    tag = Tag(input("Enter new tag: "))
    notes = Notes(input("Enter new notes: "))

    if obj.check_entered_values(name, phone, email, birthday, address, tag, notes):
        if to_add:
            new_contact = obj.add(name, phone, email,
                                  birthday, address, tag, notes)
            obj.save_to_file()
            inter.ViewContact().display(new_contact)
            print("Contact added successfully.")
        raise ValueError(
            "You did not enter any data to change the contact information. Please try again.")

#########################################   SHOW   ##########################


@input_error
def show_all_func(object):
    choice = input(
        "Would you like to see all contacts or notes.\n Write contacts or notes: ")
    if choice.lower().strip() == "contacts":
        result = object.show()
        inter.ViewContacts().display(result)
    elif choice.lower().strip() == "notes":
        result = object.show()
        inter.ViewNotes().display(result)
    else:
        print("Incorrect input. Should be 'contacts' or 'notes'.")

#################################  SHOW PER PAGE  ###########################


@input_error
def show_per_page(object):
    iter_state = None
    counting = True
    print("You want to display your 'n' contacts from Address Book.")
    try:
        n = int(
            input("How many contacts you want to display at once.\nEnter 'n' number: "))
    except ValueError:
        print("Entered number is not an integer. Please try again.")
        return

    while True:
        page, iter_state, contacts, is_last = object.show_per_page(
            n, counting, iter_state)
        counting = False
        print(f"\nPAGE {page}")
        inter.ViewContacts().display(contacts)

        if is_last:
            print("\nI've displayed all contacts from the Address Book.")
            break

        choice = input(
            f"\nDo you want to display next {n} contact(s)? (Y/N) ")

        if choice.lower().strip() not in ["y", "yes", "true"]:
            break


################################    FIND CONTACT   #########################
@input_error
def find_func(object):
    name = Name(input("\nEnter name of contact you would like to find: "))
    contact = object.check_if_contact_exists(name)
    if contact:
        print("\nI've found in the Address Book the contact you are looking for")
        inter.display_contacts(inter.ViewContact(), contact)
    else:
        print(f"Contact with name '{name.value}' not found.")

#############################  SEARCH THROUGH NOTES    #####################


@input_error
def search_tag(object):
    print("You would like to see notes with certain tag.")
    tag = Tag(input("\nEnter the name of the tag: "))
    tag_sear = object.check_if_tag_exists(tag)
    if tag_sear:
        print("\nI've found this tag.")
        inter.ViewNotes().display(tag_sear)
    else:
        print(f"There is no tag {tag.value}.")

#################################  days till birthday  ######################


@input_error
def contact_birthday(object):
    name = Name(input(
        "Which contact's birthday do you want to display (enter name)?: "))
    contact = object.check_if_contact_exists(name)
    if contact:
        result = object.birthday(contact)
        inter.ViewContactBirthday().display(result)
    else:
        print(f"Contact with name '{name}' not found.")

###########################   UPCOMING BIRTHDAYS  ##########################


@input_error
def upcoming_birthdays(object):
    days_str = int(input("Find out who will be celebrating their birthday in the near future!\nHow many days in advance would you like to see your contacts' upcoming birthdays?\nEnter number of days:  "))
    today = {}
    upcoming = {}
    list = object.func_upcoming_birthdays(days_str)
    today = list[0]
    upcoming = list[1]
    if not any(today) and not any(upcoming):
        print(f"\nNone of your contacts have upcoming birthdays in this period.")
    else:
        print(
            "   O O O O \n" "  _|_|_|_|_\n" " |         |\n",
            "|         |\n",
            "|_________|\n",
        )
    if any(today):
        print("\nSomeone has birthday today, so wish 'HAPPY BIRTHDAY' today to: ")
        inter.ViewTodayBirthday().display(today)
    if any(upcoming):
        print("\nSend birthday wishes to your contact on the upcoming days:")
        inter.ViewUpcomingBirthdays().display(upcoming)

############################################ EDIT ##########################


@input_error
def edit_func(object):
    name = Name(input("\nEnter name of contact you would like to edit: "))
    contact = object.check_if_contact_exists(name)
    if contact:
        print("\nI've found in the Address Book the contact you want to edit:")
        inter.ViewContact().display(contact)
        choice = input(
            "\nPlease confirm if this is the contact you want to edit? (Y/N): ")

        if choice.lower() in ["y", "yes", "true"]:
            while True:
                att = input("\nPlease choose which information would you like to change? "
                            "\nName, Phone, Email, Birthday, Address, Tag, or Notes: ").lower().strip()

                if att in ["name", "phone", "email", "birthday", "address", "tag", "notes"]:
                    new_value = input(
                        f"Input new {att} of the contact (press Enter to keep current): ").strip()

                    if new_value:
                        object.edit(contact, att, new_value)
                    else:
                        print(f"Keeping current {att}.")

                    another_change = input(
                        "\nDo you want to make another change? (Y/N): ")
                    if another_change.lower() not in ["y", "yes", "true"]:
                        object.save_to_file()
                        print("Contact editing complete.")
                        break
                else:
                    print("\nInvalid choice. Please choose a valid attribute.")
                    continue
        else:
            print("Contact not confirmed for editing.")
    else:
        print(f"Contact with name '{name.value}' not found.")

###################################  DELETE  ###############################


@input_error
def delete_func(object):
    name = Name(input("\nPlease enter name of the contact: "))
    contact = object.check_if_contact_exists(name)
    if len(contact) > 0:
        print("\nI've found in the Address Book this contact.")
        inter.ViewContact().display(contact)
        info_delete = input(
            "\nWhat would you like to delete?\n Contact, Name, Phone, Email, Birthday, Address, Tag, or Notes: ")
        if info_delete.lower().strip() == "contact":
            choice_1 = input(
                "\nAre you sure you want to delete hole contact form Addres Book? (Y/N): ")
            if choice_1.lower().strip() in ["y", "yes", "true"]:
                for contact_id in contact.keys():
                    object.delete(contact_id)
                    object.save_to_file()
                print("\nContact deleted successfully.")
            else:
                print("\n No contact was delete from this Address Book.")
        elif info_delete.lower().strip() in ["phone", "email", "birthday", "address", "tag", "notes"]:
            while True:
                choice_2 = input(
                    f"You would like to delete {info_delete} of the {name.value} (Y/N): ")
                if choice_2.lower().strip() in ["y", "yes", "true"]:
                    object.delete_info(contact, info_delete)
                else:
                    print(f"{info_delete} was not deleted.")
                another_change = input(
                    "\nDo you want to make another change? (Y/N): ")
                if another_change.lower().strip() not in ["y", "yes", "true"]:
                    object.save_to_file()
                    print("Delete complete.")
                    break
                else:
                    print("\nInvalid choice. Please choose a valid attribute.")
                    continue
    else:
        print(f"Contact not found.")

#######################################    EXIT    #########################


def func_exit(object):
    print(
        """
                                           ..::::------:::..                                           
                                 .:-=+*#%@@@@@@@@@@@@@@@@@@@@%##*+=:.                                  
                            :-+#%@@@@@@@@@@@@%%##******##%%@@@@@@@@@@@#*=:                             
                        :+#@@@@@@@%#*+=-:..                 ..:-=+*%@@@@@@@#+-.                        
                    .=*@@@@@@#+=:                                    :-+#@@@@@@#=.                     
                  -#@@@@@#=:    .-=*:        -.         =         =+-:    :=*%@@@@#=.                  
               :*@@@@%+-    :=*%@@@=         +%:      .*@:        .#@@@#+-.   :=#@@@@#-                
             -#@@@%+:   :+#@@@@@@@+          #@@#*****@@@-         .%@@@@@@#+:   .=%@@@%=              
           :#@@@#-   :+%@@@@@@@@@#           %@@@@@@@@@@@=          -@@@@@@@@@%+:   :*@@@%=            
         .*@@@#-   -#@@@@@@@@@@@@:           @@@@@@@@@@@@*           #@@@@@@@@@@@#-   :*@@@#:          
        :%@@%-   -%@@@@@@@@@@@@@%           .@@@@@@@@@@@@#           =@@@@@@@@@@@@@%-   :#@@@=         
       =@@@*.  .#@@@@@@@@@@@@@@@#           -@@@@@@@@@@@@@           -@@@@@@@@@@@@@@@#.   +@@@*        
      =@@@=   -@@@@@@@@@@@@@@@@@%           =@@@@@@@@@@@@@:          +@@@@@@@@@@@@@@@@@-   -%@@*       
     =@@@=   +@@@@@@@@@@@@@@@@@@@-          %@@@@@@@@@@@@@=          %@@@@@@@@@@@@@@@@@@+   :%@@*      
    :@@@=   =@@@@@@@@@@@@@@@@@@@@%.        =@@@@@@@@@@@@@@@:        *@@@@@@@@@@@@@@@@@@@@=   :@@@-     
    #@@#   :@@@@@@@@@@@@@@@@@@@@@@%-      +@@@@@@@@@@@@@@@@%-     :#@@@@@@@@@@@@@@@@@@@@@@:   +@@%     
   .@@@:   *@@@@@@@@@@@@@@@@@@@@@@@@%*==*%@@@@@@@@@@@@@@@@@@@%*+*#@@@@@@@@@@@@@@@@@@@@@@@@*   .@@@=    
   =@@%    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    *@@*    
   +@@#   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.   +@@%    
   +@@#   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    Good bye!    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.   +@@%    
   =@@@    %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%    *@@*    
   .@@@-   =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=   .@@@=    
    *@@#    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#    +@@%     
    .@@@+    *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.   :@@@-     
     -@@@=    -%@@@@@@@@@@=.   :=#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+-:.:=%@@@@@@@@@@#.   :%@@+      
      =@@@=    .*@@@@@@@@-        :#@@@@@*==*%@@@@@@@@@@@%*++%@@@@@*:       .%@@@@@@@@=    -@@@*       
       =@@@*.    :*@@@@@@.          =@@%:     =@@@@@@@@%-     +@@%-          +@@@@@@*.    +@@@+        
        :%@@%=     :*@@@@=           :%:       .%@@@@@#.       *%.           #@@@@*:    -%@@@=         
         .+@@@%-     .+%@%.                     .%@@@#         ..           :@@%+.    :#@@@#.          
           :#@@@%=.     :+*.                     :@@@:                     .#+-     -#@@@%-            
             :#@@@@*:                             +@+                      .     :+%@@@%=              
               :+@@@@%+-                          .%.                         :+%@@@@*-                
                  -*@@@@@#=:                       :                      :=*@@@@@#=.                  
                    .-*%@@@@@#*=:.                                   :-+#@@@@@@*=.                     
                        :=*%@@@@@@@#*+=-::.                ..:-=+*#%@@@@@@@#+:                         
                            .-+*%@@@@@@@@@@@@%%%#######%%%@@@@@@@@@@@%#+-:                             
                                  :-=+*#%%@@@@@@@@@@@@@@@@@@%%#*+=-:.                                  
                                           ...::------:::.                      
"""
    )
    exit()


@input_error
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
What would you like to do with your Address Book? \nIf you need instructions write 'help'. """
    )
    user_addr_book = AddressBook()
    user_addr_book.read_from_file()
    OPERATIONS_MAP = {
        "hello": func_hello,
        "help": help,
        "find": find_func,
        "search notes": search_tag,
        "show all": show_all_func,
        "show": show_per_page,
        "add": add_func,
        "birthday": contact_birthday,
        "upcoming birthdays": upcoming_birthdays,
        "edit": edit_func,
        "delete": delete_func,
        "good bye": func_exit,
        "close": func_exit,
        "exit": func_exit,
        ".": func_exit,
    }
    while True:
        listen_enterred = input("\nEnter your command here: ")
        listen = listen_enterred.lower().strip()
        if listen in OPERATIONS_MAP:
            OPERATIONS_MAP[listen](user_addr_book)
        else:
            hint_for_user = command_hint(listen, OPERATIONS_MAP.keys())
            if hint_for_user:
                print(hint_for_user)
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
