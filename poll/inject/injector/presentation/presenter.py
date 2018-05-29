from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.domain.interactor.poll import PollInteractorInjector
from poll.inject.injector.domain.interactor.bot import BotInteractorInjector
from poll.inject.injector.presentation.mapper import MapperInjector
from poll.inject.injector.presentation.telegram.view import ViewInjector
from poll.presentation.presenter.manage import ManagePollPresenter
from poll.presentation.presenter.publish import PublishPollPresenter
from poll.presentation.presenter.search import SearchPollPresenter
from poll.presentation.presenter.vote import VotePollPresenter


class PresenterInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, bot_interactor: BotInteractorInjector,
                 poll_interactor: PollInteractorInjector, view: ViewInjector, mapper: MapperInjector):
        super().__init__(cache)
        self.bot_interactor = bot_interactor
        self.poll_interactor = poll_interactor
        self.view = view
        self.mapper = mapper

    def manage(self) -> ManagePollPresenter:
        return self._cache(ManagePollPresenter, lambda: ManagePollPresenter(
            self.view.manage(),
            self.bot_interactor.manage(),
            self.poll_interactor.get(),
            self.mapper.user(),
            self.mapper.poll_number(),
            self.mapper.poll_option_number(),
            self.mapper.poll_settings(),
            self.mapper.poll_info(),
            self.mapper.full_poll()
        ))

    def search(self) -> SearchPollPresenter:
        return self._cache(SearchPollPresenter, lambda: SearchPollPresenter(
            self.view.search(),
            self.bot_interactor.search(),
            self.mapper.poll_number(),
            self.mapper.full_poll()
        ))

    def publish(self) -> PublishPollPresenter:
        return self._cache(PublishPollPresenter, lambda: PublishPollPresenter(
            self.view.publish(),
            self.poll_interactor.publish(),
            self.mapper.poll_number(),
            self.mapper.poll_publication()
        ))

    def vote(self) -> VotePollPresenter:
        return self._cache(VotePollPresenter, lambda: VotePollPresenter(
            self.view.vote(),
            self.poll_interactor.vote(),
            self.poll_interactor.get(),
            self.mapper.user(),
            self.mapper.poll_publication(),
            self.mapper.poll_option_number(),
            self.mapper.full_poll()
        ))
