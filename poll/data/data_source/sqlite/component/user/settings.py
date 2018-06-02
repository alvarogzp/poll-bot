from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.conflict_resolution import IGNORE
from sqlite_framework.sql.item.constants.operator import EQUAL
from sqlite_framework.sql.item.constants.type import INTEGER
from sqlite_framework.sql.item.constraint.column.default import Default
from sqlite_framework.sql.item.constraint.column.simple import PRIMARY_KEY, NOT_NULL
from sqlite_framework.sql.item.constraint.foreign_key.change import CASCADE
from sqlite_framework.sql.item.constraint.foreign_key.references import References
from sqlite_framework.sql.item.expression.compound.condition import Condition
from sqlite_framework.sql.item.table import Table
from sqlite_framework.sql.statement.builder.insert import Insert
from sqlite_framework.sql.statement.builder.select import Select
from sqlite_framework.sql.statement.builder.update import Update

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.component.user.user import USER
from poll.domain.model.poll.settings.anonymity import PollAnonymity
from poll.domain.model.poll.settings.settings import DEFAULT_SETTINGS, PollSettings
from poll.domain.model.poll.settings.type import PollType
from poll.domain.model.user.settings import UserSettings
from poll.domain.model.user.user import User


COMPONENT_NAME = "user_settings"
COMPONENT_VERSION = 1


ID = Column("user_id", INTEGER, PRIMARY_KEY, NOT_NULL, References(USER, on_delete=CASCADE))
POLL_TYPE = Column("poll_type", INTEGER, NOT_NULL, Default(DEFAULT_SETTINGS.type.type, is_expr=False))
POLL_ANONYMITY = Column("poll_anonymity", INTEGER, NOT_NULL, Default(DEFAULT_SETTINGS.anonymity.anonymity, is_expr=False))

USER_SETTINGS = Table("user_settings")
USER_SETTINGS.column(ID)
USER_SETTINGS.column(POLL_TYPE)
USER_SETTINGS.column(POLL_ANONYMITY)


ADD_USER_SETTINGS = Insert().or_(IGNORE)\
    .table(USER_SETTINGS)\
    .columns(ID)\
    .values(":user_id")\
    .build()

SET_POLL_TYPE = Update()\
    .table(USER_SETTINGS)\
    .set(POLL_TYPE, ":type")\
    .where(Condition(ID, EQUAL, ":user_id"))\
    .build()

SET_POLL_ANONYMITY = Update()\
    .table(USER_SETTINGS)\
    .set(POLL_ANONYMITY, ":anonymity")\
    .where(Condition(ID, EQUAL, ":user_id"))\
    .build()

GET_SETTINGS = Select()\
    .fields(POLL_TYPE, POLL_ANONYMITY)\
    .table(USER_SETTINGS)\
    .where(Condition(ID, EQUAL, ":user_id"))\
    .build()


class UserSettingsSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(COMPONENT_NAME, COMPONENT_VERSION)
        self.managed_tables(USER_SETTINGS)

    def set_poll_type(self, user: User, poll_type: PollType):
        self.statement(SET_POLL_TYPE).execute(user_id=user.id, type=poll_type.type)

    def set_poll_anonymity(self, user: User, anonymity: PollAnonymity):
        self.statement(SET_POLL_ANONYMITY).execute(user_id=user.id, anonymity=anonymity.anonymity)

    def _add_user_settings(self, user: User):
        self.statement(ADD_USER_SETTINGS).execute(user_id=user.id)

    def get(self, user: User) -> UserSettings:
        settings = self.statement(GET_SETTINGS).execute(user_id=user.id).first()
        if settings is not None:
            settings = PollSettings(
                PollType(settings[POLL_TYPE]),
                PollAnonymity(settings[POLL_ANONYMITY])
            )
        else:
            settings = DEFAULT_SETTINGS
        return UserSettings(settings)
