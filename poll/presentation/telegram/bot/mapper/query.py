from bot.api.domain import ApiObject

from poll.presentation.model.query import QueryViewModel
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class QueryViewModelMapper:
    def __init__(self, mapper_user: UserViewModelMapper):
        self.mapper_user = mapper_user

    def unmap_query(self, query: ApiObject) -> QueryViewModel:
        return QueryViewModel(
            query.id,
            self.mapper_user.unmap_user(query.from_),
            query.query
        )
