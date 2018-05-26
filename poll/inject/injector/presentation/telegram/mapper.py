from poll.inject.injector.base import BaseInjector
from poll.presentation.telegram.bot.mapper.action import PublicationActionViewModelMapper
from poll.presentation.telegram.bot.mapper.message import MessageViewModelMapper
from poll.presentation.telegram.bot.mapper.option import PollOptionIdViewModelMapper
from poll.presentation.telegram.bot.mapper.publication import PublicationViewModelMapper
from poll.presentation.telegram.bot.mapper.query import QueryViewModelMapper
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class TelegramMapperInjector(BaseInjector):
    def user(self) -> UserViewModelMapper:
        return self._cache(UserViewModelMapper, lambda: UserViewModelMapper())

    def message(self) -> MessageViewModelMapper:
        return self._cache(MessageViewModelMapper, lambda: MessageViewModelMapper(
            self.user()
        ))

    def query(self) -> QueryViewModelMapper:
        return self._cache(QueryViewModelMapper, lambda: QueryViewModelMapper(
            self.user()
        ))

    def poll_option_id(self) -> PollOptionIdViewModelMapper:
        return self._cache(PollOptionIdViewModelMapper, lambda: PollOptionIdViewModelMapper())

    def publication(self) -> PublicationViewModelMapper:
        return self._cache(PublicationViewModelMapper, lambda: PublicationViewModelMapper())

    def publication_action(self) -> PublicationActionViewModelMapper:
        return self._cache(PublicationActionViewModelMapper, lambda: PublicationActionViewModelMapper(
            self.user(),
            self.publication()
        ))
