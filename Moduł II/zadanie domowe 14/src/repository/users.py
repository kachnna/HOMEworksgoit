from libgravatar import Gravatar
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.database.models import User
from src.schemas import UserIn, UserOut, UserDb


async def get_user_by_username(username: str, db: Session) -> UserDb:
    """    
    Retrieves a user data for a specific username.

    :param username: Username of the user.
    :type username: str
    :param db: The database session.
    :type db: Session
    :return: Data of the user found via username.
    :rtype: UserOut
    """
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserIn, db: Session) -> UserOut:
    """    
    Creates a new user for a specific data.

    :param body: The data for the user to create.
    :type body: UserIn
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: UserOut
    """
    avatar = None
    try:
        g = Gravatar(body.username)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """    
    Updates the refresh token for a specific user.

    :param user: The data of the user.
    :type user: User
    :param token: Genereted a new token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: Nothing is returned. The function performs updates to the database.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()

# async def get_user_by_email(email: str, db: Session) -> UserOut:
#     return db.query(User).filter(User.email == email).first()


async def confirmed_email(username: str, db: Session) -> None:
    """    
    Confirmes an email of the user.

    :param username: Username of the user.
    :type username: str
    :param db: The database session.
    :type db: Session
    :return: Nothing is returned. The function performs updates to the database.
    :rtype: None
    """
    user = await get_user_by_username(username, db)
    try:
        user.confirmed = True
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="User not found")


async def update_avatar(username, url: str, db: Session) -> UserDb:
    """    
    Updates the avatar of the user with new one.

    :param username: Username of the user.
    :type username: str
    :param url: Address URL of the new avatar.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated user data with new avatar.
    :rtype: UserOut
    """
    try:
        user = await get_user_by_username(username, db)
        user.avatar = url
        db.commit()
        return user
    except:
        raise HTTPException(status_code=404, detail="User not found")
