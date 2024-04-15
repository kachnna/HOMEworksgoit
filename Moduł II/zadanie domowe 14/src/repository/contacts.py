from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract, and_
from src.database.models import Contact, User
from src.schemas import ContactIn, ContactUpdate
from datetime import date, datetime, timedelta


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: i nt
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def find_contact(keyword: str, skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts with entered keyword for a specified user.

    :param body: The data for the contact to create.
    :type body: ContactIn
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of contacts with the specified keyword.
    :rtype: List[Contact]
    """
    word = f"%{keyword}%"
    query = db.query(Contact).filter(and_(or_(Contact.name.ilike(word), Contact.lastname.ilike(
        word), Contact.email.ilike(word)), Contact.user_id == user.id)).offset(skip).limit(limit).all()
    return query


async def create_contact(body: ContactIn, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactIn
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(name=body.name, lastname=body.lastname, email=body.email,
                      phone=body.phone, birthday=body.birthday, notes=body.notes, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        if body.name:
            contact.name = body.name
        if body.lastname:
            contact.lastname = body.lastname
        if body.email:
            contact.email = body.email
        if body.phone:
            contact.phone = body.phone
        if body.birthday:
            contact.birthday = body.birthday
        if body.notes:
            contact.notes = body.notes
        db.commit()
        db.refresh(contact)
    return contact


async def get_contacts_birthday_for_next_seven_days(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """    
    Retrieves a list of contacts for a specific user with specified pagination parameters, which have birthdays within the next seven days.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: List of contacts who have a birthday in the next seven days, in ascending order by 'birthday'.
    :rtype: List[Contact]
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    query = db.query(Contact).filter(and_(
        or_(
            and_(
                extract("month", today) == extract("month", next_week),
                extract("month", Contact.birthday) == extract("month", today),
                extract("day", Contact.birthday) >= extract("day", today),
                extract("day", Contact.birthday) <= extract("day", next_week)
            ),
            and_(
                extract("month", today) != extract("month", next_week),
                extract("month", Contact.birthday) == extract("month", today),
                extract("day", Contact.birthday) >= extract("day", today)
            ),
            and_(
                extract("month", today) != extract("month", next_week),
                extract("month", Contact.birthday) == extract(
                    "month", next_week),
                extract("day", Contact.birthday) <= extract("day", next_week)
            )
        ),
        Contact.user_id == user.id
    )).order_by("birthday").offset(skip).limit(limit).all()
    return query
