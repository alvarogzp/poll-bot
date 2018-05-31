from bot.api.api import Api
from bot.logger.logger import Logger
from bot.multithreading.worker import Worker

from poll.inject.injector.all.domain import DomainInjector
from poll.inject.injector.all.telegram import TelegramInjector
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.data.repository.logger import SqliteLoggerInjector
from poll.inject.injector.presentation.telegram.formatter.log import LogFormatterInjector
from poll.inject.injector.presentation.telegram.logger import LoggerInjector
from poll.inject.injector.presentation.telegram.mapper import TelegramMapperInjector


class Injector(BaseInjector):
    def __init__(self, api: Api, debug: bool, database_filename: str, sqlite_worker: Worker, logger: Logger):
        super().__init__(InjectorCache())
        self.api = api
        self.debug = debug
        self.database_filename = database_filename
        self.sqlite_worker = sqlite_worker
        self.logger = logger

    def telegram(self) -> TelegramInjector:
        return self._cache(TelegramInjector, lambda: TelegramInjector(
            self.cache,
            self.domain(),
            self._telegram_mapper(),
            self.api
        ))

    def domain(self) -> DomainInjector:
        return self._cache(DomainInjector, lambda: DomainInjector(
            self.cache,
            self.debug,
            self.database_filename,
            self._sqlite_logger().sqlite(),
            self.sqlite_worker
        ))

    def _sqlite_logger(self) -> SqliteLoggerInjector:
        return self._cache(SqliteLoggerInjector, lambda: SqliteLoggerInjector(
            self.cache,
            self._logger()
        ))

    def _logger(self) -> LoggerInjector:
        return self._cache(LoggerInjector, lambda: LoggerInjector(
            self.cache,
            self._log_formatter(),
            self.logger
        ))

    def _log_formatter(self) -> LogFormatterInjector:
        return self._cache(LogFormatterInjector, lambda: LogFormatterInjector(
            self.cache,
            self._telegram_mapper()
        ))

    def _telegram_mapper(self) -> TelegramMapperInjector:
        return self._cache(TelegramMapperInjector, lambda: TelegramMapperInjector(
            self.cache
        ))
