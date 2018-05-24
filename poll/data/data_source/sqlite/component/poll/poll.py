from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.operator import EQUAL, AND
from sqlite_framework.sql.item.constants.order_mode import DESC
from sqlite_framework.sql.item.constants.type import INTEGER, TEXT
from sqlite_framework.sql.item.constraint.column.default import Default
from sqlite_framework.sql.item.constraint.column.simple import PRIMARY_KEY, NOT_NULL
from sqlite_framework.sql.item.constraint.foreign_key.change import CASCADE
from sqlite_framework.sql.item.constraint.foreign_key.references import References
from sqlite_framework.sql.item.constraint.table.unique import Unique
from sqlite_framework.sql.item.expression.compound.condition import Condition, MultipleCondition
from sqlite_framework.sql.item.expression.constants import CURRENT_UNIX_TIMESTAMP
from sqlite_framework.sql.item.table import Table
from sqlite_framework.sql.statement.builder.delete import Delete
from sqlite_framework.sql.statement.builder.insert import Insert
from sqlite_framework.sql.statement.builder.select import Select
from sqlite_framework.sql.statement.builder.update import Update

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.component.user.user import POLL_USER, POLL_USER_USER_ID, POLL_USER_ID
from poll.data.data_source.sqlite.model.poll.info import PollInfoData
from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.domain.model.poll.poll import Poll, PollNumber
from poll.domain.model.poll.settings.anonymity import PollAnonymity
from poll.domain.model.poll.settings.settings import PollSettings
from poll.domain.model.poll.settings.type import PollType
from poll.domain.model.user.user import User


NAME = "poll"
VERSION = 1


ID = Column("poll_id", INTEGER, PRIMARY_KEY, NOT_NULL)  # filled automatically
OWNER = Column("owner", INTEGER, NOT_NULL, References(POLL_USER, on_delete=CASCADE))
NUMBER = Column("number", INTEGER, NOT_NULL)
TYPE = Column("type", INTEGER, NOT_NULL)
ANONYMITY = Column("anonymity", INTEGER, NOT_NULL)
TITLE = Column("title", TEXT, NOT_NULL)
TIMESTAMP = Column("created_at", INTEGER, NOT_NULL, Default(CURRENT_UNIX_TIMESTAMP))
COMPLETE = Column("complete", INTEGER, NOT_NULL, Default(0, is_expr=False))


POLL = Table("poll")
POLL.column(ID)
POLL.column(OWNER)
POLL.column(NUMBER)
POLL.column(TYPE)
POLL.column(ANONYMITY)
POLL.column(TITLE)
POLL.column(TIMESTAMP)
POLL.column(COMPLETE)
POLL.constraint(Unique(OWNER, NUMBER))  # real constraint should be Unique(owner.user_id, number)


ADD_POLL = Insert()\
    .table(POLL)\
    .columns(OWNER, NUMBER, TYPE, ANONYMITY, TITLE)\
    .values(":owner", ":number", ":type", ":anonymity", ":title")\
    .build()

GET_FROM_USER = Select()\
    .fields(ID)\
    .table(POLL).join(POLL_USER, on=Condition(OWNER, EQUAL, POLL_USER_ID))\
    .where(
        MultipleCondition(
            AND,
            Condition(POLL_USER_USER_ID, EQUAL, ":user_id"),
            Condition(NUMBER, EQUAL, ":number")
        )
    )\
    .build()

GET_LAST_FROM_USER = Select()\
    .fields(NUMBER)\
    .table(POLL).join(POLL_USER, on=Condition(OWNER, EQUAL, POLL_USER_ID))\
    .where(Condition(POLL_USER_USER_ID, EQUAL, ":user_id"))\
    .order_by(NUMBER, DESC)\
    .limit(1)\
    .build()

GET_POLL = Select()\
    .fields(OWNER, TYPE, ANONYMITY, TITLE, COMPLETE)\
    .table(POLL)\
    .where(Condition(ID, EQUAL, ":id"))\
    .build()

GET_LAST_NUMBER_FOR_USER = Select()\
    .fields(NUMBER)\
    .table(POLL).join(POLL_USER, on=Condition(OWNER, EQUAL, POLL_USER_ID))\
    .where(Condition(POLL_USER_USER_ID, EQUAL, ":user_id"))\
    .order_by(NUMBER, DESC)\
    .limit(1)\
    .build()

SET_COMPLETE = Update()\
    .table(POLL)\
    .set(COMPLETE, 1)\
    .where(Condition(ID, EQUAL, ":id"))\
    .build()

DELETE_POLL = Delete()\
    .table(POLL)\
    .where(Condition(ID, EQUAL, ":id"))\
    .build()


class PollSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(NAME, VERSION)
        self.managed_tables(POLL)

    def get_from_user(self, user: User, poll: PollNumber) -> Poll:
        poll_id = self.statement(GET_FROM_USER).execute(user_id=user.id, number=poll.number).first_field()
        self._check_not_none(poll_id, "poll number", poll.number)
        return Poll(poll_id)

    def get_last_from_user(self, user: User) -> PollNumber:
        last_poll_number = self.statement(GET_LAST_FROM_USER).execute(user_id=user.id).first_field()
        self._check_not_none(last_poll_number, "last poll from user", user.id)
        return PollNumber(last_poll_number)

    def get_info(self, poll: Poll) -> PollInfoData:
        info = self.statement(GET_POLL).execute(id=poll.id).first()
        return PollInfoData(
            PollUserData(info[OWNER]),
            PollSettings(
                PollType(info[TYPE]),
                PollAnonymity(info[ANONYMITY])
            ),
            info[TITLE],
            bool(info[COMPLETE])
        )

    def new(self, info: PollInfoData, user: User) -> PollNumber:
        number = self._get_next_number_for(user)
        self.statement(ADD_POLL).execute(
            owner=info.owner.id, number=number, type=info.settings.type.type,
            anonymity=info.settings.anonymity.anonymity, title=info.title
        )
        return PollNumber(number)

    def _get_next_number_for(self, user: User) -> int:
        last_number = self.statement(GET_LAST_NUMBER_FOR_USER).execute(user_id=user.id).first_field()
        return self._next_number(last_number)

    def complete(self, poll: Poll):
        self.statement(SET_COMPLETE).execute(id=poll.id)

    def delete(self, poll: Poll):
        self.statement(DELETE_POLL).execute(id=poll.id)
