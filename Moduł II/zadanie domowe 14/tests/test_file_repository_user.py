import unittest
from fastapi import HTTPException, status
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract, and_
from src.database.models import User
from src.schemas import UserIn, UserDb, UserOut, TokenModel, RequestEmail
from src.repository.users import get_user_by_username, create_user, update_token, confirmed_email, update_avatar


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_username_found(self):
        user = User(username="kachnna")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_username(username="kachnna", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_username_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_username(username="kachnna", db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserIn(
            username="kachnna",
            email="sara486@.pl",
            password=""
        )
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        user = User(username="kachnna")
        token = ""
        await update_token(user=user, token=token, db=self.session)
        self.session.commit.assert_called_once()

    async def test_confirm_email_found(self):
        user = User(username="kachnna")
        await confirmed_email(username=user.username, db=self.session)
        self.session.commit.assert_called_once()

    async def test_confirm_email_not_found(self):
        user = User(username="kachnna", email="")
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            await confirmed_email(username=user.username, db=self.session)
        self.session.commit.assert_not_called()
        self.assertEqual(context.exception.status_code,
                         status.HTTP_404_NOT_FOUND)

    async def test_update_avatar_found(self):
        user = User(username="kachnna",
                    avatar="")
        self.session.query().filter(user.username).first.return_value = user
        result = await update_avatar(username=user.username, url=user.avatar, db=self.session)
        self.assertEqual(result, user)

    async def test_update_avatar_not_found(self):
        user = User(username="kachnna",
                    avatar="")
        self.session.query().filter(user.username).first.return_value = None
        with self.assertRaises(HTTPException) as context:
            await update_avatar(username=user.username, url=user.avatar, db=self.session)
        self.session.commit.assert_not_called()
        self.assertEqual(context.exception.status_code,
                         status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
