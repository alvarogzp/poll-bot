from poll.presentation.model.poll.full.poll import FullOptionPollViewModel, FullPollViewModel


class OptionPollDescriptionFormatter:
    @staticmethod
    def format_description(poll: FullOptionPollViewModel) -> str:
        return "{options}".format(
            options=" | ".join(option.name for option in poll.options)
        )


class PollDescriptionFormatter:
    def __init__(self, option_poll_description_formatter: OptionPollDescriptionFormatter):
        self.option_poll_description_formatter = option_poll_description_formatter

    def format_description(self, poll: FullPollViewModel) -> str:
        if isinstance(poll, FullOptionPollViewModel):
            return self.option_poll_description_formatter.format_description(poll)
        raise NotImplementedError()
