from bot.multithreading.worker import Worker

from poll.data.repository import PollDataRepository, PollDataRepositoryFactory
from poll.domain.repository.poll.get import GetPollRepository
from poll.domain.repository.poll.manage import ManagePollRepository
from poll.domain.repository.poll.publish import PublishPollRepository
from poll.domain.repository.poll.vote import VotePollRepository
from poll.domain.repository.state import UserStateRepository
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.data.repository.data_source import DataSourceInjector


class RepositoryInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, data_source: DataSourceInjector, worker: Worker):
        super().__init__(cache)
        self.data_source = data_source
        self.worker = worker

    def manage(self) -> ManagePollRepository:
        return self.poll_data_repository()

    def get(self) -> GetPollRepository:
        return self.poll_data_repository()

    def publish(self) -> PublishPollRepository:
        return self.poll_data_repository()

    def vote(self) -> VotePollRepository:
        return self.poll_data_repository()

    def state(self) -> UserStateRepository:
        return self.poll_data_repository()

    def poll_data_repository(self) -> PollDataRepository:
        return self._cache(PollDataRepository, lambda: PollDataRepositoryFactory.repository(
            self.data_source.data_source(),
            self.worker
        ))
