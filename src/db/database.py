from utils.decorators import singleton

from ._appeals import AppealsMixin
from ._connection import ConnectionMixin
from ._users import UsersMixin


@singleton
class DataBase(ConnectionMixin, UsersMixin, AppealsMixin):
    pass
