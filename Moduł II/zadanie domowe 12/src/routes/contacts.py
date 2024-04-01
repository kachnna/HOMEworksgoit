from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactIn, ContactOut, ContactUpdate
from src.repository import contacts as repository_contacts
from src.database.models import User
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts')


@router.get("/", response_model=List[ContactOut])
async def read_contacts(skip: int = 0, limit: int = 100, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactOut)
async def read_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.get("/search/{keyword}", response_model=List[ContactOut])
async def search_contact(keyword: str, skip: int = 0, limit: int = 100, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.find_contact(keyword, skip, limit, current_user, db)
    return contacts


@router.post("/", response_model=ContactOut)
async def create_contact(body: ContactIn, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactOut)
async def update_contact(body: ContactUpdate, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.delete("/{contact_id}", response_model=ContactOut)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.get("/birthday/", response_model=List[ContactOut])
async def get_contacts_birthday_for_next_seven_days(skip: int = 0, limit: int = 100, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_birthday_for_next_seven_days(skip, limit, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No person has a birthday in the next 7 days.")
    return contacts
