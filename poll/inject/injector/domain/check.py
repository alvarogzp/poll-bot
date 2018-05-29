from poll.domain.check.complete import CompletePollCheck
from poll.domain.check.exists_publication import ExistsPublicationPollCheck
from poll.domain.check.unique_vote import UniqueVotePollCheck
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.data.repository.repository import RepositoryInjector


class CheckInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, repository: RepositoryInjector):
        super().__init__(cache)
        self.repository = repository

    def complete(self) -> CompletePollCheck:
        return self._cache(CompletePollCheck, lambda: CompletePollCheck())

    def exists(self) -> ExistsPublicationPollCheck:
        return self._cache(ExistsPublicationPollCheck, lambda: ExistsPublicationPollCheck(
            self.repository.publish()
        ))

    def unique(self) -> UniqueVotePollCheck:
        return self._cache(UniqueVotePollCheck, lambda: UniqueVotePollCheck())
