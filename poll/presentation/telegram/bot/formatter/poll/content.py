from bot.action.util.textformat import FormattedText

from poll.presentation.model.poll.full.option import FullPollOptionViewModel
from poll.presentation.model.poll.full.poll import FullOptionPollViewModel, FullPollViewModel
from poll.presentation.model.poll.vote import OptionPollVoteViewModel


class OptionPollFormatter:
    def format_poll(self, poll: FullOptionPollViewModel) -> FormattedText:
        title = poll.title
        vote_count = poll.vote_count

        options = FormattedText()\
            .newline().newline()\
            .join(self._option(option) for option in poll.options)

        return FormattedText().normal(
            "📊 {title}\n"
            "\n"
            "{options}\n"
            "\n"
            "👥 {vote_count} votes"
        ).start_format().bold(
            title=title,
            vote_count=vote_count
        ).concat(
            options=options
        ).end_format()

    def _option(self, option: FullPollOptionViewModel):
        name = option.name
        vote_count = option.vote_count

        text = FormattedText().normal(
            "▪️ {name} [{vote_count}]"
        ).start_format().bold(
            name=name
        ).normal(
            vote_count=vote_count
        ).end_format()

        if vote_count > 0:
            text.newline().concat(
                FormattedText()
                .newline()
                .join(self._vote(vote) for vote in option.votes)
            )

        return text

    @staticmethod
    def _vote(vote: OptionPollVoteViewModel):
        user = vote.user.name

        return FormattedText().normal(
            "   ▫️ {user}"
        ).start_format().normal(
            user=user
        ).end_format()


class PollFormatter:
    def __init__(self, option_poll_formatter: OptionPollFormatter):
        self.option_poll_formatter = option_poll_formatter

    def format_poll(self, poll: FullPollViewModel) -> FormattedText:
        if isinstance(poll, FullOptionPollViewModel):
            return self.option_poll_formatter.format_poll(poll)
        raise NotImplementedError()
