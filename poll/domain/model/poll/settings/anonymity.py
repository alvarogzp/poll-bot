from poll.domain.model.base import Comparable


class PollAnonymity(Comparable):
    def __init__(self, anonymity: int):
        super().__init__(anonymity, PollAnonymity)
        self.anonymity = anonymity


PERSONAL = PollAnonymity(0)
