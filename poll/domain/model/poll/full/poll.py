from poll.domain.model.poll.full.options import FullPollOptions
from poll.domain.model.poll.group.publications import PollPublications
from poll.domain.model.poll.info import PollInfo


class FullPoll:
    def __init__(self, info: PollInfo, publications: PollPublications):
        self.info = info
        self.publications = publications


class FullOptionPoll(FullPoll):
    def __init__(self, info: PollInfo, publications: PollPublications, options: FullPollOptions):
        super().__init__(info, publications)
        self.options = options
