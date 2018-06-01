from bot.action.util.textformat import FormattedText
from bot.api.api import Api

from poll.domain.model.poll.option import PollOptionInfo
from poll.presentation.model.message import MessageViewModel
from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.poll.info import PollInfoViewModel
from poll.presentation.model.poll.option import PollOptionIdViewModel
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.poll.settings import PollSettingsViewModel
from poll.presentation.telegram.bot.formatter.poll.content import PollFormatter
from poll.presentation.telegram.bot.formatter.poll.inline.keyboard import PollInlineKeyboardFormatter
from poll.presentation.telegram.bot.view.base import BaseView
from poll.presentation.view.manage import ManagePollView


class ManagePoll(BaseView, ManagePollView):
    def __init__(self, api: Api, poll_formatter: PollFormatter, inline_keyboard_formatter: PollInlineKeyboardFormatter):
        super().__init__(api)
        self.poll_formatter = poll_formatter
        self.inline_keyboard_formatter = inline_keyboard_formatter

    def started(self, message: MessageViewModel, settings: PollSettingsViewModel):
        text = FormattedText()\
            .bold("Starting a new poll...").newline().newline()\
            .normal("Current settings:\n"
                    " - Type: {type}\n"
                    " - Anonymity: {anonymity}").newline().newline()\
            .italic("Poll settings cannot be modified yet, sorry.").newline().newline()\
            .bold("Please, send the poll title.")\
            .start_format().bold(
                type=settings.type.type,
                anonymity=settings.anonymity.anonymity
            ).end_format()
        self._send_formatted_text(text, message)

    def poll_created(self, message: MessageViewModel, poll_id: PollIdViewModel, info: PollInfoViewModel):
        text = FormattedText()\
            .normal(
                "Creating poll #{id} with title:\n"
                "{title}\n"
                "\n"
            )\
            .bold("Please, send now the answers.")\
            .start_format().normal(
                id=poll_id.id,
            ).bold(
                title=info.title
            ).end_format()
        self._send_formatted_text(text, message)

    def option_added(self, message: MessageViewModel, option_id: PollOptionIdViewModel, info: PollOptionInfo):
        text = FormattedText()\
            .normal("Option {id} added:\n{name}\n\nSend another answer or /done to end poll creation.")\
            .start_format().bold(
                id=option_id.id,
                name=info.name,
            ).end_format()
        self._send_formatted_text(text, message)

    def message_ignored(self, message: MessageViewModel):
        text = "To start a new poll, first send /start"
        self._send(text, message)

    def poll_completed(self, message: MessageViewModel, poll_id: PollIdViewModel, full_poll: FullPollViewModel):
        text = FormattedText()\
            .normal("Poll #{id}:\n\n{poll}")\
            .start_format()\
            .normal(
                id=poll_id.id
            ).concat(
                poll=self.poll_formatter.format_poll(full_poll)
        ).end_format()
        inline_keyboard = self.inline_keyboard_formatter.poll_created_inline_keyboard(poll_id)
        api_message = text.build_message().with_reply_markup(inline_keyboard)
        self._send_message(api_message, message)

    def poll_cancelled(self, message: MessageViewModel, poll_id: PollIdViewModel):
        text = FormattedText()\
            .normal("Poll #{id} has been cancelled")\
            .start_format().normal(id=poll_id.id).end_format()
        self._send_formatted_text(text, message)

    def nothing_to_complete(self, message: MessageViewModel):
        text = "There is no poll to end :/"
        self._send(text, message)

    def nothing_to_cancel(self, message: MessageViewModel):
        text = "Nothing to cancel :/"
        self._send(text, message)

    def back_to_idle(self, message: MessageViewModel):
        text = "Ok, send /start again to create a new poll."
        self._send(text, message)
