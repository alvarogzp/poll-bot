from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.domain.model.poll.settings.settings import PollSettings


class PollInfoData:
    def __init__(self, owner: PollUserData, settings: PollSettings, title: str, complete: bool):
        self.owner = owner
        self.settings = settings
        self.title = title
        self.complete = complete
