from bot.api.domain import ApiObject

from poll.presentation.model.message import MessageViewModel
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class MessageViewModelMapper:
    def __init__(self, mapper_user: UserViewModelMapper):
        self.mapper_user = mapper_user

    def unmap_message(self, message: ApiObject) -> MessageViewModel:
        return MessageViewModel(
            message.message_id,
            self.mapper_user.unmap_user(message.from_),
            message.chat.id,
            message.text
        )
