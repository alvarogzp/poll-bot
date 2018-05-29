from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.conflict_resolution import IGNORE
from sqlite_framework.sql.item.constants.operator import AND, EQUAL
from sqlite_framework.sql.item.constants.type import INTEGER, TEXT
from sqlite_framework.sql.item.constraint.column.simple import PRIMARY_KEY, NOT_NULL
from sqlite_framework.sql.item.constraint.foreign_key.change import CASCADE
from sqlite_framework.sql.item.constraint.foreign_key.references import References
from sqlite_framework.sql.item.constraint.table.unique import Unique
from sqlite_framework.sql.item.expression.compound.condition import MultipleCondition, Condition
from sqlite_framework.sql.item.table import Table
from sqlite_framework.sql.statement.builder.insert import Insert
from sqlite_framework.sql.statement.builder.select import Select

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.domain.model.poll.user import PollUser
from poll.domain.model.user.user import User


COMPONENT_NAME = "user"
COMPONENT_VERSION = 1


# USER table definition

ID = Column("user_id", INTEGER, PRIMARY_KEY, NOT_NULL)

USER = Table("user")
USER.column(ID)


# POLL_USER table definition

POLL_USER_ID = Column("poll_user_id", INTEGER, PRIMARY_KEY, NOT_NULL)  # to be filled automatically
POLL_USER_USER_ID = Column("user_id", INTEGER, NOT_NULL, References(USER, on_delete=CASCADE))
USERNAME = Column("username", TEXT, NOT_NULL)
NAME = Column("name", TEXT, NOT_NULL)

POLL_USER = Table("poll_user")
POLL_USER.column(POLL_USER_ID)
POLL_USER.column(POLL_USER_USER_ID)
POLL_USER.column(USERNAME)
POLL_USER.column(NAME)
POLL_USER.constraint(Unique(POLL_USER_USER_ID, USERNAME, NAME))


ADD_USER = Insert().or_(IGNORE)\
    .table(USER)\
    .columns(ID)\
    .values(":id")\
    .build()

ADD_POLL_USER = Insert().or_(IGNORE)\
    .table(POLL_USER)\
    .columns(POLL_USER_USER_ID, USERNAME, NAME)\
    .values(":user_id", ":username", ":name")\
    .build()

GET_POLL_USER_ID = Select()\
    .fields(POLL_USER_ID)\
    .table(POLL_USER)\
    .where(
        MultipleCondition(
            AND,
            Condition(POLL_USER_USER_ID, EQUAL, ":user_id"),
            Condition(USERNAME, EQUAL, ":username"),
            Condition(NAME, EQUAL, ":name")
        )
    )\
    .build()

GET_POLL_USER = Select()\
    .fields(POLL_USER_USER_ID, USERNAME, NAME)\
    .table(POLL_USER)\
    .where(Condition(POLL_USER_ID, EQUAL, ":id"))\
    .build()


class UserSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(COMPONENT_NAME, COMPONENT_VERSION)
        self.managed_tables(USER, POLL_USER)

    def add_user(self, user: User):
        self.statement(ADD_USER).execute(id=user.id)

    def add_poll_user(self, user: PollUser) -> PollUserData:
        self.add_user(user)
        username = self._empty_if_none(user.username)
        name = self._empty_if_none(user.name)
        self.statement(ADD_POLL_USER).execute(user_id=user.id, username=username, name=name)
        poll_user_id = self.statement(GET_POLL_USER_ID)\
            .execute(user_id=user.id, username=username, name=name)\
            .first_field()
        return PollUserData(poll_user_id)

    def get_poll_user(self, poll_user_id: PollUserData) -> PollUser:
        poll_user = self.statement(GET_POLL_USER).execute(id=poll_user_id.id).first()
        return PollUser(
            poll_user[POLL_USER_USER_ID],
            poll_user[USERNAME],
            poll_user[NAME]
        )
