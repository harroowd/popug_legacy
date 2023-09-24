from datetime import datetime

from bcrypt import checkpw, gensalt, hashpw
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession


class Security:
    def __init__(self, password: str = None):
        self._password = password

    def get_password_hash(self) -> str:
        password = self._password.encode("utf-8")

        salt = gensalt()
        hashed_password = hashpw(password, salt)
        return hashed_password.decode("utf-8")

    def verify_password(self, hashed_password: str) -> bool:
        return checkpw(
            self._password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    async def verify_account(self, user: User, db: AsyncSession):
        if user and self.verify_password(user.password):
            user.current_sign_in_at = datetime.utcnow()
            await db.commit()
            return user
