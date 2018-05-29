from bot.api.api import Api

from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.base import BaseInjector
from poll.inject.injector.all.domain import DomainInjector
from poll.inject.injector.presentation.mapper import MapperInjector
from poll.inject.injector.presentation.presenter import PresenterInjector
from poll.inject.injector.presentation.telegram.action import TelegramActionInjector
from poll.inject.injector.presentation.telegram.formatter import FormatterInjector
from poll.inject.injector.presentation.telegram.mapper import TelegramMapperInjector
from poll.inject.injector.presentation.telegram.view import ViewInjector


class TelegramInjector(BaseInjector):
    def __init__(self, cache: InjectorCache, domain: DomainInjector, formatter: FormatterInjector,
                 telegram_mapper: TelegramMapperInjector, api: Api):
        super().__init__(cache)
        self.domain = domain
        self.formatter = formatter
        self.telegram_mapper = telegram_mapper
        self.api = api

    def action(self) -> TelegramActionInjector:
        return self._cache(TelegramActionInjector, lambda: TelegramActionInjector(
            self.cache,
            self._presenter(),
            self.telegram_mapper
        ))

    def _presenter(self) -> PresenterInjector:
        return self._cache(PresenterInjector, lambda: PresenterInjector(
            self.cache,
            self.domain.bot_interactor(),
            self.domain.poll_interactor(),
            self._view(),
            self._mapper()
        ))

    def _view(self) -> ViewInjector:
        return self._cache(ViewInjector, lambda: ViewInjector(
            self.cache,
            self.formatter,
            self.api
        ))

    def _mapper(self) -> MapperInjector:
        return self._cache(MapperInjector, lambda: MapperInjector(
            self.cache
        ))
