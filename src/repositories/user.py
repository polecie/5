from src.api.v1.schemas.users import UserRequest
from src.repositories.base import AbstractRepository
from dataclasses import dataclass
from src.models import User
from sqlalchemy import select

__all__ = ("UserRepository",)


@dataclass
class UserRepository(AbstractRepository):
    model: type[User] = User

    async def add(self, user: UserRequest) -> User:  # модель из базы
        new_user = User(**user.dict())
        self.session.add(new_user)
        return new_user

    async def _get(self, user_id: int) -> User | None:
        statement = select(self.model).where(self.model.id == user_id)  # type: ignore
        response = await self.session.execute(statement)
        return response.scalars().one_or_none()

    async def get(self, user_id: int) -> User | None:
        return await self._get(user_id=user_id)

    async def delete(self, *args, **kwargs):
        pass

    async def list(self,) -> list[User]:
        statement = select(self.model)
        response = await self.session.execute(statement)
        return response.scalars().all()  # type: ignore
