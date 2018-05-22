from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.user.user import User


class PublishPollRepository:
    def publish(self, user: User, poll: PollNumber, publication: PollPublication):
        raise NotImplementedError()

    def exists_publication(self, publication: PollPublication) -> bool:
        raise NotImplementedError()
