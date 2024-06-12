import os
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.repositories.sqlite import engine, session_local
from sqlalchemy.orm import Session
from src.repositories.sqlite.models import user
from src.entities.token import Token,TokenData
from dotenv import load_dotenv
from src.api import api_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
