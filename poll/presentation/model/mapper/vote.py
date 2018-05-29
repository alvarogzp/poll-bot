from typing import Iterable, Sequence

from poll.domain.model.poll.vote import OptionPollVote
from poll.presentation.model.poll.vote import OptionPollVoteViewModel


class OptionPollVoteMapper:
    @staticmethod
    def map_option_poll_vote(vote: OptionPollVote) -> OptionPollVoteViewModel:
        return OptionPollVoteViewModel(
            vote.user
        )

    def map_option_poll_vote_iter(self, votes: Iterable[OptionPollVote]) -> Sequence[OptionPollVoteViewModel]:
        return [
            self.map_option_poll_vote(vote)
            for vote in votes
        ]
