from poll.domain.interactors.user.state import UserStateInteractor
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.data.repository.repository import RepositoryInjector


class UserInteractorInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, repository: RepositoryInjector):
        super().__init__(cache)
        self.repository = repository

    def state(self) -> UserStateInteractor:
        return self._cache(UserStateInteractor, lambda: UserStateInteractor(
            self.repository.state()
        ))
