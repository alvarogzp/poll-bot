from poll.domain.check.complete import CompletePollCheck
from poll.domain.model.poll.full.poll import FullPoll
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionNumber, PollOptionInfo
from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.user.user import User
from poll.domain.repository.poll.get import GetPollRepository


class GetPollInteractor:
    def __init__(self, get: GetPollRepository, check: CompletePollCheck):
        self.get = get
        self.check = check

    def by_publication(self, publication: PollPublication) -> FullPoll:
        poll = self.get.get_from_publication(publication)
        return self.get.get_full_poll(poll)

    def by_number(self, user: User, number: PollNumber) -> FullPoll:
        poll = self.get.get_from_user(user, number)
        full_poll = self.get.get_full_poll(poll)
        self.check.completed(full_poll.info)
        return full_poll

    def info(self, user: User, poll: PollNumber) -> PollInfo:
        poll = self.get.get_from_user(user, poll)
        return self.get.get_info(poll)

    def option_info(self, user: User, poll: PollNumber, option: PollOptionNumber) -> PollOptionInfo:
        poll = self.get.get_from_user(user, poll)
        return self.get.get_option_info(poll, option)

    def last(self, user: User) -> PollNumber:
        return self.get.get_last_poll_from_user(user)
