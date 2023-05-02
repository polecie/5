from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.email import EmailRepository
from src.repositories.sender import SenderRepository
from src.repositories.user import UserRepository
from src.uow.base import AbstractUnitOfWork

__all__ = ("SqlAlchemyUnitOfWork",)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo: UserRepository = UserRepository(session=self.session)
        self.email_repo: EmailRepository = EmailRepository(session=self.session)
        self.sender_repo: SenderRepository = SenderRepository(session=self.session)

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
