from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.presentation.presenter import PresenterInjector
from poll.inject.injector.presentation.telegram.mapper import TelegramMapperInjector
from poll.presentation.telegram.bot.action.inline.callback import PublishedPollAction
from poll.presentation.telegram.bot.action.inline.chosen import ChosenPollAction
from poll.presentation.telegram.bot.action.inline.query import SearchPollAction
from poll.presentation.telegram.bot.action.manage.base import BaseManageAction


class TelegramActionInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, presenter: PresenterInjector, telegram_mapper: TelegramMapperInjector):
        super().__init__(cache)
        self.presenter = presenter
        self.telegram_mapper = telegram_mapper

    def manage(self, action: BaseManageAction):
        action.inject(
            self.presenter.manage(),
            self.telegram_mapper.message()
        )

    def search(self, action: SearchPollAction):
        action.inject(
            self.presenter.search(),
            self.telegram_mapper.query()
        )

    def chosen(self, action: ChosenPollAction):
        action.inject(
            self.presenter.publish(),
            self.telegram_mapper.user(),
            self.telegram_mapper.publication()
        )

    def action(self, action: PublishedPollAction):
        action.inject(
            self.presenter.vote(),
            self.telegram_mapper.publication_action(),
            self.telegram_mapper.poll_option_id()
        )
