from poll.presentation.model.user import UserViewModel


class QueryViewModel:
    def __init__(self, query_id: str, user: UserViewModel, query: str):
        self.id = query_id
        self.user = user
        self.query = query
