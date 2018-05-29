from poll.domain.model.poll.option import PollOptionNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.poll.user import PollUser


class PollVote:
    def __init__(self, user: PollUser, publication: PollPublication):
        self.user = user
        self.publication = publication


class OptionPollVote(PollVote):
    def __init__(self, user: PollUser, publication: PollPublication, option: PollOptionNumber):
        super().__init__(user, publication)
        self.option = option
