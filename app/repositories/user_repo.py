from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserCreate


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def list_with_filters(
    db: Session,
    *,
    query: str | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> tuple[list[User], int]:
    conditions = []
    if query:
        like = f"%{query}%"
        conditions.append(or_(User.name.ilike(like), User.email.ilike(like)))
    if age_min is not None:
        conditions.append(User.age >= age_min)
    if age_max is not None:
        conditions.append(User.age <= age_max)

    total = db.scalar(select(func.count()).select_from(User).where(*conditions)) or 0
    items = db.scalars(
        select(User).where(*conditions).order_by(User.id).offset(offset).limit(limit)
    ).all()
    return list(items), total


def create(db: Session, payload: UserCreate) -> User:
    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, data: dict) -> User:
    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()