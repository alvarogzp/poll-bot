from poll.domain.model.base import Comparable


class PollType(Comparable):
    def __init__(self, poll_type: int):
        super().__init__(poll_type, PollType)
        self.type = poll_type


SINGLE_VOTE = PollType(0)
