from typing import Sequence

from poll.domain.model.poll.option import PollOption


class BasePollOptions:
    def __init__(self, options: Sequence):
        self.options = options

    def __iter__(self):
        return self.options.__iter__()

    def __contains__(self, item):
        return self.options.__contains__(item)


class PollOptions(BasePollOptions):
    def __init__(self, options: Sequence[PollOption]):
        super().__init__(options)
        self.options = options  # fix type hinting
