from typing import Iterable

from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.operator import EQUAL, AND, IN
from sqlite_framework.sql.item.constants.order_mode import DESC
from sqlite_framework.sql.item.constants.type import INTEGER
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

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.component.poll.option import POLL_OPTION
from poll.data.data_source.sqlite.component.poll.publication import POLL_PUBLICATION, POLL_ID, PUBLICATION_ID
from poll.data.data_source.sqlite.component.user.user import POLL_USER, POLL_USER_USER_ID, POLL_USER_ID
from poll.data.data_source.sqlite.model.poll.publication import PollPublicationData
from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.data.data_source.sqlite.model.poll.vote import OptionPollVoteData
from poll.domain.model.poll.option import PollOption
from poll.domain.model.poll.poll import Poll
from poll.domain.model.user.user import User


COMPONENT_NAME = "poll_vote_option"
COMPONENT_VERSION = 1


ID = Column("id", INTEGER, PRIMARY_KEY, NOT_NULL)  # filled automatically
USER = Column("user", INTEGER, NOT_NULL, References(POLL_USER, on_delete=CASCADE))
PUBLICATION = Column("publication", INTEGER, NOT_NULL, References(POLL_PUBLICATION, on_delete=CASCADE))
OPTION = Column("option", INTEGER, NOT_NULL, References(POLL_OPTION, on_delete=CASCADE))
NUMBER = Column("poll_vote_number", INTEGER, NOT_NULL)
TIMESTAMP = Column("timestamp", INTEGER, NOT_NULL, Default(CURRENT_UNIX_TIMESTAMP))


POLL_VOTE_OPTION = Table("poll_vote_option")
POLL_VOTE_OPTION.column(ID)
POLL_VOTE_OPTION.column(USER)
POLL_VOTE_OPTION.column(PUBLICATION)
POLL_VOTE_OPTION.column(OPTION)
POLL_VOTE_OPTION.column(NUMBER)
POLL_VOTE_OPTION.column(TIMESTAMP)
# real constraint should be Unique(user.user_id, publication, option)
POLL_VOTE_OPTION.constraint(Unique(USER, PUBLICATION, OPTION))
# real constraint should be Unique(poll, number)
POLL_VOTE_OPTION.constraint(Unique(PUBLICATION, NUMBER))


ADD_VOTE = Insert()\
    .table(POLL_VOTE_OPTION)\
    .columns(USER, PUBLICATION, OPTION, NUMBER)\
    .values(":user", ":publication", ":option", ":number")\
    .build()

GET_LAST_NUMBER_FOR_POLL = Select()\
    .fields(NUMBER)\
    .table(POLL_VOTE_OPTION).join(POLL_PUBLICATION, on=Condition(PUBLICATION, EQUAL, PUBLICATION_ID))\
    .where(Condition(POLL_ID, EQUAL,
                     Select()
                     .fields(POLL_ID)
                     .table(POLL_PUBLICATION)
                     .where(Condition(PUBLICATION_ID, EQUAL, ":publication"))
                     ))\
    .order_by(NUMBER, DESC)\
    .limit(1)\
    .build()

REMOVE_VOTE = Delete()\
    .table(POLL_VOTE_OPTION)\
    .where(
        MultipleCondition(
            AND,
            Condition(USER, IN,
                      Select()
                      .fields(POLL_USER_ID)
                      .table(POLL_USER)
                      .where(Condition(POLL_USER_USER_ID, EQUAL, ":user_id"))
                      ),
            Condition(PUBLICATION, IN,
                      Select()
                      .fields(PUBLICATION_ID)
                      .table(POLL_PUBLICATION)
                      .where(Condition(POLL_ID, EQUAL, ":poll_id"))
                      ),
            Condition(OPTION, EQUAL, ":option")
        )
    )\
    .build()

GET_USER_VOTES = Select()\
    .fields(USER, PUBLICATION, OPTION)\
    .table(POLL_VOTE_OPTION)\
    .join(POLL_USER, on=Condition(USER, EQUAL, POLL_USER_ID))\
    .join(POLL_PUBLICATION, on=Condition(PUBLICATION, EQUAL, PUBLICATION_ID))\
    .where(
        MultipleCondition(
            AND,
            Condition(POLL_USER_USER_ID, EQUAL, ":user_id"),
            Condition(POLL_ID, EQUAL, ":poll_id")
        )
    )\
    .order_by(NUMBER)\
    .build()

GET_OPTION_VOTES = Select()\
    .fields(USER, PUBLICATION)\
    .table(POLL_VOTE_OPTION)\
    .join(POLL_PUBLICATION, on=Condition(PUBLICATION, EQUAL, PUBLICATION_ID))\
    .where(
        MultipleCondition(
            AND,
            Condition(POLL_ID, EQUAL, ":poll_id"),
            Condition(OPTION, EQUAL, ":option")
        )
    )\
    .order_by(NUMBER)\
    .build()


class PollVoteOptionSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(COMPONENT_NAME, COMPONENT_VERSION)
        self.managed_tables(POLL_VOTE_OPTION)

    def vote_option(self, vote: OptionPollVoteData):
        number = self._get_next_number_for(vote)
        self.statement(ADD_VOTE).execute(
            user=vote.user.id, publication=vote.publication.id, option=vote.option.id, number=number
        )

    def _get_next_number_for(self, vote: OptionPollVoteData) -> int:
        last_number = self.statement(GET_LAST_NUMBER_FOR_POLL).execute(publication=vote.publication.id).first_field()
        return self._next_number(last_number)

    def unvote_option(self, user: User, poll: Poll, option: PollOption):
        self.statement(REMOVE_VOTE).execute(user_id=user.id, poll_id=poll.id, option=option.id)

    def get_user_votes(self, poll: Poll, user: User) -> Iterable[OptionPollVoteData]:
        votes = self.statement(GET_USER_VOTES)\
            .execute(poll_id=poll.id, user_id=user.id)\
            .map(lambda vote: OptionPollVoteData(
                PollUserData(vote[USER]),
                PollPublicationData(vote[PUBLICATION]),
                PollOption(vote[OPTION])
            ))
        return tuple(votes)

    def get_option_votes(self, poll: Poll, option: PollOption) -> Iterable[OptionPollVoteData]:
        votes = self.statement(GET_OPTION_VOTES)\
            .execute(poll_id=poll.id, option=option.id)\
            .map(lambda vote: OptionPollVoteData(
                PollUserData(vote[USER]),
                PollPublicationData(vote[PUBLICATION]),
                option
            ))
        return tuple(votes)
