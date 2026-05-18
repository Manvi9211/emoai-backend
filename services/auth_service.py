from supabase import create_client, Client
from fastapi import HTTPException
from config import SUPABASE_URL, SUPABASE_ANON_KEY

_client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def sign_up(email: str, password: str) -> dict:
    try:
        res = _client.auth.sign_up({"email": email, "password": password})
        if res.user is None:
            raise HTTPException(
                status_code=400, detail="Signup failed. Try a different email.")
        return {
            "user_id":      res.user.id,
            "email":        res.user.email,
            "access_token": res.session.access_token if res.session else None,
            "message":      "Account created! Check your email to confirm.",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def sign_in(email: str, password: str) -> dict:
    try:
        res = _client.auth.sign_in_with_password(
            {"email": email, "password": password})
        if res.user is None:
            raise HTTPException(
                status_code=401, detail="Invalid email or password.")
        return {
            "user_id":       res.user.id,
            "email":         res.user.email,
            "access_token":  res.session.access_token,
            "refresh_token": res.session.refresh_token,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid email or password.")


def get_user(access_token: str) -> dict:
    """Validate a JWT and return the user — used to protect routes."""
    try:
        res = _client.auth.get_user(access_token)
        if res.user is None:
            raise HTTPException(
                status_code=401, detail="Invalid or expired token.")
        return {"user_id": res.user.id, "email": res.user.email}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token.")
