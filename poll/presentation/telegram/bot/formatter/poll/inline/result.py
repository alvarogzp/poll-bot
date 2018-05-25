from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.telegram.bot.formatter.poll.content import PollFormatter
from poll.presentation.telegram.bot.formatter.poll.description import PollDescriptionFormatter
from poll.presentation.telegram.bot.formatter.poll.inline.keyboard import PollInlineKeyboardFormatter


class PollInlineResultFormatter:
    def __init__(self, poll_formatter: PollFormatter, poll_description_formatter: PollDescriptionFormatter,
                 inline_keyboard_formatter: PollInlineKeyboardFormatter):
        self.poll_formatter = poll_formatter
        self.poll_description_formatter = poll_description_formatter
        self.inline_keyboard_formatter = inline_keyboard_formatter

    def inline_result(self, poll_id: PollIdViewModel, poll: FullPollViewModel):
        formatted_poll = self.poll_formatter.format_poll(poll)
        description = self.poll_description_formatter.format_description(poll)
        inline_keyboard = self.inline_keyboard_formatter.vote_inline_keyboard(poll).data
        return {
            "type": "article",
            "id": poll_id.id,
            "title": poll.title,
            "input_message_content": {
                "message_text": formatted_poll.text,
                "parse_mode": formatted_poll.mode,
                "disable_web_page_preview": True
            },
            "reply_markup": inline_keyboard,
            "description": description
        }
