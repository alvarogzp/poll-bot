from bot.storage.data_source.data_sources.sqlite.sqlite import SqliteStorageDataSource
from sqlite_framework.log.logger import SqliteLogger
from sqlite_framework.session.session import SqliteSession

from poll.data.data_source.data_source import PollDataSource
from poll.data.data_source.sqlite.component.factory import SqlitePollComponentFactory
from poll.data.data_source.sqlite.component.poll.option import PollOptionSqliteComponent
from poll.data.data_source.sqlite.component.poll.poll import PollSqliteComponent
from poll.data.data_source.sqlite.component.poll.publication import PollPublicationSqliteComponent
from poll.data.data_source.sqlite.component.poll.vote.option import PollVoteOptionSqliteComponent
from poll.data.data_source.sqlite.component.user.state import UserStateSqliteComponent
from poll.data.data_source.sqlite.component.user.user import UserSqliteComponent
from poll.data.data_source.sqlite.model.mapper.all import SqliteModelMappers
from poll.domain.model.poll.full.poll import FullPoll, FullOptionPoll
from poll.domain.model.poll.group.votes import PollVotes
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import Poll, PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.poll.vote import OptionPollVote
from poll.domain.model.user.state import State
from poll.domain.model.user.user import User


DATABASE_FILENAME = "state/poll.db"


class SqlitePollDataSource(SqliteStorageDataSource, PollDataSource):
    def __init__(self, session: SqliteSession, logger: SqliteLogger):
        super().__init__(session, logger)
        self.user = None  # type: UserSqliteComponent
        self.user_state = None  # type: UserStateSqliteComponent
        self.poll = None  # type: PollSqliteComponent
        self.poll_option = None  # type: PollOptionSqliteComponent
        self.poll_publication = None  # type: PollPublicationSqliteComponent
        self.poll_vote_option = None  # type: PollVoteOptionSqliteComponent
        self.mappers = None  # type: SqliteModelMappers

    def init(self):
        super().init()
        self._init_components()

    def _init_components(self):
        factory = SqlitePollComponentFactory(self.session, self.logger)
        self.user = factory.user()
        self.user_state = factory.user_state()
        self.poll = factory.poll()
        self.poll_option = factory.poll_option()
        self.poll_publication = factory.poll_publication()
        self.poll_vote_option = factory.poll_vote_option()
        self.mappers = SqliteModelMappers(self.user, self.poll_option, self.poll_publication, self.poll_vote_option)

    def get_last_poll_from_user(self, user: User) -> PollNumber:
        return self.poll.get_last_from_user(user)

    def get_info(self, poll: Poll) -> PollInfo:
        info = self.poll.get_info(poll)
        return self.mappers.info.unmap_poll_info(info)

    def get_option_info(self, poll: Poll, option: PollOptionNumber) -> PollOptionInfo:
        return self.poll_option.get_info(poll, option)

    def get_from_user(self, user: User, poll: PollNumber) -> Poll:
        return self.poll.get_from_user(user, poll)

    def get_from_publication(self, publication: PollPublication) -> Poll:
        return self.poll_publication.get_poll(publication)

    def get_full_poll(self, poll: Poll) -> FullPoll:
        info = self.poll.get_info(poll)
        publications = self.poll_publication.get_publications(poll)
        full_options = self.poll_option.get_full_options(poll)
        return FullOptionPoll(
            self.mappers.info.unmap_poll_info(info),
            publications,
            self.mappers.option.unmap_full_options(full_options, poll)
        )

    def new_poll(self, info: PollInfo) -> PollNumber:
        poll_user_id = self.user.add_poll_user(info.owner)
        sqlite_info = self.mappers.info.map_poll_info(info, poll_user_id)
        return self.poll.new(sqlite_info, info.owner)

    def add_option(self, poll: Poll, option: PollOptionInfo) -> PollOptionNumber:
        return self.poll_option.add(poll, option)

    def complete(self, poll: Poll):
        self.poll.complete(poll)

    def delete(self, poll: Poll):
        self.poll.delete(poll)

    def publish(self, user: User, poll: PollNumber, publication: PollPublication):
        poll = self.poll.get_from_user(user, poll)
        self.poll_publication.new(poll, publication)

    def exists_publication(self, publication: PollPublication) -> bool:
        return self.poll_publication.exists(publication)

    def vote_option(self, vote: OptionPollVote):
        poll_user_id = self.user.add_poll_user(vote.user)
        vote = self.mappers.option_vote.map_option_vote(vote, poll_user_id)
        self.poll_vote_option.vote_option(vote)

    def unvote_option(self, vote: OptionPollVote):
        poll = self.poll_publication.get_poll(vote.publication)
        option = self.poll_option.get_id(poll, vote.option)
        self.poll_vote_option.unvote_option(vote.user, poll, option)

    def get_votes(self, poll: Poll, user: User) -> PollVotes:
        votes = self.poll_vote_option.get_user_votes(poll, user)
        return self.mappers.option_vote.unmap_option_votes(votes)

    def set_state(self, user: User, state: State):
        self.user.add_user(user)
        self.user_state.set(user, state)

    def get_state(self, user: User) -> State:
        return self.user_state.get(user)
