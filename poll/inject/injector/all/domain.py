from bot.multithreading.worker import Worker
from sqlite_framework.log.logger import SqliteLogger

from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.data.repository.data_source import DataSourceInjector
from poll.inject.injector.data.repository.repository import RepositoryInjector
from poll.inject.injector.domain.check import CheckInjector
from poll.inject.injector.domain.interactor.poll import PollInteractorInjector
from poll.inject.injector.domain.interactor.bot import BotInteractorInjector
from poll.inject.injector.domain.interactor.user import UserInteractorInjector


class DomainInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, debug: bool, database_filename: str, sqlite_logger: SqliteLogger,
                 sqlite_worker: Worker):
        super().__init__(cache)
        self.debug = debug
        self.database_filename = database_filename
        self.sqlite_logger = sqlite_logger
        self.sqlite_worker = sqlite_worker

    def poll_interactor(self) -> PollInteractorInjector:
        return self._cache(PollInteractorInjector, lambda: PollInteractorInjector(
            self.cache,
            self.repository(),
            self._check()
        ))

    def bot_interactor(self) -> BotInteractorInjector:
        return self._cache(BotInteractorInjector, lambda: BotInteractorInjector(
            self.cache,
            self.user_interactor(),
            self.poll_interactor()
        ))

    def user_interactor(self) -> UserInteractorInjector:
        return self._cache(UserInteractorInjector, lambda: UserInteractorInjector(
            self.cache,
            self.repository()
        ))

    def _check(self) -> CheckInjector:
        return self._cache(CheckInjector, lambda: CheckInjector(
            self.cache,
            self.repository()
        ))

    def repository(self) -> RepositoryInjector:
        return self._cache(RepositoryInjector, lambda: RepositoryInjector(
            self.cache,
            self._data_source(),
            self.sqlite_worker
        ))

    def _data_source(self) -> DataSourceInjector:
        return self._cache(DataSourceInjector, lambda: DataSourceInjector(
            self.cache,
            self.database_filename,
            self.debug,
            self.sqlite_logger
        ))
