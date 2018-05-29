from bot.action.util.textformat import FormattedText
from bot.api.api import Api
from bot.api.domain import Message

from poll.presentation.model.message import MessageViewModel
from poll.presentation.model.user import UserViewModel


class BaseView:
    def __init__(self, api: Api):
        self.api = api

    def _send(self, text: str, message: MessageViewModel):
        api_message = Message.create(text)
        self._send_message(api_message, message)

    def _send_formatted_text(self, text: FormattedText, message: MessageViewModel):
        return self._send_message(text.build_message(), message)

    def _send_message(self, api_message: Message, message: MessageViewModel):
        self._send_to(api_message, message.chat)

    def _send_to_user(self, api_message: Message, user: UserViewModel):
        self._send_to(api_message, user.id)

    def _send_to(self, api_message: Message, chat_id: int):
        api_message.to_chat(chat_id=chat_id)
        self.api.send_message(api_message)
