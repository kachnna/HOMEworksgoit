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


if __name__ == "__main__":

    address_book = AddressBook()

    record1 = Record("Mary")
    record1.add_phone("123-456-7890")
    address_book.add_record(record1)

    record2 = Record("Mat")
    record2.add_phone("987-654-3210")
    record2.add_phone("555-123-4567")
    address_book.add_record(record2)

    for result in address_book.search("Mat"):
        print(result.name.value, [phone.value for phone in result.phones])

    record2.remove_phone("555-123-4567")
    record2.edit_phone("987-654-3210", "757-333-892")

    for results in address_book:
        for result in address_book.search(results):
            print(f"{results}: {[phone.value for phone in result.phones]} ")
