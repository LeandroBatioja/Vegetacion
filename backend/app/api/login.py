from fastapi import APIRouter, HTTPException
from app.models.user_model import UserLogin
from app.utils.auth import authenticate_user, create_token

router = APIRouter()

@router.post("/login/login")
def login(user: UserLogin):
    if authenticate_user(user.username, user.password):
        token = create_token(user.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
