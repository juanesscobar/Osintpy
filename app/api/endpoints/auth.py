from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from jose import JWTError, jwt

from core.database import get_db
from core.security import verify_password, create_access_token, get_password_hash
from core.config import settings

router = APIRouter()
security = HTTPBasic()

# Simple user store for MVP (in production, use proper user management)
USERS = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin"),
        "full_name": "Administrator"
    }
}

@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """Login endpoint with basic auth"""
    user = USERS.get(credentials.username)

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    """Get current user info"""
    user = USERS.get(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user["username"],
        "full_name": user["full_name"]
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = USERS.get(username)
    if user is None:
        raise credentials_exception

    return username

# OAuth2 scheme for JWT tokens
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Re-export for use in other modules
__all__ = ["get_current_user", "oauth2_scheme"]