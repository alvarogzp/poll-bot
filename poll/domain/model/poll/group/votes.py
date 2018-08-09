from typing import Sequence

from poll.domain.model.poll.vote import PollVote, OptionPollVote, OpenPollVote


class PollVotes:
    def __init__(self, votes: Sequence[PollVote]):
        self.votes = votes

    def __len__(self):
        return len(self.votes)

    def __iter__(self):
        return self.votes.__iter__()

    def __getitem__(self, item):
        return self.votes[item]

    def is_empty(self):
        return len(self) == 0

    def first(self):
        return self[0]


class OptionPollVotes(PollVotes):
    def __init__(self, votes: Sequence[OptionPollVote]):
        super().__init__(votes)
        self.votes = votes  # fix type hinting


class OpenPollVotes(PollVotes):
    def __init__(self, votes: Sequence[OpenPollVote]):
        super().__init__(votes)
        self.votes = votes  # fix type hinting
