from bot.action.util.reply_markup.inline_keyboard.button import InlineKeyboardButton
from bot.action.util.reply_markup.inline_keyboard.markup import InlineKeyboardMarkup

from poll.domain.interactors.bot.search import SEARCH_PREFIX_BY_NUMBER
from poll.presentation.model.poll.full.option import FullPollOptionViewModel
from poll.presentation.model.poll.full.poll import FullPollViewModel, FullOptionPollViewModel
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.telegram.bot.mapper.option import PollOptionIdViewModelMapper


class PollInlineKeyboardFormatter:
    def __init__(self, mapper_option: PollOptionIdViewModelMapper):
        self.mapper_option = mapper_option

    @staticmethod
    def poll_created_inline_keyboard(poll_id: PollIdViewModel):
        return InlineKeyboardMarkup\
            .with_fixed_columns(1)\
            .add(InlineKeyboardButton.switch_inline_query(
                "Publish",
                SEARCH_PREFIX_BY_NUMBER + poll_id.id,
                current_chat=False
            ))

    def vote_inline_keyboard(self, poll: FullPollViewModel):
        if isinstance(poll, FullOptionPollViewModel):
            return self.vote_inline_keyboard_for_option_poll(poll)
        raise NotImplementedError()

    def vote_inline_keyboard_for_option_poll(self, poll: FullOptionPollViewModel):
        keyboard = InlineKeyboardMarkup.with_fixed_columns(1)
        for option in poll.options:
            button = InlineKeyboardButton.callback(
                self._get_vote_option_text(option),
                self.mapper_option.map_option(option.id)
            )
            keyboard.add(button)
        return keyboard

    @staticmethod
    def _get_vote_option_text(option: FullPollOptionViewModel):
        return "{name} - {vote_count}".format(name=option.name, vote_count=option.vote_count)
