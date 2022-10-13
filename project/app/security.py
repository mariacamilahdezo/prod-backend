# from datetime import datetime, timedelta
# from typing import Any, Union, Optional

# from jose import jwt
# from passlib.context import CryptContext

# from app.config import get_settings
# from app import schemas
# from fastapi import Request
# import logging

# logger = logging.getLogger(__name__)


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# hashing_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# ALGORITHM = "HS256"


# def create_access_token(
#     subject: Union[str, Any],
#     roles: str,  # TODO: validate Role Exists. Multiple or Single one?
#     is_active: bool = False,
#     expires_delta: timedelta = None,
# ) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     # SYNC: TokenPayload Schema
#     to_encode = {
#         "sub": str(subject),
#         "roles": str(roles),
#         "active": is_active,
#         "iat": datetime.utcnow(),
#         "exp": expire,
#     }
#     encoded_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def extract_token_data(token: str):
#     payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[ALGORITHM])
#     token_data = schemas.TokenPayload(**payload)
#     return token_data


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


# def get_hash(anything: Any) -> str:
#     return hashing_context.hash(anything)


# def verify_hash(plain_obj: Any, hashed_obj: Any) -> bool:
#     return hashing_context.verify(plain_obj, hashed_obj)


# def generate_reset_password_link(request: Request, token: str):
#     server_host = request.url.hostname
#     scheme = request.url.scheme
#     print("Schema  + host: ", scheme, server_host)
#     print("Base url", request.base_url)
#     link = f"{request.base_url}/reset-password?token={token}"
#     return link


# def send_reset_password_email(
#     email_to: str, email: str, token: str, request: Request
# ) -> None:
#     # TODO: Add this functionality if needed
#     # project_name = settings.PROJECT_NAME
#     # subject = f"{project_name} - Password recovery for user {email}"
#     # with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
#     #    template_str = f.read()
#     # link = generate_reset_password_link(request, token)
#     # send_email(
#     #    email_to=email_to,
#     #    subject_template=subject,
#     #    html_template=template_str,
#     #    environment={
#     #        "project_name": settings.PROJECT_NAME,
#     #        "username": email,
#     #        "email": email_to,
#     #        "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
#     #        "link": link,
#     #    },
#     # )
#     pass


# def generate_password_reset_token(email: str) -> str:
#     delta = timedelta(hours=get_settings().EMAIL_RESET_TOKEN_EXPIRE_HOURS)
#     now = datetime.utcnow()
#     expires = now + delta
#     exp = expires.timestamp()
#     encoded_jwt = jwt.encode(
#         {"exp": exp, "nbf": now, "sub": email},
#         get_settings().SECRET_KEY,
#         algorithm=ALGORITHM,
#     )
#     return encoded_jwt


# def verify_password_reset_token(token: str) -> Optional[str]:
#     try:
#         decoded_token = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[ALGORITHM])
#         return decoded_token["email"]
#     except jwt.JWTError:
#         return None
