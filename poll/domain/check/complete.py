from poll.domain.check.exception import RuleViolationError
from poll.domain.model.poll.info import PollInfo


class CompletePollCheck:
    def completed(self, poll: PollInfo):
        if not self._completed(poll):
            raise RuleViolationError("poll is not complete")

    def not_completed(self, poll: PollInfo):
        if self._completed(poll):
            raise RuleViolationError("poll is complete")

    @staticmethod
    def _completed(poll: PollInfo):
        return poll.complete
