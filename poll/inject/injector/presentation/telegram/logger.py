from bot.logger.logger import Logger

from poll.domain.logger import PollLogger
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.presentation.telegram.formatter.log import LogFormatterInjector
from poll.presentation.telegram.bot.logger import TelegramPollLogger


class LoggerInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, log_formatter: LogFormatterInjector, logger: Logger):
        super().__init__(cache)
        self.log_formatter = log_formatter
        self.logger = logger

    def poll(self) -> PollLogger:
        return self.telegram()

    def telegram(self) -> TelegramPollLogger:
        return self._cache(TelegramPollLogger, lambda: TelegramPollLogger(
            self.logger,
            self.log_formatter.repository()
        ))
