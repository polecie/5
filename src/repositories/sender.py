from src.api.v1.schemas.senders import SenderRequest
from src.repositories.base import AbstractRepository
from dataclasses import dataclass
from src.models import Sender
from sqlalchemy import select

__all__ = ("SenderRepository",)


@dataclass
class SenderRepository(AbstractRepository):
    model: type[Sender] = Sender

    async def add(self, data: SenderRequest, user_id: int) -> Sender:  # модель из базы
        sender_to_connect = Sender(**data.dict(), user_id=user_id)
        self.session.add(sender_to_connect)
        return sender_to_connect

    async def get(self, data: SenderRequest = None, sender_id: int = None) -> Sender | None:
        if data:
            statement = select(self.model).where(self.model.email == data.email)  # type: ignore
            response = await self.session.execute(statement)
            return response.scalars().one_or_none()
        return await self._get(sender_id=sender_id)

    async def delete(self, sender_id: int) -> bool:
        sender = await self._get(sender_id=sender_id)
        if sender:
            await self.session.delete(sender)
            return True
        return False

    async def list(self, user_id: int):
        statement = select(self.model).where(self.model.user_id == user_id)  # type: ignore
        response = await self.session.execute(statement)
        return response.scalars().all()  # type: ignore

    async def _get(self, sender_id: int):
        statement = select(self.model).where(self.model.id == sender_id)  # type: ignore
        response = await self.session.execute(statement)
        return response.scalars().one_or_none()
