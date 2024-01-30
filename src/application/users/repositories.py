from application.repositories import TortoiseRepository
from application.users.models import User


class UserRepository(TortoiseRepository):
    model_class = User

    async def retrieve_by_email(self, reference):
        return await self.model_class.get_or_none(email=reference)
