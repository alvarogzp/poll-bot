from poll.domain.model.poll.full.poll import FullPoll
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionNumber, PollOptionInfo
from poll.domain.model.poll.poll import PollNumber, Poll
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.user.user import User


class GetPollRepository:
    def get_last_poll_from_user(self, user: User) -> PollNumber:
        raise NotImplementedError()

    def get_info(self, poll: Poll) -> PollInfo:
        raise NotImplementedError()

    def get_option_info(self, poll: Poll, option: PollOptionNumber) -> PollOptionInfo:
        raise NotImplementedError()

    def get_from_user(self, user: User, poll: PollNumber) -> Poll:
        raise NotImplementedError()

    def get_from_publication(self, publication: PollPublication) -> Poll:
        raise NotImplementedError()

    def get_full_poll(self, poll: Poll) -> FullPoll:
        raise NotImplementedError()
