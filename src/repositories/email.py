from src.api.v1.schemas.emails import EmailRequest
from src.repositories.base import AbstractRepository
from dataclasses import dataclass
from src.models import Email
from sqlalchemy import select

__all__ = ("EmailRepository",)


@dataclass
class EmailRepository(AbstractRepository):
    model: type[Email] = Email

    async def add(self, data: EmailRequest, user_id: int) -> Email:  # модель из базы
        new_email = Email(**data.dict(), user_id=user_id)
        self.session.add(new_email)
        return new_email

    async def _get(self, email_id: int) -> Email | None:
        statement = select(self.model).where(self.model.id == email_id)  # type: ignore
        response = await self.session.execute(statement)
        return response.scalars().one_or_none()

    async def get(self, data: EmailRequest = None, email_id: int = None) -> Email | None:
        if data:
            statement = select(self.model).where(self.model.email == data.email)  # type: ignore
            response = await self.session.execute(statement)
            return response.scalars().one_or_none()
        return await self._get(email_id=email_id)

    async def delete(self, email_id: int) -> bool:
        email = await self._get(email_id=email_id)
        if email:
            await self.session.delete(email)
            return True
        return False

    async def list(self, user_id: int):
        statement = select(self.model).where(self.model.user_id == user_id)  # type: ignore
        response = await self.session.execute(statement)
        return response.scalars().all()
