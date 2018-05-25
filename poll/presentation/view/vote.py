from poll.domain.model.poll.option import PollOptionInfo
from poll.domain.model.vote_result import VoteResult
from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.publication.action import PublicationActionViewModel
from poll.presentation.model.publication.publication import PublicationViewModel


class VotePollView:
    def voted(self, action: PublicationActionViewModel, option: PollOptionInfo, result: VoteResult):
        raise NotImplementedError()

    def update_poll(self, publication: PublicationViewModel, full_poll: FullPollViewModel):
        raise NotImplementedError()
