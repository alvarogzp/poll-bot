from sqlite_framework.log.logger import SqliteLogger
from sqlite_framework.session.session import SqliteSession

from poll.data.data_source.data_source import PollDataSource
from poll.data.data_source.sqlite.sqlite import SqlitePollDataSource
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector


class DataSourceInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, database_filename: str, debug: bool, logger: SqliteLogger):
        super().__init__(cache)
        self.database_filename = database_filename
        self.debug = debug
        self.logger = logger

    def data_source(self) -> PollDataSource:
        return self._cache(PollDataSource, lambda: SqlitePollDataSource(
            self._session(),
            self.logger
        ))

    def _session(self) -> SqliteSession:
        return self._cache(SqliteSession, lambda: SqliteSession(
            self.database_filename,
            self.debug,
            enable_foreign_keys=True
        ))
