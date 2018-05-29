from poll.domain.model.poll.settings.settings import PollSettings
from poll.domain.model.poll.user import PollUser


class PollInfo:
    def __init__(self, owner: PollUser, settings: PollSettings, title: str, complete: bool):
        self.owner = owner
        self.settings = settings
        self.title = title
        self.complete = complete
