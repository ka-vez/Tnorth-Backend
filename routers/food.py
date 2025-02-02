from ..db.database import SessionLocal 
from .auth  import get_current_user

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(prefix="/food" ,tags=['food'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[str, Depends(get_current_user)]

@router.get("/")
async def health_check(user: user_dependency):
    return {"message": user['username']}