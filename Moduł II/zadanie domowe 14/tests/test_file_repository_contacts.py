import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from sqlalchemy import or_, extract, and_
from src.database.models import Contact, User
from src.schemas import ContactIn, ContactUpdate
from datetime import datetime, timedelta

from src.repository.contacts import (
    get_contacts,
    get_contact,
    find_contact,
    create_contact,
    remove_contact,
    update_contact,
    get_contacts_birthday_for_next_seven_days,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactIn(
            name="John",
            lastname="Doe",
            email="johndoe@example.com",
            phone="123456789",
            birthday="1990-01-01",
            notes="string",
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.notes, body.notes)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactUpdate(
            name="Jane",
            lastname="Doe",
            email="janedoe@example.com",
            phone="",
            birthday="",
            notes="",
        )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(
            name="Jane",
            lastname="Doe",
            email="janedoe@example.com",
            phone="",
            birthday="",
            notes="",
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_find_contact_found(self):
        contacts = [Contact(name="Jane"), Contact(
            email="johndoe@example.com"), Contact(lastname="Kowalska")]
        word = "Jane"
        self.session.query().filter(and_(or_(Contact.name.ilike(word), Contact.lastname.ilike(
            word), Contact.email.ilike(word)))).offset().limit().all.return_value = contacts
        result = await find_contact(keyword="Jane", skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_find_contact_not_found(self):
        word = "Jane"
        self.session.query().filter(and_(or_(Contact.name.ilike(word), Contact.lastname.ilike(
            word), Contact.email.ilike(word)))).offset().limit().all.return_value = None
        result = await find_contact(keyword="Jane", skip=0, limit=10, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_birthday_for_next_seven_days_found(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        birthday1 = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        birthday2 = (today + timedelta(days=2)).strftime("%Y-%m-%d")
        birthday3 = (today + timedelta(days=3)).strftime("%Y-%m-%d")
        contacts = [Contact(birthday=birthday1), Contact(
            birthday=birthday2), Contact(birthday=birthday3)]
        self.session.query().filter(and_(
            or_(
                and_(
                    extract("month", today) == extract("month", next_week),
                    extract("month", Contact.birthday) == extract(
                        "month", today),
                    extract("day", Contact.birthday) >= extract("day", today),
                    extract("day", Contact.birthday) <= extract(
                        "day", next_week)
                ),
                and_(
                    extract("month", today) != extract("month", next_week),
                    extract("month", Contact.birthday) == extract(
                        "month", today),
                    extract("day", Contact.birthday) >= extract("day", today)
                ),
                and_(
                    extract("month", today) != extract("month", next_week),
                    extract("month", Contact.birthday) == extract(
                        "month", next_week),
                    extract("day", Contact.birthday) <= extract(
                        "day", next_week)
                )
            ))).order_by("birthday").offset().limit().all.return_value = contacts
        result = await get_contacts_birthday_for_next_seven_days(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_birthday_for_next_seven_days_notfound(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        self.session.query().filter(and_(
            or_(
                and_(
                    extract("month", today) == extract("month", next_week),
                    extract("month", Contact.birthday) == extract(
                        "month", today),
                    extract("day", Contact.birthday) >= extract("day", today),
                    extract("day", Contact.birthday) <= extract(
                        "day", next_week)
                ),
                and_(
                    extract("month", today) != extract("month", next_week),
                    extract("month", Contact.birthday) == extract(
                        "month", today),
                    extract("day", Contact.birthday) >= extract("day", today)
                ),
                and_(
                    extract("month", today) != extract("month", next_week),
                    extract("month", Contact.birthday) == extract(
                        "month", next_week),
                    extract("day", Contact.birthday) <= extract(
                        "day", next_week)
                )
            ))).order_by("birthday").offset().limit().all.return_value = None
        result = await get_contacts_birthday_for_next_seven_days(skip=0, limit=10, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
