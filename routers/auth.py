from db.database import SessionLocal 
from db.models import Users
from schemas import CreateUserRequest

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError


router = APIRouter(prefix="/auth", tags=['auth'])

SECRET_KEY = '2342n23j4n24nin423k424iinINI3ININIIIN2iinin323i2ni2n3i2n3i2nini'
ALGORITHM = 'HS256'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oath2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(user_id: int, username: str, user_role: str, user_first_name: str, user_last_name: str, expires_delta: timedelta):
    encode = {"user_id": user_id, "username": username, "role": user_role, "first_name":user_first_name, "last_name": user_last_name}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        user_id: int = payload.get('user_id')
        user_role: str = payload.get('user_role')
        user_first_name: str = payload.get('first_name')
        user_last_name: str = payload.get('last_name')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
        return {"username": username, "id": user_id, "role": user_role, "first_name": user_first_name, "user_last_name": user_last_name}
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate user '{err}'")

@router.get("/")
async def get_users(db: db_dependency):
    users = db.query(Users).all()   
    return {"users": users}

@router.post("/")
async def create_users(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        is_active = create_user_request.is_active,
        role = create_user_request.role,
        phone_number = create_user_request.phone_number,
        hashed_password =  bcrypt_context.hash(create_user_request.password)
    )   

    db.add(create_user_model)
    db.commit()
    return {"detail": "New user has been created"}

@router.post("/token")
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    token = create_access_token(user.id, user.username, user.role, user.first_name, user.last_name, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
