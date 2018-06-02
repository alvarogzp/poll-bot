from sqlite_framework.component.factory import SqliteStorageComponentFactory

from poll.data.data_source.sqlite.component.poll.option import PollOptionSqliteComponent
from poll.data.data_source.sqlite.component.poll.poll import PollSqliteComponent
from poll.data.data_source.sqlite.component.poll.publication import PollPublicationSqliteComponent
from poll.data.data_source.sqlite.component.poll.vote.option import PollVoteOptionSqliteComponent
from poll.data.data_source.sqlite.component.user.settings import UserSettingsSqliteComponent
from poll.data.data_source.sqlite.component.user.state import UserStateSqliteComponent
from poll.data.data_source.sqlite.component.user.user import UserSqliteComponent


class SqlitePollComponentFactory(SqliteStorageComponentFactory):
    def user(self):
        return self._initialized(UserSqliteComponent())

    def user_state(self):
        return self._initialized(UserStateSqliteComponent())

    def user_settings(self):
        return self._initialized(UserSettingsSqliteComponent())

    def poll(self):
        return self._initialized(PollSqliteComponent())

    def poll_option(self):
        return self._initialized(PollOptionSqliteComponent())

    def poll_publication(self):
        return self._initialized(PollPublicationSqliteComponent())

    def poll_vote_option(self):
        return self._initialized(PollVoteOptionSqliteComponent())
