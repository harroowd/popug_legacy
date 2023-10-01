from bcrypt import (
    checkpw,
    gensalt,
    hashpw,
)


class Password:
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
