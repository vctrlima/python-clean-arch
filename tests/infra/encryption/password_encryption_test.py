import pytest

from infra.encryption.password_encryption import PasswordEncryption


class TestPasswordEncryption:
    def test_encrypt_creates_hash(self):
        password = "my_secure_password"

        hash = PasswordEncryption.encrypt(password)

        assert hash is not None
        assert isinstance(hash, str)
        assert len(hash) > 0
        assert password != hash

    def test_verify_correct_password(self):
        password = "my_secure_password"

        hash = PasswordEncryption.encrypt(password)

        assert PasswordEncryption.verify(password, hash) is True

    def test_verify_incorrect_password(self):
        password = "my_secure_password"
        incorrect_password = "wrong_password"

        hash = PasswordEncryption.encrypt(password)

        assert PasswordEncryption.verify(incorrect_password, hash) is False

    def test_verify_with_tampered_hash(self):
        password = "my_secure_password"

        hash = PasswordEncryption.encrypt(password)

        tampered_hash = hash[:-1] + ("a" if hash[-1] != "a" else "b")
        assert PasswordEncryption.verify(password, tampered_hash) is False
