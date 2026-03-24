from utils.decorators import singleton

from ._admins import AdminMixin
from ._appeals import AppealsMixin
from ._connection import ConnectionMixin
from ._users import UsersMixin
from ._role_invites import RoleInvitesMixin
from ._moderators import ModeratorsMixin
from ._medias import MediasMixin


@singleton
class DataBase(ConnectionMixin, UsersMixin, AppealsMixin, RoleInvitesMixin, ModeratorsMixin, AdminMixin, MediasMixin):
    pass
