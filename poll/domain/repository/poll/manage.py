from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import Poll, PollNumber


class ManagePollRepository:
    def new_poll(self, info: PollInfo) -> PollNumber:
        raise NotImplementedError()

    def add_option(self, poll: Poll, option: PollOptionInfo) -> PollOptionNumber:
        raise NotImplementedError()

    def complete(self, poll: Poll):
        raise NotImplementedError()

    def delete(self, poll: Poll):
        raise NotImplementedError()
