import unittest
import os
from unittest.mock import patch
from jwt import encode
from infra.authorization.token_authorization import TokenAuthorization


class TestTokenAuthorization(unittest.TestCase):
    @patch.dict(os.environ, {"JWT_SECRET": "test_secret"})
    def test_encode(self):
        payload = {"user_id": 123}

        token = TokenAuthorization.encode(payload)

        expected_token = encode(payload, "test_secret", algorithm="HS256")
        self.assertEqual(token, expected_token)

    @patch("infra.authorization.token_authorization.get_unverified_header")
    def test_verify_valid_token(self, mock_get_unverified_header):
        token = "dummy_token"
        mock_header = {"alg": "HS256"}
        mock_get_unverified_header.return_value = mock_header

        header = TokenAuthorization.verify(token)

        self.assertEqual(header, mock_header)
        mock_get_unverified_header.assert_called_once_with(token)


if __name__ == "__main__":
    unittest.main()
