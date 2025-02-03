from db.database import SessionLocal, engine
from db.models import Base
from routers import auth, food

from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://tnorth.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(food.router)

