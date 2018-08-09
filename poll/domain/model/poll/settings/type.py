from poll.domain.model.base import Comparable


class PollType(Comparable):
    def __init__(self, poll_type: int):
        super().__init__(poll_type, PollType)
        self.type = poll_type


SINGLE_VOTE = PollType(0)
MULTI_VOTE = PollType(1)
MULTI_VOTE_LIMITED = PollType(2)
OPEN = PollType(3)
RANGE = PollType(4)
