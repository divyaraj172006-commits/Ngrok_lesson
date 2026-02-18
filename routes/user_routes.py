from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import User
from repositories.User_repo import UserRepo
from schemas.User_schema import UserSchema

router = APIRouter()


@router.post("/users")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    """Create a new user."""
    user_repo = UserRepo(db)
    existing_user = user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(email=user.email, password=user.password)
    user_repo.add_user(db_user)
    return {"id": db_user.id, "email": db_user.email}


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    """Get all users."""
    user_repo = UserRepo(db)
    users = user_repo.get_all_users()
    return [{"id": u.id, "email": u.email} for u in users]


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID."""
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email}