from typing import Sequence

from poll.presentation.model.poll.full.option import FullPollOptionViewModel
from poll.presentation.model.poll.info import PollInfoViewModel


class FullPollViewModel:
    def __init__(self, info: PollInfoViewModel):
        self.info = info

    @property
    def title(self):
        return self.info.title


class FullOptionPollViewModel(FullPollViewModel):
    def __init__(self, info: PollInfoViewModel, options: Sequence[FullPollOptionViewModel]):
        super().__init__(info)
        self.options = options

    @property
    def vote_count(self):
        return sum(option.vote_count for option in self.options)
