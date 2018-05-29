from typing import Sequence

from poll.data.data_source.sqlite.component.poll.vote.option import PollVoteOptionSqliteComponent
from poll.data.data_source.sqlite.model.mapper.vote import PollVoteMapper
from poll.data.data_source.sqlite.model.poll.option import FullPollOptionData
from poll.domain.model.poll.full.option import FullPollOption
from poll.domain.model.poll.full.options import FullPollOptions
from poll.domain.model.poll.poll import Poll


class FullPollOptionMapper:
    def __init__(self, component_vote: PollVoteOptionSqliteComponent, mapper_vote: PollVoteMapper):
        self.component_vote = component_vote
        self.mapper_vote = mapper_vote

    def unmap_full_option(self, option: FullPollOptionData, poll: Poll) -> FullPollOption:
        votes = self.component_vote.get_option_votes(poll, option.id)
        return FullPollOption(
            option.number,
            option.info,
            self.mapper_vote.unmap_votes(votes)
        )

    def unmap_full_options(self, options: Sequence[FullPollOptionData], poll: Poll) -> FullPollOptions:
        return FullPollOptions([
            self.unmap_full_option(option, poll)
            for option in options
        ])
