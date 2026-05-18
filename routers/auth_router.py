from fastapi import APIRouter, Header
from pydantic import BaseModel, EmailStr
from services.auth_service import sign_up, sign_in, get_user

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(req: AuthRequest):
    return sign_up(req.email, req.password)


@router.post("/login")
def login(req: AuthRequest):
    return sign_in(req.email, req.password)


@router.get("/me")
def me(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    return get_user(token)
