from typing import Sequence

from poll.domain.model.poll.full.option import FullPollOption
from poll.domain.model.poll.group.options import BasePollOptions
from poll.domain.model.poll.option import PollOptionNumber, PollOptionInfo
from poll.domain.exception import NotFoundError


class FullPollOptions(BasePollOptions):
    def __init__(self, options: Sequence[FullPollOption]):
        super().__init__(options)
        self.options = options  # fix type hinting

    def get_info(self, option: PollOptionNumber) -> PollOptionInfo:
        for full_option in self.options:
            if full_option.option == option:
                return full_option.info
        raise NotFoundError("poll option number", option.number)
