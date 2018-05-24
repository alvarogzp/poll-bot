from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel


class PublicationActionViewModel:
    def __init__(self, action_id: str, user: UserViewModel, publication: PublicationViewModel):
        self.id = action_id
        self.user = user
        self.publication = publication
