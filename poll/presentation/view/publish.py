from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel


class PublishPollView:
    def poll_published(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        raise NotImplementedError()
