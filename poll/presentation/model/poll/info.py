from poll.presentation.model.poll.settings import PollSettingsViewModel


class PollInfoViewModel:
    def __init__(self, settings: PollSettingsViewModel, title: str):
        self.settings = settings
        self.title = title
