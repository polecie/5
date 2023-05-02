from fastapi import Depends

from src.api.v1.schemas.users import UserRequest, UserResponse
from src.db import get_async_session
from src.services.mixin import ServiceMixin
from sqlalchemy.ext.asyncio import AsyncSession
from src.uow import SqlAlchemyUnitOfWork
from fastapi import status, HTTPException

__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):
    async def create(self, user: UserRequest) -> UserResponse:
        async with self.uow:
            if user_exist := await self.uow.user_repo.get(user_id=user.id):
                raise HTTPException(status_code=status.HTTP_200_OK, detail="user already exist")
            new_user = await self.uow.user_repo.add(user=user)
        return UserResponse.from_orm(new_user)

    async def get_one(self, user_id: int) -> UserResponse:
        async with self.uow:
            if not (user := await self.uow.user_repo.get(user_id=user_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return UserResponse.from_orm(user)

    async def get_many(self) -> list[UserResponse]:
        async with self.uow:
            users = await self.uow.user_repo.list()
        return [UserResponse.from_orm(user) for user in users]


async def get_user_service(
    # cache: AbstractCache = Depends(get_cache),
    # TODO: добавить кеширование гет запросов
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    uow = SqlAlchemyUnitOfWork(session=session)
    return UserService(uow=uow)
