from poll.domain.model.user.user import User


class UserViewModel(User):
    def __init__(self, user_id: int, username: str, first_name: str, last_name: str, language: str):
        super().__init__(user_id)
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language = language
