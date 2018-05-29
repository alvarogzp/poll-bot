from poll.domain.model.base import Comparable


class VoteResult(Comparable):
    def __init__(self, result_id: int):
        super().__init__(result_id, VoteResult)
        self.id = result_id


VOTED = VoteResult(0)
UNVOTED = VoteResult(1)
CHANGED_VOTE = VoteResult(2)
