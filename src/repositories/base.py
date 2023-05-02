from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

__all__ = ("AbstractRepository",)


@dataclass
class AbstractRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def add(self, *args, **kwargs):
        """"""

    @abstractmethod
    async def get(self, *args, **kwargs):
        """"""

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """"""

    @abstractmethod
    async def list(self, *args, **kwargs):
        """"""
