class PollTypeViewModel:
    def __init__(self, poll_type: str):
        self.type = poll_type


class PollAnonymityViewModel:
    def __init__(self, anonymity: str):
        self.anonymity = anonymity


class PollSettingsViewModel:
    def __init__(self, poll_type: PollTypeViewModel, anonymity: PollAnonymityViewModel):
        self.type = poll_type
        self.anonymity = anonymity
