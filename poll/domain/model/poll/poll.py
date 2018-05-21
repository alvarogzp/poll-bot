from poll.domain.model.base import Comparable


class Poll(Comparable):
    def __init__(self, poll_id: int):
        super().__init__(poll_id, Poll)
        self.id = poll_id


class PollNumber:
    def __init__(self, number: int):
        self.number = number
