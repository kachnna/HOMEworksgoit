from dataclasses import dataclass
import re
from datetime import datetime


@dataclass
class Field:
    value: str = None


@dataclass
class Name(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


@dataclass
class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None and not self.validate_phone(new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value

    def validate_phone(self, value):
        if len(value) == 0:
            return True
        if value is not None:
            validate_regex = r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
            if re.match(validate_regex, value):
                return True
        return False


@dataclass
class Email(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None and not self.validate_email(new_value):
            raise ValueError("Invalid email address format")
        self._value = new_value

    def validate_email(self, value):
        if len(value) == 0:
            return True
        if value is not None:
            email_regex = r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}"
            return bool(re.match(email_regex, value))
        return False


@dataclass
class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None and not self.validate_birthday(new_value):
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        self._value = new_value

    def validate_birthday(self, value):
        date_format = "%Y-%m-%d"
        if len(value) == 0:
            return True
        try:
            datetime.strptime(value, date_format)
            return True
        except:
            return False


@dataclass
class Address(Field):
    @property
    def value(self):
        return self._value

    # @value.setter
    # def value(self, new_value):
    #     if new_value is not None and not self.validate_address(new_value):
    #         raise ValueError("Invalid address format")

    #     self._value = new_value

    # def validate_address(self, value):
    #     address_parts = [part.strip() for part in value.split(",")]
    #     return len(address_parts) == 4

    @value.setter
    def value(self, new_value):
        self._value = new_value


@dataclass
class Tag(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


@dataclass
class Notes(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


@dataclass
class Record:
    name: Name
    phone: Phone
    email: Email
    birthday: Birthday
    address: Address
    tag: Tag
    notes: Notes

    def edit_phone(self, new_phone):
        self.phone = new_phone
        print(f"Phone number updated for {self.name}")

    def edit_email(self, new_email):
        self.email = new_email
        print(f"Email updated for {self.name}")

    def edit_birthday(self, new_birthday):
        self.birthday = new_birthday
        print(f"Birthday updated for {self.name}")

    def delete_phone(self):
        self.phone = None
        print(f"Phone number deleted for {self.name}")

    def delete_email(self):
        self.email = None
        print(f"Email deleted for {self.name}")

    def delete_birthday(self):
        self.birthday = None
        print(f"Birthday deleted for {self.name}")

    def days_to_birthday(self, contact_name, contact_birthday):
        if contact_birthday is not None and len(contact_birthday) > 0:
            current_datetime = datetime.now()
            birthday_strptime = datetime.strptime(contact_birthday, "%Y-%m-%d")
            birthday_date = datetime(
                current_datetime.year, birthday_strptime.month, birthday_strptime.day
            )
            if current_datetime.date() == birthday_date.date():
                print(f"Today is {contact_name}'s birthday!")
            else:
                if current_datetime.date() > birthday_date.date():
                    birthday_date = datetime(
                        current_datetime.year + 1,
                        birthday_strptime.month,
                        birthday_strptime.day,
                    )
                to_birthday = (birthday_date - current_datetime).days
                print(f"Days until {contact_name}'s birthday: {to_birthday}")
        else:
            print(f"{contact_name} has no birthday entered in the address book.")

    def edit_address(self, new_address):
        self.address = new_address
        print(f"Address updated for {self.name}")

    def delete_address(self):
        self.address = None
        print(f"Address deleted for {self.name}")

    def edit_notes(self, new_notes):
        self.notes = new_notes
        print(f"Notes updated for {self.name}")

    def delete_notes(self):
        self.notes = None
        print(f"Notes deleted for {self.name}")

    def edit_tag(self, new_tag):
        self.tag = new_tag
        print(f"Tag updated for {self.name}")
    
    def delete_tag(self):
        self.tag = None
        print(f"Tag deleted for {self.name}")