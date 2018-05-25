from bot.api.domain import ApiObject

from poll.presentation.model.publication.action import PublicationActionViewModel
from poll.presentation.telegram.bot.mapper.publication import PublicationViewModelMapper
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class PublicationActionViewModelMapper:
    def __init__(self, mapper_user: UserViewModelMapper, mapper_publication: PublicationViewModelMapper):
        self.mapper_user = mapper_user
        self.mapper_publication = mapper_publication

    def unmap_publication_action(self, query: ApiObject) -> PublicationActionViewModel:
        return PublicationActionViewModel(
            query.id,
            self.mapper_user.unmap_user(query.from_),
            self.mapper_publication.unmap_publication(query)
        )
