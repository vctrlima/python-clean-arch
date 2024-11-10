import unittest
from uuid import uuid4
from pydantic import ValidationError
from src.app.data_transfer_objects.user_response_dto import UserResponseDTO


class TestUserResponseDTO(unittest.TestCase):

    def test_initialization_with_defaults(self):
        dto = UserResponseDTO()

        self.assertIsNone(dto.id)
        self.assertEqual(dto.name, "")
        self.assertEqual(dto.email, "")

    def test_initialization_with_values(self):
        test_id = uuid4()

        dto = UserResponseDTO(id=test_id, name="John Doe", email="john.doe@example.com")

        self.assertEqual(dto.id, test_id)
        self.assertEqual(dto.name, "John Doe")
        self.assertEqual(dto.email, "john.doe@example.com")

    def test_uuid_validation(self):
        with self.assertRaises(ValidationError):
            UserResponseDTO(
                id="invalid-uuid", name="Jane Doe", email="jane.doe@example.com"
            )

    def test_model_config_from_attributes(self):
        test_data = {"id": uuid4(), "name": "Alice", "email": "alice@example.com"}

        dto = UserResponseDTO(**test_data)

        self.assertEqual(dto.id, test_data["id"])
        self.assertEqual(dto.name, test_data["name"])
        self.assertEqual(dto.email, test_data["email"])


if __name__ == "__main__":
    unittest.main()
