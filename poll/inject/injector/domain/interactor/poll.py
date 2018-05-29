from poll.domain.interactors.poll.get import GetPollInteractor
from poll.domain.interactors.poll.manage import ManagePollInteractor
from poll.domain.interactors.poll.publish import PublishPollInteractor
from poll.domain.interactors.poll.vote import VotePollInteractor
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.domain.check import CheckInjector
from poll.inject.injector.data.repository.repository import RepositoryInjector


class PollInteractorInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, repository: RepositoryInjector, check: CheckInjector):
        super().__init__(cache)
        self.repository = repository
        self.check = check

    def manage(self) -> ManagePollInteractor:
        return self._cache(ManagePollInteractor, lambda: ManagePollInteractor(
            self.repository.manage(),
            self.repository.get(),
            self.check.complete()
        ))

    def get(self) -> GetPollInteractor:
        return self._cache(GetPollInteractor, lambda: GetPollInteractor(
            self.repository.get(),
            self.check.complete()
        ))

    def publish(self) -> PublishPollInteractor:
        return self._cache(PublishPollInteractor, lambda: PublishPollInteractor(
            self.repository.publish(),
            self.check.exists()
        ))

    def vote(self) -> VotePollInteractor:
        return self._cache(VotePollInteractor, lambda: VotePollInteractor(
            self.repository.vote(),
            self.repository.get(),
            self.check.unique()
        ))
