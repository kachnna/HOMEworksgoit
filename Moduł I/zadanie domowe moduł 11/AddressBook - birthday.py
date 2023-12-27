from datetime import datetime


class Field:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __repr__(self):
        return self.name


class Phone(Field):
    def __set__(self, instance, value):
        if not value or not value.isdigit():
            raise ValueError(
                "Phone number must be a non-empty string of digits")
        super().__set__(instance, value)


class Birthday(Field):
    def __set__(self, instance, value):
        if not isinstance(value, datetime):
            raise ValueError("Birthday must be a datetime object")
        super().__set__(instance, value)


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(
                today.year, self.birthday.month, self.birthday.day).date()

            if today > next_birthday:
                next_birthday = datetime(
                    today.year + 1, self.birthday.month, self.birthday.day).date()

            days_until_birthday = (next_birthday - today).days
            return days_until_birthday
        else:
            return None

    def __repr__(self):
        birthday_str = (
            self.birthday.strftime('%Y-%m-%d') if self.birthday else 'None'
        )
        days_to_birthday = self.days_to_birthday()
        days_str = f"Days till next birthday: {days_to_birthday}" if days_to_birthday is not None else "No birthday set"
        return f' Record: {self.name}\n Phone:{self.phone}\n Birthday:{birthday_str}.\n {days_str}'


class AddressBook:
    def __init__(self):
        self.records = []
        self.current_page = 0

    def add_record(self, record):
        self.records.append(record)

    def __iter__(self):
        return self

    def __next__(self):
        start = self.current_page
        end = self.current_page + 1
        if start >= len(self.records):
            raise StopIteration

        page = self.records[start:end]
        self.current_page += 1
        return page

    def __repr__(self):
        return '\n\n'.join([f"Page {i + 1}:\n" + '\n'.join(map(repr, page))
                            for i, page in enumerate(self)])


def main():

    record1 = Record(name="Loki Ragnarson", phone="1234567890",
                     birthday=datetime(1990, 11, 19))
    record2 = Record(name="Ragnar Ragarson", phone="9876543210")
    record3 = Record(name="Freya Ragarson", phone="24654521433",
                     birthday=datetime(1999, 7, 20))
    record4 = Record(name="Odyn Ragarson", phone=535323243,
                     birthday=datetime(1999, 12, 4))

    address_book = AddressBook()
    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)
    address_book.add_record(record4)
    print(address_book)


if __name__ == '__main__':
    main()
