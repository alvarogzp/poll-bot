from typing import Union, Optional

from poll.domain.interactors.poll.get import GetPollInteractor
from poll.domain.interactors.poll.manage import ManagePollInteractor
from poll.domain.interactors.user.settings import UserSettingsInteractor
from poll.domain.interactors.user.state import UserStateInteractor
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.poll.settings.settings import PollSettings
from poll.domain.model.poll.user import PollUser
from poll.domain.model.user.state import WAITING_TITLE, INCOMPLETE_POLL_STATES, WAITING_MORE_OPTIONS, IDLE, IDLE_STATES, \
    State, ADDING_OPTIONS_STATES, READY_TO_COMPLETE_STATES, WAITING_FIRST_OPTION
from poll.domain.model.user.user import User


class BotManagePollInteractor:
    def __init__(self, manage: ManagePollInteractor, get: GetPollInteractor, state: UserStateInteractor,
                 settings: UserSettingsInteractor):
        self.manage = manage
        self.get = get
        self.state = state
        self.settings = settings

    # PUBLIC INTERFACE

    def start(self, user: User) -> PollSettings:
        self._cancel(user, new_state=WAITING_TITLE)
        settings = self.settings.get(user)
        return settings.poll_settings

    def message(self, user: PollUser, text: str) -> Union[PollNumber, PollOptionNumber, None]:
        state = self.state.get_state(user)
        if state == WAITING_TITLE:
            number = self._new_poll(user, text)
            self.state.set_state(user, WAITING_FIRST_OPTION)
            return number
        elif state in ADDING_OPTIONS_STATES:
            number = self._option(user, text)
            if state == WAITING_FIRST_OPTION:
                self.state.set_state(user, WAITING_MORE_OPTIONS)
            return number

    def _new_poll(self, user: PollUser, title: str) -> PollNumber:
        settings = self.settings.get(user)
        info = PollInfo(user, settings.poll_settings, title, False)
        return self.manage.new_poll(info)

    def _option(self, user: User, option: str) -> PollOptionNumber:
        number = self.get.last(user)
        option = PollOptionInfo(option)
        return self.manage.add_option(user, number, option)

    def complete(self, user: User) -> Optional[PollNumber]:
        state = self.state.get_state(user)
        if state in READY_TO_COMPLETE_STATES:
            number = self.get.last(user)
            self.manage.complete(user, number)
            self.state.set_state(user, IDLE)
            return number

    def cancel(self, user: User) -> Union[PollNumber, bool]:
        return self._cancel(user, new_state=IDLE)

    def _cancel(self, user: User, new_state: State) -> Union[PollNumber, bool]:
        state = self.state.get_state(user)
        incomplete_poll = state in INCOMPLETE_POLL_STATES
        number = None
        if incomplete_poll:
            number = self.get.last(user)
            self.manage.cancel(user, number)
        self.state.set_state(user, new_state)
        return number if incomplete_poll else state not in IDLE_STATES
