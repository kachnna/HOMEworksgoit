import json


class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, email):
        contact = {'Name': name, 'Surname': email, 'Phone': phone}
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            pass

    def search_contacts(self, query):
        results = []
        for contact in self.contacts:
            if (
                query.lower() in contact['Name'].lower() or query.lower() in contact['Surname'].lower() or
                query in contact['Phone']
            ):
                results.append(contact)
        return results


contact_book = ContactBook()


contact_book.add_contact('Obi-wan', 'Kenobi', '123-456-7890')
contact_book.add_contact('Anakin', 'Skywalker', '987-654-3210')

contact_book.save_to_file('contacts_list.json')


new_contact_book = ContactBook()
new_contact_book.load_from_file('contacts_list.json')


search_query = input("Wprowadź ciąg znaków do wyszukania: ")
results = new_contact_book.search_contacts(search_query)


print("Wyniki wyszukiwania:")
for result in results:
    print(result)
