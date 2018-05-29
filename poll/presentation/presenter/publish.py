from poll.domain.interactors.poll.publish import PublishPollInteractor
from poll.presentation.model.mapper.poll import PollNumberMapper
from poll.presentation.model.mapper.publication import PollPublicationMapper
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel
from poll.presentation.view.publish import PublishPollView


class PublishPollPresenter:
    def __init__(self, view: PublishPollView, publish: PublishPollInteractor, mapper_poll_number: PollNumberMapper,
                 mapper_poll_publication: PollPublicationMapper):
        self.view = view
        self.interactor_publish = publish
        self.mapper_poll_number = mapper_poll_number
        self.mapper_poll_publication = mapper_poll_publication

    def publish(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        """
        :param publication: A unique id safe and not able to be modified by users.
          See :class:`PollPublication` for more info.
        """
        number = self.mapper_poll_number.unmap_poll_number(poll_id)
        poll_publication = self.mapper_poll_publication.unmap_publication(publication)
        self.interactor_publish.publish(user, number, poll_publication)
        self.view.poll_published(user, poll_id, publication)
