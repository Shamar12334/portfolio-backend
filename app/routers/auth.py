from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import verify_password
from app.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(username: str, password:str, db:Session=Depends(get_db)):
    user= db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password,user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token=create_access_token({"sub": user.username})
    return{"access_token": token, "token_type": "bearer"}