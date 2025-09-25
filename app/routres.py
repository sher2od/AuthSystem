from random import randint

from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from .database import get_db

from fastapi_mail import FastMail,MessageSchema


from .schemas import UserCreate,UserVerify
from .models import User

from .config import mail_conf

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def register_api(user:UserCreate,db:Annotated[Session,Depends(get_db)]):
    verification_code = randint(1000000,9999999)
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        hashed_password = hashed_password,
        is_active = False,
        is_verified = False,
        verification_code  = verification_code
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)



    message = MessageSchema(
        subject="Verification Code",
        recipients=[user.email],
        body=f"Tasdiqlash Kod:{verification_code}",
        subtype="plain"
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message)

    return {"message":"zorr"}

@router.post("/verify")
async def verify_code(user_verify:UserVerify,db:Annotated[Session,Depends(get_db)]):
    user = db.query(User).filter(User.email == user_verify.email).first()

    if user:
        if user.verification_code == int(user_verify.verification_code):
            return{"message":"succes"}
        
    raise HTTPException(status_code=400,detail="erroor")