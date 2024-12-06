import os
import logging
from datetime import datetime, timedelta
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from jwt import encode, decode, get_unverified_header, ExpiredSignatureError
from dotenv import load_dotenv

load_dotenv()


class TokenAuthorization:
    @staticmethod
    def encode(payload: dict):
        return encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")

    @staticmethod
    def decode(token: str):
        return decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])

    @staticmethod
    def verify(token: str):
        try:
            return get_unverified_header(token)
        except ExpiredSignatureError as error:
            logging.getLogger(__name__).exception(error)
            raise ExpiredSignatureError(error)

    @staticmethod
    def generate_access_token(user_dto: UserResponseDTO):
        payload = {
            "id": str(user_dto.id),
            "name": user_dto.name,
            "email": user_dto.email,
            "exp": datetime.now() + timedelta(minutes=30),
        }
        return TokenAuthorization.encode(payload)

    @staticmethod
    def generate_refresh_token(user_dto: UserResponseDTO):
        payload = {
            "id": str(user_dto.id),
            "exp": datetime.now() + timedelta(days=1),
        }
        return TokenAuthorization.encode(payload)
