from fastapi import status, HTTPException
from fastapi import Depends
from src.db import get_async_session
from src.models import Email
from sqlalchemy.ext.asyncio import AsyncSession
from src.uow import SqlAlchemyUnitOfWork
from src.api.v1.schemas.emails import EmailRequest, EmailResponse
from src.services.mixin import ServiceMixin

__all__ = ("EmailService", "get_email_service")


class EmailService(ServiceMixin):
    async def create(self, data: EmailRequest, user_id: int) -> EmailResponse:
        async with self.uow:
            if not (user := await self.uow.user_repo.get(user_id=user_id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            if exist := await self.uow.email_repo.get(data=data):
                raise HTTPException(status_code=status.HTTP_200_OK)
            connected = await self.uow.email_repo.add(data=data, user_id=user_id)
        return EmailResponse.from_orm(connected)

    async def get_many(self, user_id: int) -> list[EmailResponse]:
        async with self.uow:
            if not (user := await self.uow.user_repo.get(user_id=user_id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            emails = await self.uow.email_repo.list(user_id=user_id)
        return [EmailResponse.from_orm(email) for email in emails]

    async def remove(self, email_id: int, user_id: int) -> bool:
        async with self.uow:
            if not (email := await self.uow.email_repo.get(email_id=email_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if email.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return await self.uow.email_repo.delete(email_id=email_id)


async def get_email_service(
    # cache: AbstractCache = Depends(get_cache),
    # TODO: добавить кеширование гет запросов
    session: AsyncSession = Depends(get_async_session),
) -> EmailService:
    uow = SqlAlchemyUnitOfWork(session=session)
    return EmailService(uow=uow)
