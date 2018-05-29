from typing import Sequence

from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.operator import EQUAL, AND
from sqlite_framework.sql.item.constants.order_mode import DESC
from sqlite_framework.sql.item.constants.type import INTEGER, TEXT
from sqlite_framework.sql.item.constraint.column.simple import PRIMARY_KEY, NOT_NULL
from sqlite_framework.sql.item.constraint.foreign_key.change import CASCADE
from sqlite_framework.sql.item.constraint.foreign_key.references import References
from sqlite_framework.sql.item.constraint.table.unique import Unique
from sqlite_framework.sql.item.expression.compound.condition import Condition, MultipleCondition
from sqlite_framework.sql.item.table import Table
from sqlite_framework.sql.statement.builder.insert import Insert
from sqlite_framework.sql.statement.builder.select import Select

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.component.poll.poll import POLL
from poll.data.data_source.sqlite.model.poll.option import FullPollOptionData
from poll.domain.model.poll.option import PollOptionInfo, PollOption, PollOptionNumber
from poll.domain.model.poll.poll import Poll


COMPONENT_NAME = "poll_option"
COMPONENT_VERSION = 1


ID = Column("id", INTEGER, PRIMARY_KEY, NOT_NULL)  # filled automatically
POLL_ID = Column("poll", INTEGER, NOT_NULL, References(POLL, on_delete=CASCADE))
NUMBER = Column("number", INTEGER, NOT_NULL)
NAME = Column("name", TEXT, NOT_NULL)


POLL_OPTION = Table("poll_option")
POLL_OPTION.column(ID)
POLL_OPTION.column(POLL_ID)
POLL_OPTION.column(NUMBER)
POLL_OPTION.column(NAME)
POLL_OPTION.constraint(Unique(POLL_ID, NUMBER))


ADD_OPTION = Insert()\
    .table(POLL_OPTION)\
    .columns(POLL_ID, NUMBER, NAME)\
    .values(":poll", ":number", ":name")\
    .build()

GET_LAST_NUMBER_FOR_POLL = Select()\
    .fields(NUMBER)\
    .table(POLL_OPTION)\
    .where(Condition(POLL_ID, EQUAL, ":poll"))\
    .order_by(NUMBER, DESC)\
    .limit(1)\
    .build()

GET_FULL_POLL_OPTIONS = Select()\
    .fields(ID, NUMBER, NAME)\
    .table(POLL_OPTION)\
    .where(Condition(POLL_ID, EQUAL, ":poll"))\
    .order_by(NUMBER)\
    .build()

GET_OPTION_NUMBER = Select()\
    .fields(NUMBER)\
    .table(POLL_OPTION)\
    .where(Condition(ID, EQUAL, ":id"))\
    .build()

GET_OPTION_ID = Select()\
    .fields(ID)\
    .table(POLL_OPTION)\
    .where(
        MultipleCondition(
            AND,
            Condition(POLL_ID, EQUAL, ":poll"),
            Condition(NUMBER, EQUAL, ":number")
        )
    )\
    .build()

GET_OPTION_NAME = Select()\
    .fields(NAME)\
    .table(POLL_OPTION)\
    .where(
        MultipleCondition(
            AND,
            Condition(POLL_ID, EQUAL, ":poll"),
            Condition(NUMBER, EQUAL, ":number")
        )
    )\
    .build()


class PollOptionSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(COMPONENT_NAME, COMPONENT_VERSION)
        self.managed_tables(POLL_OPTION)

    def add(self, poll: Poll, option: PollOptionInfo) -> PollOptionNumber:
        number = self._get_next_number_for(poll)
        self.statement(ADD_OPTION).execute(poll=poll.id, number=number, name=option.name)
        return PollOptionNumber(number)

    def _get_next_number_for(self, poll: Poll) -> int:
        last_number = self.statement(GET_LAST_NUMBER_FOR_POLL).execute(poll=poll.id).first_field()
        return self._next_number(last_number)

    def get_full_options(self, poll: Poll) -> Sequence[FullPollOptionData]:
        options = self.statement(GET_FULL_POLL_OPTIONS)\
            .execute(poll=poll.id)\
            .map(lambda option: FullPollOptionData(
                PollOption(option[ID]),
                PollOptionNumber(option[NUMBER]),
                PollOptionInfo(option[NAME])
            ))
        return tuple(options)

    def get_number(self, option: PollOption) -> PollOptionNumber:
        number = self.statement(GET_OPTION_NUMBER).execute(id=option.id).first_field()
        self._check_not_none(number, "poll option id", option.id)
        return PollOptionNumber(number)

    def get_id(self, poll: Poll, option: PollOptionNumber) -> PollOption:
        option_id = self.statement(GET_OPTION_ID).execute(poll=poll.id, number=option.number).first_field()
        self._check_not_none(option_id, "poll option number", option.number)
        return PollOption(option_id)

    def get_info(self, poll: Poll, option: PollOptionNumber) -> PollOptionInfo:
        name = self.statement(GET_OPTION_NAME).execute(poll=poll.id, number=option.number).first_field()
        self._check_not_none("poll option number", option.number)
        return PollOptionInfo(name)
