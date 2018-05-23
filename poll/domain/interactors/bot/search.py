from typing import Optional, Tuple

from poll.domain.interactors.poll.get import GetPollInteractor
from poll.domain.model.poll.full.poll import FullPoll
from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.user.user import User


SEARCH_PREFIX_BY_NUMBER = "#"


class BotSearchPollInteractor:
    def __init__(self, get: GetPollInteractor):
        self.get = get

    def search(self, user: User, text: str) -> Optional[Tuple[PollNumber, FullPoll]]:
        if text.startswith(SEARCH_PREFIX_BY_NUMBER):
            text = text[len(SEARCH_PREFIX_BY_NUMBER):]
            if text.isdigit():
                number = PollNumber(int(text))
                return number, self.get.by_number(user, number)
