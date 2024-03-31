from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserIn, UserOut


async def get_user_by_username(username: str, db: Session) -> UserOut:
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserIn, db: Session) -> UserOut:
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
    user.refresh_token = token
    db.commit()
