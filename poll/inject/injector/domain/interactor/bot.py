from poll.domain.interactors.bot.manage import BotManagePollInteractor
from poll.domain.interactors.bot.search import BotSearchPollInteractor
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.domain.interactor.poll import PollInteractorInjector
from poll.inject.injector.domain.interactor.user import UserInteractorInjector


class BotInteractorInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, user: UserInteractorInjector, poll: PollInteractorInjector):
        super().__init__(cache)
        self.user = user
        self.poll = poll

    def manage(self) -> BotManagePollInteractor:
        return self._cache(BotManagePollInteractor, lambda: BotManagePollInteractor(
            self.poll.manage(),
            self.poll.get(),
            self.user.state()
        ))

    def search(self) -> BotSearchPollInteractor:
        return self._cache(BotSearchPollInteractor, lambda: BotSearchPollInteractor(
            self.poll.get()
        ))
