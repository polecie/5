import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    Integer,
    event,
    select,
    func
)
from sqlalchemy.engine.base import Connection
from src.db import base

__all__ = ("User", "Email", "Provider", "Sender")


class User(base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, unique=True, index=True)  # id в телеграм
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # senders = relationship("Sender", back_populates="user", cascade="all, delete")
    # emails = relationship("Email", back_populates="user", cascade="all, delete")


class Provider(base):
    __tablename__ = "provider"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, nullable=False, unique=True)
    server = Column(String, nullable=False)
    port = Column(Integer, nullable=False)


class Email(base):
    __tablename__ = "email"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    provider_id = Column(Integer, ForeignKey("provider.id", ondelete="CASCADE"), nullable=False)
    # user = relationship("User", back_populates="emails")


class Sender(base):
    __tablename__ = "sender"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # id в телеграм
    # user = relationship("User", back_populates="senders")


@event.listens_for(Email, "after_delete")
def after_delete_listener(mapper, connection: Connection, target: Email):
    count = connection.execute(
        select(
            func.count(Email.id)
        ).where(Email.user_id == target.user_id)  # type: ignore
    ).scalar()
    if count == 0:
        statement = select(
            func.count(Sender.id)
        ).where(Sender.user_id == target.user_id)  # type: ignore
        senders = connection.execute(statement).scalar()
        if senders > 0:
            connection.execute(
                Sender.__table__.delete().where(
                    Sender.user_id == target.user_id
                )  # type: ignore
            )
