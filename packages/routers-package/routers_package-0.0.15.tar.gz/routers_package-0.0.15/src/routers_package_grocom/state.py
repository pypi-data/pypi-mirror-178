import os

from .backend import TokenBackend
from dotenv import load_dotenv
load_dotenv()


algorithm = os.getenv('ALGORITHM', None)
secret_key = os.getenv('SECRET_KEY', None)
verifying_key = os.getenv('VERIFYING_KEY', None)
audience = os.getenv('AUDIENCE', None)
issuer = os.getenv('ISSUER', None)
token_type_claim = os.getenv('TOKEN_TYPE_CLAIM', None)
jti_claim = os.getenv('JTI_CLAIM', None)
user_id_field = os.getenv('USER_ID_FIELD', None)
user_id_claim = os.getenv('USER_ID_CLAIM', None)

token_backend = TokenBackend(algorithm, secret_key, verifying_key, audience, issuer)
