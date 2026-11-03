from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.models import Message
from app.schemas.message import MessageCreate


def get_by_id(db: Session, message_id: int) -> Message | None:
    return db.get(Message, message_id)


def list_for_ad(
    db: Session, ad_id: int, *, offset: int = 0, limit: int = 20
) -> tuple[list[Message], int]:
    conditions = [Message.ad_id == ad_id]
    total = db.scalar(
        select(func.count()).select_from(Message).where(*conditions)
    ) or 0
    items = db.scalars(
        select(Message)
        .where(*conditions)
        .order_by(Message.created_at.desc(), Message.id.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return list(items), total


def list_inbox_for_user(
    db: Session, user_id: int, *, offset: int = 0, limit: int = 20
) -> tuple[list[Message], int]:
    conditions = [Message.recipient_id == user_id]
    total = db.scalar(
        select(func.count()).select_from(Message).where(*conditions)
    ) or 0
    items = db.scalars(
        select(Message)
        .where(*conditions)
        .order_by(Message.created_at.desc(), Message.id.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return list(items), total


def list_conversation(
    db: Session,
    user_a_id: int,
    user_b_id: int,
    *,
    ad_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> tuple[list[Message], int]:
    pair = or_(
        and_(Message.sender_id == user_a_id, Message.recipient_id == user_b_id),
        and_(Message.sender_id == user_b_id, Message.recipient_id == user_a_id),
    )
    conditions = [pair]
    if ad_id is not None:
        conditions.append(Message.ad_id == ad_id)

    total = db.scalar(
        select(func.count()).select_from(Message).where(*conditions)
    ) or 0
    items = db.scalars(
        select(Message)
        .where(*conditions)
        .order_by(Message.created_at.asc(), Message.id.asc())
        .offset(offset)
        .limit(limit)
    ).all()
    return list(items), total


def create(db: Session, payload: MessageCreate) -> Message:
    message = Message(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def delete(db: Session, message: Message) -> None:
    db.delete(message)
    db.commit()