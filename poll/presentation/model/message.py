from poll.presentation.model.user import UserViewModel


class MessageViewModel:
    def __init__(self, message_id: int, user: UserViewModel, chat: int, text: str):
        self.id = message_id
        self.user = user
        self.chat = chat
        self.text = text
