from poll.domain.model.user.user import User


class PollUser(User):
    def __init__(self, user_id: int, username: str, name: str):
        super().__init__(user_id)
        self.username = username
        self.name = name
