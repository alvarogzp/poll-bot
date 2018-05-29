from sqlite_framework.log.logger import SqliteLogger

from poll.data.data_source.sqlite.logger import PollLoggerAdapter
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.presentation.telegram.logger import LoggerInjector


class SqliteLoggerInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, logger: LoggerInjector):
        super().__init__(cache)
        self.logger = logger

    def sqlite(self) -> SqliteLogger:
        return self._cache(SqliteLogger, lambda: PollLoggerAdapter(
            self.logger.poll()
        ))
