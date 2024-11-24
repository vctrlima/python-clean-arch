import os
import logging
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
