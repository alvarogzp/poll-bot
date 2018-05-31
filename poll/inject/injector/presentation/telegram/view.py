from bot.api.api import Api

from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.presentation.telegram.formatter.poll import PollFormatterInjector
from poll.inject.injector.presentation.telegram.logger import LoggerInjector
from poll.presentation.telegram.bot.view.manage import ManagePoll
from poll.presentation.telegram.bot.view.publish import PublishPoll
from poll.presentation.telegram.bot.view.search import SearchPoll
from poll.presentation.telegram.bot.view.vote import VotePoll
from poll.presentation.view.manage import ManagePollView
from poll.presentation.view.publish import PublishPollView
from poll.presentation.view.search import SearchPollView
from poll.presentation.view.vote import VotePollView


class ViewInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, poll_formatter: PollFormatterInjector, logger: LoggerInjector, api: Api):
        super().__init__(cache)
        self.poll_formatter = poll_formatter
        self.logger = logger
        self.api = api

    def manage(self) -> ManagePollView:
        return self._cache(ManagePollView, lambda: ManagePoll(
            self.api,
            self.poll_formatter.poll(),
            self.poll_formatter.inline_keyboard()
        ))

    def search(self) -> SearchPollView:
        return self._cache(SearchPollView, lambda: SearchPoll(
            self.api,
            self.poll_formatter.inline_result()
        ))

    def publish(self) -> PublishPollView:
        return self._cache(PublishPollView, lambda: PublishPoll(
            self.api,
            self.logger.telegram()
        ))

    def vote(self) -> VotePollView:
        return self._cache(VotePollView, lambda: VotePoll(
            self.api,
            self.poll_formatter.poll(),
            self.poll_formatter.inline_keyboard(),
            self.poll_formatter.vote_result()
        ))
