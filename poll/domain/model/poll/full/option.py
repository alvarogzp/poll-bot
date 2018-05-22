from poll.domain.model.base import Comparable
from poll.domain.model.poll.group.votes import PollVotes
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber


class FullPollOption(Comparable):
    def __init__(self, option: PollOptionNumber, info: PollOptionInfo, votes: PollVotes):
        super().__init__(option, FullPollOption)
        self.option = option
        self.info = info
        self.votes = votes
