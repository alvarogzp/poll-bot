from poll.domain.model.base import Comparable


class User(Comparable):
    def __init__(self, user_id: int):
        super().__init__(user_id, User)
        self.id = user_id


class AnonymousUser(User):
    def __init__(self, anonymized_user_id: int):
        super().__init__(anonymized_user_id)
