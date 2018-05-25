from typing import Iterable, Sequence

from poll.domain.model.poll.full.option import FullPollOption
from poll.presentation.model.mapper.option import PollOptionNumberMapper
from poll.presentation.model.mapper.vote import OptionPollVoteMapper
from poll.presentation.model.poll.full.option import FullPollOptionViewModel


class FullPollOptionMapper:
    def __init__(self, mapper_poll_option_number: PollOptionNumberMapper,
                 mapper_option_poll_vote: OptionPollVoteMapper):
        self.mapper_poll_option_number = mapper_poll_option_number
        self.mapper_option_poll_vote = mapper_option_poll_vote

    def map_full_poll_option(self, option: FullPollOption) -> FullPollOptionViewModel:
        return FullPollOptionViewModel(
            self.mapper_poll_option_number.map_poll_option_number(option.option),
            option.info,
            self.mapper_option_poll_vote.map_option_poll_vote_iter(option.votes)
        )

    def map_full_poll_option_iter(self, options: Iterable[FullPollOption]) -> Sequence[FullPollOptionViewModel]:
        return [
            self.map_full_poll_option(option)
            for option in options
        ]
