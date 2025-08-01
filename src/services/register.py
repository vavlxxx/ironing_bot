from src.services.base import BaseService
from src.utils.exceptions import UserNotFoundException
from src.schemas.users import UserRequestDTO


class RegisterService(BaseService):

    async def get_user_by(self, **fields):
        await self.db.rollback()
        user = await self.db.users.get_one_or_none(**fields)
        if user is None:
            raise UserNotFoundException
        return user
    
    async def create_user(self, phone, telegram_id):
        await self.db.rollback()
        user = UserRequestDTO(telegram_id=telegram_id, phone=phone)
        await self.db.users.add(user)
        self.db.commit()
    
    async def update_user(self, phone, telegram_id):
        await self.db.rollback()
        user = UserRequestDTO(telegram_id=telegram_id, phone=phone)
        await self.db.users.edit(user, phone=phone)
        await self.db.commit()
    