from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.conflict_resolution import REPLACE
from sqlite_framework.sql.item.constants.operator import EQUAL
from sqlite_framework.sql.item.constants.type import INTEGER
from sqlite_framework.sql.item.constraint.column.default import Default
from sqlite_framework.sql.item.constraint.column.simple import PRIMARY_KEY, NOT_NULL
from sqlite_framework.sql.item.constraint.foreign_key.change import CASCADE
from sqlite_framework.sql.item.constraint.foreign_key.references import References
from sqlite_framework.sql.item.expression.compound.condition import Condition
from sqlite_framework.sql.item.expression.constants import CURRENT_UNIX_TIMESTAMP
from sqlite_framework.sql.item.table import Table
from sqlite_framework.sql.statement.builder.insert import Insert
from sqlite_framework.sql.statement.builder.select import Select

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.component.user.user import USER
from poll.domain.model.user.state import State, DEFAULT_STATE
from poll.domain.model.user.user import User


COMPONENT_NAME = "user_state"
COMPONENT_VERSION = 1


ID = Column("user_id", INTEGER, PRIMARY_KEY, NOT_NULL, References(USER, on_delete=CASCADE))
STATE_VALUE = Column("state", INTEGER, NOT_NULL)
TIMESTAMP = Column("changed_at", INTEGER, NOT_NULL, Default(CURRENT_UNIX_TIMESTAMP))

USER_STATE = Table("user_state")
USER_STATE.column(ID)
USER_STATE.column(STATE_VALUE)
USER_STATE.column(TIMESTAMP)


SET_STATE = Insert().or_(REPLACE)\
    .table(USER_STATE)\
    .columns(ID, STATE_VALUE)\
    .values(":user_id", ":state")\
    .build()

GET_STATE = Select()\
    .fields(STATE_VALUE)\
    .table(USER_STATE)\
    .where(Condition(ID, EQUAL, ":user_id"))\
    .build()


class UserStateSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(COMPONENT_NAME, COMPONENT_VERSION)
        self.managed_tables(USER_STATE)

    def set(self, user: User, state: State):
        self.statement(SET_STATE).execute(user_id=user.id, state=state.id)

    def get(self, user: User) -> State:
        state = self.statement(GET_STATE).execute(user_id=user.id).first_field()
        if state is None:
            return DEFAULT_STATE
        return State(state)
