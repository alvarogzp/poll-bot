from poll.data.data_source.sqlite.model.poll.publication import PollPublicationData
from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.domain.model.poll.option import PollOption


class PollVoteData:
    def __init__(self, user: PollUserData, publication: PollPublicationData):
        self.user = user
        self.publication = publication


class OptionPollVoteData(PollVoteData):
    def __init__(self, user: PollUserData, publication: PollPublicationData, option: PollOption):
        super().__init__(user, publication)
        self.option = option


class OpenPollVoteData(PollVoteData):
    def __init__(self, user: PollUserData, publication: PollPublicationData, text: str):
        super().__init__(user, publication)
        self.text = text
