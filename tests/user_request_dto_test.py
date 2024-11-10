import unittest
from domain.entities.user import User
from src.app.data_transfer_objects.user_request_dto import UserRequestDTO


class TestUserRequestDTO(unittest.TestCase):

    def test_initialization_with_defaults(self):
        dto = UserRequestDTO()

        self.assertEqual(dto.id, "")
        self.assertEqual(dto.name, "")
        self.assertEqual(dto.email, "")
        self.assertEqual(dto.password, "")

    def test_initialization_with_values(self):
        dto = UserRequestDTO(
            id="123", name="John Doe", email="john.doe@example.com", password="secret"
        )
        self.assertEqual(dto.id, "123")
        self.assertEqual(dto.name, "John Doe")
        self.assertEqual(dto.email, "john.doe@example.com")
        self.assertEqual(dto.password, "secret")

    def test_to_entity_method(self):
        dto = UserRequestDTO(
            id="123", name="John Doe", email="john.doe@example.com", password="secret"
        )

        user = dto.to_entity()

        self.assertIsInstance(user, User)
        self.assertEqual(user.id, "123")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.password, "secret")

    def test_validation(self):
        dto = UserRequestDTO(
            name="Jane Doe", email="jane.doe@example.com", password="securepass"
        )

        self.assertEqual(dto.name, "Jane Doe")
        self.assertEqual(dto.email, "jane.doe@example.com")
        self.assertEqual(dto.password, "securepass")

        with self.assertRaises(ValueError):
            UserRequestDTO(name="Invalid", email=123, password="password")
        with self.assertRaises(ValueError):
            UserRequestDTO(name=123, email="test@example.com", password="password")
        with self.assertRaises(ValueError):
            UserRequestDTO(name="Test", email="test@example.com", password=123)


if __name__ == "__main__":
    unittest.main()
