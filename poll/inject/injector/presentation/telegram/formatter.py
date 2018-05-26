from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.presentation.telegram.mapper import TelegramMapperInjector
from poll.presentation.telegram.bot.formatter.log import LogFormatter
from poll.presentation.telegram.bot.formatter.poll.content import PollFormatter, OptionPollFormatter
from poll.presentation.telegram.bot.formatter.poll.description import PollDescriptionFormatter, \
    OptionPollDescriptionFormatter
from poll.presentation.telegram.bot.formatter.poll.inline.keyboard import PollInlineKeyboardFormatter
from poll.presentation.telegram.bot.formatter.poll.inline.result import PollInlineResultFormatter
from poll.presentation.telegram.bot.formatter.poll.vote_result import VoteResultFormatter


class FormatterInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, telegram_mapper: TelegramMapperInjector):
        super().__init__(cache)
        self.telegram_mapper = telegram_mapper

    def poll(self) -> PollFormatter:
        return self._cache(PollFormatter, lambda: PollFormatter(
            self._option_poll()
        ))

    def poll_description(self) -> PollDescriptionFormatter:
        return self._cache(PollDescriptionFormatter, lambda: PollDescriptionFormatter(
            self._option_poll_description()
        ))

    def inline_keyboard(self) -> PollInlineKeyboardFormatter:
        return self._cache(PollInlineKeyboardFormatter, lambda: PollInlineKeyboardFormatter(
            self.telegram_mapper.poll_option_id()
        ))

    def inline_result(self) -> PollInlineResultFormatter:
        return self._cache(PollInlineResultFormatter, lambda: PollInlineResultFormatter(
            self.poll(),
            self.poll_description(),
            self.inline_keyboard()
        ))

    def vote_result(self) -> VoteResultFormatter:
        return self._cache(VoteResultFormatter, lambda: VoteResultFormatter())

    def _option_poll(self) -> OptionPollFormatter:
        return self._cache(OptionPollFormatter, lambda: OptionPollFormatter())

    def _option_poll_description(self) -> OptionPollDescriptionFormatter:
        return self._cache(OptionPollDescriptionFormatter, lambda: OptionPollDescriptionFormatter())

    def log(self) -> LogFormatter:
        return self._cache(LogFormatter, lambda: LogFormatter())
