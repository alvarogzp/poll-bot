from typing import Sequence

from poll.domain.model.poll.option import PollOptionInfo
from poll.presentation.model.poll.option import PollOptionIdViewModel
from poll.presentation.model.poll.vote import OptionPollVoteViewModel


class FullPollOptionViewModel:
    def __init__(self, option_id: PollOptionIdViewModel, info: PollOptionInfo,
                 votes: Sequence[OptionPollVoteViewModel]):
        self.id = option_id
        self.info = info
        self.votes = votes

    @property
    def name(self):
        return self.info.name

    @property
    def vote_count(self):
        return len(self.votes)
