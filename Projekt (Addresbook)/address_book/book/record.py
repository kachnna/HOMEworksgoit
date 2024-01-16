from dataclasses import dataclass
import re
from datetime import datetime


@dataclass
class Field:
    value: None


@dataclass
class Name(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __lt__(self, other):
        return self.value < other.value


@dataclass
class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None and not self.validate_phone(new_value):
            raise ValueError("Invalid phone number format")
        if new_value == "":
            self._value = None
        else:
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
        if new_value == "":
            self._value = None
        else:
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
        if new_value == "":
            self._value = None
        else:
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

    @value.setter
    def value(self, new_value):
        if new_value == "":
            self._value = None
        else:
            self._value = new_value


@dataclass
class Tag(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == "":
            self._value = None
        else:
            self._value = new_value


@dataclass
class Notes(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == "":
            self._value = None
        else:
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
#########################   EDIT    ##########################################################################

    def edit_name(self, new_name):
        self.name.value = new_name
        print(f"Name of the contact updated to {new_name}.")

    def edit_phone(self, new_phone):
        self.phone.value = new_phone
        print(f"Phone number updated for {self.name.value}")

    def edit_email(self, new_email):
        self.email.value = new_email
        print(f"Email updated for {self.name.value}")

    def edit_birthday(self, new_birthday):
        self.birthday.value = new_birthday
        print(f"Birthday updated for {self.name.value}")

    def edit_address(self, new_address):
        self.address.value = new_address
        print(f"Address updated for {self.name.value}")

    def edit_tag(self, new_tag):
        self.tag.value = new_tag
        print(f"Tag updated for {self.name.value}")

    def edit_notes(self, new_notes):
        self.notes.value = new_notes
        print(f"Notes updated for {self.name.value}")

####################### DELETE  ###################################################################################
    def delete_phone(self):
        self.phone.value = None
        print(f"Phone number deleted for {self.name.value}")

    def delete_email(self):
        self.email.value = None
        print(f"Email deleted for {self.name.value}")

    def delete_birthday(self):
        self.birthday.value = None
        print(f"Birthday deleted for {self.name.value}")

    def delete_address(self):
        self.address.value = None
        print(f"Address deleted for {self.name.value}")

    def delete_notes(self):
        self.notes.value = None
        print(f"Notes deleted for {self.name.value}")

    def delete_tag(self):
        self.tag.value = None
        print(f"Tag deleted for {self.name.value}")

###########################  DAYS TO BIRTHDAY   #####################################################################

    def days_to_birthday(self, contact_birthday):
        if contact_birthday is not None:
            current_datetime = datetime.now()
            birthday_strptime = datetime.strptime(contact_birthday, "%Y-%m-%d")
            birthday_date = datetime(
                current_datetime.year, birthday_strptime.month, birthday_strptime.day
            )
            if current_datetime.date() == birthday_date.date():
                return "Today!"
            else:
                if current_datetime.date() > birthday_date.date():
                    birthday_date = datetime(
                        current_datetime.year + 1,
                        birthday_strptime.month,
                        birthday_strptime.day,
                    )
                to_birthday = (birthday_date - current_datetime).days
                return to_birthday
        else:
            return None
