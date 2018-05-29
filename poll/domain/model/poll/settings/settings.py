from poll.domain.model.poll.settings.anonymity import PollAnonymity, PERSONAL
from poll.domain.model.poll.settings.type import PollType, SINGLE_VOTE


class PollSettings:
    def __init__(self, poll_type: PollType, anonymity: PollAnonymity):
        self.type = poll_type
        self.anonymity = anonymity


DEFAULT_SETTINGS = PollSettings(SINGLE_VOTE, PERSONAL)
