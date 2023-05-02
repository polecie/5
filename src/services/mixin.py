from abc import ABC
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

# from src.db import fake
# from src.db.base import AbstractCache

__all__ = ("ServiceMixin",)

from src.uow import AbstractUnitOfWork


@dataclass
class ServiceMixin(ABC):
    # cache: AbstractCache
    uow: AbstractUnitOfWork

    # def __post_init__(self):
    #     if self.cache is None:
    #         self.cache = fake.FakeCache()
