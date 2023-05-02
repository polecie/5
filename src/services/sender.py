from fastapi import status, HTTPException
from fastapi import Depends

from src.api.v1.schemas.senders import SenderRequest
from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.uow import SqlAlchemyUnitOfWork
from src.api.v1.schemas.senders import SenderResponse
from src.services.mixin import ServiceMixin

__all__ = ("SenderService", "get_sender_service")


class SenderService(ServiceMixin):
    async def create(self, data: SenderRequest, user_id: int) -> SenderResponse:
        async with self.uow:
            if not (user := await self.uow.user_repo.get(user_id=user_id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            if not (email := await self.uow.email_repo.list(user_id=user_id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            if exist := await self.uow.sender_repo.get(data=data):
                raise HTTPException(status_code=status.HTTP_200_OK)
            connected = await self.uow.sender_repo.add(data=data, user_id=user_id)
            print(connected)
        return SenderResponse.from_orm(connected)

    async def get_many(self, user_id: int) -> list[SenderResponse]:
        async with self.uow:
            if not (user := await self.uow.user_repo.get(user_id=user_id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            senders = await self.uow.sender_repo.list(user_id=user_id)
        return [SenderResponse.from_orm(sender) for sender in senders]

    async def remove(self, sender_id: int, user_id: int) -> bool:
        async with self.uow:
            if not (sender := await self.uow.sender_repo.get(sender_id=sender_id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            if sender.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return await self.uow.sender_repo.delete(sender_id=sender_id)


async def get_sender_service(
    # cache: AbstractCache = Depends(get_cache),
    # TODO: добавить кеширование гет запросов
    session: AsyncSession = Depends(get_async_session),
) -> SenderService:
    uow = SqlAlchemyUnitOfWork(session=session)
    return SenderService(uow=uow)
