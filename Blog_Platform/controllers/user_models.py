from database.postgres_connector import create_session, User
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import JWTDecodeError
from passlib.hash import pbkdf2_sha256 as sha


from config import SECRET_KEY_SIGNATURES

obj = jwt.JWT()
key = jwt.jwk_from_dict({
    "kty": "oct",
    "k": SECRET_KEY_SIGNATURES,
    "alg": "HS256",
    "use": "sig",
   })

def generate_jwt_token(user_id: int, username: str, role: str) -> str:
    expiration = int((datetime.now(tz=timezone.utc) + timedelta(minutes=10)).timestamp())
    payload = {
        "user_id": user_id,
        "username": username,
        "role" : role,
        "exp": expiration
    }
    return obj.encode(payload, key, alg="HS256")

def verify_jwt_token(token: str) -> dict:
    try:
        payload = obj.decode(token, key, algorithms=["HS256"])
        return payload
    except JWTDecodeError as e:
        print("Token invalid or expired, try logging in again. Error:", e)
        return None

async def create_user(username: str, password: str, role: str):
    try:
        session = create_session()
        user = User(username=username, hashed_password=sha.hash(password), role=role)
        session.add(user)
        session.commit()
        return user.id
    except Exception as e:
        print(f"Error creating user: {e}")
        session.rollback()
        return None
    finally:
        session.close()

async def login_user(username: str, password: str):
    try:
        session = create_session()
        user = session.query(User).filter_by(username=username).first()
        if not user:
            raise ValueError("Invalid username or password.")
        if not sha.verify(password, user.hashed_password):
            raise ValueError("Invalid username or password.")
        jwt = generate_jwt_token(user.id, user.username, user.role)
        return jwt
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None
    finally:
        session.close()

async def get_all_users():
    try:
        session = create_session()
        users = session.query(User).all()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return None
    finally:
        session.close()