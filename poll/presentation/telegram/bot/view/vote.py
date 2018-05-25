from bot.api.api import Api

from poll.domain.model.poll.option import PollOptionInfo
from poll.domain.model.vote_result import VoteResult
from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.publication.action import PublicationActionViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.telegram.bot.formatter.poll.content import PollFormatter
from poll.presentation.telegram.bot.formatter.poll.inline.keyboard import PollInlineKeyboardFormatter
from poll.presentation.telegram.bot.formatter.poll.vote_result import VoteResultFormatter
from poll.presentation.telegram.bot.view.base import BaseView
from poll.presentation.view.vote import VotePollView


class VotePoll(BaseView, VotePollView):
    def __init__(self, api: Api, poll_formatter: PollFormatter, inline_keyboard_formatter: PollInlineKeyboardFormatter,
                 vote_result_formatter: VoteResultFormatter):
        super().__init__(api)
        self.poll_formatter = poll_formatter
        self.inline_keyboard_formatter = inline_keyboard_formatter
        self.vote_result_formatter = vote_result_formatter

    def voted(self, action: PublicationActionViewModel, option: PollOptionInfo, result: VoteResult):
        text = self.vote_result_formatter.format_option_vote_result(result, option)
        self.api.answerCallbackQuery(
            callback_query_id=action.id,
            text=text
        )

    def update_poll(self, publication: PublicationViewModel, full_poll: FullPollViewModel):
        formatted_poll = self.poll_formatter.format_poll(full_poll)
        inline_keyboard = self.inline_keyboard_formatter.vote_inline_keyboard(full_poll)
        message = formatted_poll.build_message()
        message.inline_message_id(publication.id)
        message.with_reply_markup(inline_keyboard)
        self.api.editMessageText(**message.data)
