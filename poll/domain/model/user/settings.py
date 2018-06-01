from poll.domain.model.poll.settings.settings import PollSettings


class UserSettings:
    def __init__(self, poll_settings: PollSettings):
        self.poll_settings = poll_settings
