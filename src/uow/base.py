from abc import ABC, abstractmethod

from src.repositories.base import AbstractRepository

__all__ = ("AbstractUnitOfWork",)


class AbstractUnitOfWork(ABC):
    user_repo: AbstractRepository
    email_repo: AbstractRepository
    sender_repo: AbstractRepository

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, *args):
        try:
            await self.commit()
        except Exception:
            await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
