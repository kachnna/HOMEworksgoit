import json


class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, surname,  phone):
        contact = {'Name': name, 'Surname': surname, 'Phone': phone}
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found. No contacts loaded.")

    def search_contacts(self, query):
        results = []
        for contact in self.contacts:
            if (
                query.lower() in contact['Name'].lower() or
                query.lower() in contact['Surname'].lower() or
                query in contact['Phone']
            ):
                results.append(
                    f"{contact['Name']} {contact['Surname']}, Phone: {contact['Phone']}")
        return results

    def display_contacts(self):
        if not self.contacts:
            print("No contacts available.")
        else:
            for i, contact in enumerate(self.contacts, 1):
                print(
                    f"  {i}. {contact['Name']} {contact['Surname']}, Phone: {contact['Phone']}")


def main():
    contact_book = ContactBook()

    while True:
        contact_book.load_from_file('contacts.json')
        command = input(
            "You would like to add, search, or display the list of contacts (add/search/save/display): ")

        if command == "add":
            try:
                print("Please write: \nName Surname Phone")
                new_contact_input = input("")
                name, surname, phone = new_contact_input.split()
                contact_book.add_contact(name, surname, phone)
                print(
                    f"Contact book updated. {name} {surname} was added to the list.")
            except ValueError:
                print("Invalid input. Please provide Name, Surname, and Phone.")

        elif command.strip().lower() == "save":
            contact_book.save_to_file('contacts.json')
            print("Contacts were saved in file 'contacts.json'")

        elif command.strip().lower() == "search":
            search_query = input("Input contact you would like to find: ")
            results = contact_book.search_contacts(search_query)
            print("Search results:")
            if results:
                print("Search results:")
                for result in results:
                    print(f"   {result}")
            else:
                print("No matching contacts found.")

        elif command.strip().lower() == "display":
            contact_book.display_contacts()

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
