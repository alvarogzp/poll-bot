from bot.logger.logger import Logger

from poll.domain.logger import PollLogger
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.presentation.telegram.formatter import FormatterInjector
from poll.presentation.telegram.bot.logger import TelegramPollLogger


class LoggerInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, formatter: FormatterInjector, logger: Logger):
        super().__init__(cache)
        self.formatter = formatter
        self.logger = logger

    def poll(self) -> PollLogger:
        return self._cache(PollLogger, lambda: TelegramPollLogger(
            self.logger,
            self.formatter.log()
        ))
