from poll.domain.model.base import Comparable


class Poll(Comparable):
    """
    Identify a single poll among all bot polls.
    Should not be presented to users.
    Ids are allocated by repository.
    """
    def __init__(self, poll_id: int):
        super().__init__(poll_id, Poll)
        self.id = poll_id


class PollNumber:
    """
    Identify a poll within a user's owned polls.
    Allocated by repository.
    """
    def __init__(self, number: int):
        self.number = number
