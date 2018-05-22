from poll.domain.check.exception import RuleViolationError
from poll.domain.model.poll.publication import PollPublication
from poll.domain.repository.poll.publish import PublishPollRepository


class ExistsPublicationPollCheck:
    def __init__(self, publish: PublishPollRepository):
        self.publish = publish

    def does_not_exist_publication(self, publication: PollPublication):
        if self.publish.exists_publication(publication):
            raise RuleViolationError("publication already exists")
