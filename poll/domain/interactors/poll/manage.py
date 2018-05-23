from poll.domain.check.complete import CompletePollCheck
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import Poll, PollNumber
from poll.domain.model.user.user import User
from poll.domain.repository.poll.get import GetPollRepository
from poll.domain.repository.poll.manage import ManagePollRepository


class ManagePollInteractor:
    def __init__(self, manage: ManagePollRepository, get: GetPollRepository, check: CompletePollCheck):
        self.manage = manage
        self.get = get
        self.check = check

    # PUBLIC INTERFACE

    def new_poll(self, info: PollInfo) -> PollNumber:
        return self.manage.new_poll(info)

    def add_option(self, user: User, number: PollNumber, option: PollOptionInfo) -> PollOptionNumber:
        poll = self.get.get_from_user(user, number)
        self._check_not_completed(poll)
        return self.manage.add_option(poll, option)

    def complete(self, user: User, number: PollNumber):
        poll = self.get.get_from_user(user, number)
        self._check_not_completed(poll)
        self.manage.complete(poll)

    def cancel(self, user: User, number: PollNumber):
        poll = self.get.get_from_user(user, number)
        self._check_not_completed(poll)
        self.manage.delete(poll)

    # PRIVATE METHODS

    def _check_not_completed(self, poll: Poll):
        info = self.get.get_info(poll)
        self.check.not_completed(info)
