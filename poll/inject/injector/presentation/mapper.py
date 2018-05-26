from poll.inject.injector.base import BaseInjector
from poll.presentation.model.mapper.full.option import FullPollOptionMapper
from poll.presentation.model.mapper.full.poll import FullPollMapper, FullOptionPollMapper
from poll.presentation.model.mapper.info import PollInfoMapper
from poll.presentation.model.mapper.option import PollOptionNumberMapper
from poll.presentation.model.mapper.poll import PollNumberMapper
from poll.presentation.model.mapper.publication import PollPublicationMapper
from poll.presentation.model.mapper.settings import PollTypeMapper, PollAnonymityMapper, PollSettingsMapper
from poll.presentation.model.mapper.user import UserMapper
from poll.presentation.model.mapper.vote import OptionPollVoteMapper


class MapperInjector(BaseInjector):
    def user(self) -> UserMapper:
        return self._cache(UserMapper, lambda: UserMapper())

    def poll_number(self) -> PollNumberMapper:
        return self._cache(PollNumberMapper, lambda: PollNumberMapper())

    def poll_option_number(self) -> PollOptionNumberMapper:
        return self._cache(PollOptionNumberMapper, lambda: PollOptionNumberMapper())

    def poll_info(self) -> PollInfoMapper:
        return self._cache(PollInfoMapper, lambda: PollInfoMapper(
            self.poll_settings()
        ))

    def poll_settings(self) -> PollSettingsMapper:
        return self._cache(PollSettingsMapper, lambda: PollSettingsMapper(
            self._poll_type(),
            self._poll_anonymity()
        ))

    def _poll_type(self) -> PollTypeMapper:
        return self._cache(PollTypeMapper, lambda: PollTypeMapper())

    def _poll_anonymity(self) -> PollAnonymityMapper:
        return self._cache(PollAnonymityMapper, lambda: PollAnonymityMapper())

    def full_poll(self) -> FullPollMapper:
        return self._cache(FullPollMapper, lambda: FullPollMapper(
            self._full_option_poll()
        ))

    def _full_option_poll(self) -> FullOptionPollMapper:
        return self._cache(FullOptionPollMapper, lambda: FullOptionPollMapper(
            self.poll_info(),
            self._full_poll_option()
        ))

    def _full_poll_option(self) -> FullPollOptionMapper:
        return self._cache(FullPollOptionMapper, lambda: FullPollOptionMapper(
            self.poll_option_number(),
            self._option_poll_vote()
        ))

    def _option_poll_vote(self) -> OptionPollVoteMapper:
        return self._cache(OptionPollVoteMapper, lambda: OptionPollVoteMapper())

    def poll_publication(self) -> PollPublicationMapper:
        return self._cache(PollPublicationMapper, lambda: PollPublicationMapper())
