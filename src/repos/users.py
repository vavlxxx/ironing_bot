from src.repos.base import BaseRepository
from schemas.users import UserDTO


class UsersRepository(BaseRepository):
    schema = UserDTO
