from src.repos.base import BaseRepository
from src.schemas.users import UserDTO


class UsersRepository(BaseRepository):
    schema = UserDTO
