import bcrypt


class PasswordEncryption:
    @staticmethod
    def encrypt(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash)
