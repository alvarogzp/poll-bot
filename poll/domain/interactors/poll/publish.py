from poll.domain.check.exists_publication import ExistsPublicationPollCheck
from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.user.user import User
from poll.domain.repository.poll.publish import PublishPollRepository


class PublishPollInteractor:
    def __init__(self, publish: PublishPollRepository, check: ExistsPublicationPollCheck):
        self.repository_publish = publish
        self.check = check

    def publish(self, user: User, poll: PollNumber, publication: PollPublication):
        """
        :param user: User who wants to perform the action
        :param poll: Poll that the user wants to publish
        :param publication: Identification of the published poll.
          Can be used to vote and to get poll info.
          Must be unique, see :class:`PollPublication` for exact requisites.
        """
        self.check.does_not_exist_publication(publication)
        self.repository_publish.publish(user, poll, publication)
