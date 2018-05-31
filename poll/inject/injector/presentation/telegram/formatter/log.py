from poll.inject.injector.base import BaseInjector
from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.presentation.telegram.mapper import TelegramMapperInjector
from poll.presentation.telegram.bot.formatter.log.publication import PublicationLogFormatter
from poll.presentation.telegram.bot.formatter.log.repository import RepositoryLogFormatter


class LogFormatterInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, telegram_mapper: TelegramMapperInjector):
        super().__init__(cache)
        self.telegram_mapper = telegram_mapper

    def repository(self) -> RepositoryLogFormatter:
        return self._cache(RepositoryLogFormatter, lambda: RepositoryLogFormatter())

    def publication(self) -> PublicationLogFormatter:
        return self._cache(PublicationLogFormatter, lambda: PublicationLogFormatter(
            self.telegram_mapper.user()
        ))
