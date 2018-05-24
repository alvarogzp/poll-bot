from sqlite_framework.sql.item.column import Column
from sqlite_framework.sql.item.constants.operator import EQUAL
from sqlite_framework.sql.item.constants.order_mode import DESC
from sqlite_framework.sql.item.constants.type import INTEGER, TEXT
from sqlite_framework.sql.item.constraint.column.default import Default
from sqlite_framework.sql.item.constraint.column.simple import PRIMARY_KEY, NOT_NULL, UNIQUE
from sqlite_framework.sql.item.constraint.foreign_key.change import CASCADE
from sqlite_framework.sql.item.constraint.foreign_key.references import References
from sqlite_framework.sql.item.constraint.table.unique import Unique
from sqlite_framework.sql.item.expression.compound.condition import Condition
from sqlite_framework.sql.item.expression.constants import CURRENT_UNIX_TIMESTAMP
from sqlite_framework.sql.item.table import Table
from sqlite_framework.sql.statement.builder.insert import Insert
from sqlite_framework.sql.statement.builder.select import Select

from poll.data.data_source.sqlite.component.base import BasePollSqliteStorageComponent
from poll.data.data_source.sqlite.component.poll.poll import POLL
from poll.data.data_source.sqlite.model.poll.publication import PollPublicationData
from poll.domain.model.poll.group.publications import PollPublications
from poll.domain.model.poll.poll import Poll
from poll.domain.model.poll.publication import PollPublication


COMPONENT_NAME = "poll_publication"
COMPONENT_VERSION = 1


PUBLICATION_ID = Column("publication_id", INTEGER, PRIMARY_KEY, NOT_NULL)  # filled automatically
PUBLICATION = Column("publication_value", TEXT, UNIQUE, NOT_NULL)
POLL_ID = Column("poll", INTEGER, NOT_NULL, References(POLL, on_delete=CASCADE))
NUMBER = Column("number", INTEGER, NOT_NULL)
TIMESTAMP = Column("published_at", INTEGER, NOT_NULL, Default(CURRENT_UNIX_TIMESTAMP))


POLL_PUBLICATION = Table("poll_publication")
POLL_PUBLICATION.column(PUBLICATION_ID)
POLL_PUBLICATION.column(PUBLICATION)
POLL_PUBLICATION.column(POLL_ID)
POLL_PUBLICATION.column(NUMBER)
POLL_PUBLICATION.column(TIMESTAMP)
POLL_PUBLICATION.constraint(Unique(POLL_ID, NUMBER))


ADD_PUBLICATION = Insert()\
    .table(POLL_PUBLICATION)\
    .columns(PUBLICATION, POLL_ID, NUMBER)\
    .values(":publication", ":poll", ":number")\
    .build()

GET_LAST_NUMBER_FOR_POLL = Select()\
    .fields(NUMBER)\
    .table(POLL_PUBLICATION)\
    .where(Condition(POLL_ID, EQUAL, ":poll"))\
    .order_by(NUMBER, DESC)\
    .limit(1)\
    .build()

GET_POLL_FROM_PUBLICATION = Select()\
    .fields(POLL_ID)\
    .table(POLL_PUBLICATION)\
    .where(Condition(PUBLICATION, EQUAL, ":publication"))\
    .build()

GET_PUBLICATION_ID = Select()\
    .fields(PUBLICATION_ID)\
    .table(POLL_PUBLICATION)\
    .where(Condition(PUBLICATION, EQUAL, ":publication"))\
    .build()

GET_PUBLICATION_FROM_ID = Select()\
    .fields(PUBLICATION)\
    .table(POLL_PUBLICATION)\
    .where(Condition(PUBLICATION_ID, EQUAL, ":publication_id"))\
    .build()

GET_PUBLICATIONS = Select()\
    .fields(PUBLICATION)\
    .table(POLL_PUBLICATION)\
    .where(Condition(POLL_ID, EQUAL, ":poll"))\
    .order_by(NUMBER)\
    .build()


class PollPublicationSqliteComponent(BasePollSqliteStorageComponent):
    def __init__(self):
        super().__init__(COMPONENT_NAME, COMPONENT_VERSION)
        self.managed_tables(POLL_PUBLICATION)

    def new(self, poll: Poll, publication: PollPublication):
        number = self._get_next_number_for(poll)
        self.statement(ADD_PUBLICATION).execute(publication=publication.id, poll=poll.id, number=number)

    def _get_next_number_for(self, poll: Poll) -> int:
        last_number = self.statement(GET_LAST_NUMBER_FOR_POLL).execute(poll=poll.id).first_field()
        return self._next_number(last_number)

    def exists(self, publication: PollPublication) -> bool:
        poll = self.statement(GET_POLL_FROM_PUBLICATION).execute(publication=publication.id).first_field()
        return poll is not None

    def get_poll(self, publication: PollPublication) -> Poll:
        poll = self.statement(GET_POLL_FROM_PUBLICATION).execute(publication=publication.id).first_field()
        self._check_not_none(poll, "poll publication", publication.id)
        return Poll(poll)

    def get_id(self, publication: PollPublication) -> PollPublicationData:
        publication_id = self.statement(GET_PUBLICATION_ID).execute(publication=publication.id).first_field()
        self._check_not_none(publication_id, "poll publication", publication.id)
        return PollPublicationData(publication_id)

    def get_publication_from_id(self, publication: PollPublicationData) -> PollPublication:
        publication_id = self.statement(GET_PUBLICATION_FROM_ID).execute(publication_id=publication.id).first_field()
        self._check_not_none(publication_id, "poll publication id", publication.id)
        return PollPublication(publication_id)

    def get_publications(self, poll: Poll) -> PollPublications:
        publications = self.statement(GET_PUBLICATIONS)\
            .execute(poll=poll.id)\
            .map(lambda publication: PollPublication(
                publication[PUBLICATION]
            ))
        return PollPublications(tuple(publications))
