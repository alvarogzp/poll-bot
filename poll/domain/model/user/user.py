from poll.domain.model.base import Comparable


class User(Comparable):
    def __init__(self, user_id: int):
        super().__init__(user_id, User)
        self.id = user_id
