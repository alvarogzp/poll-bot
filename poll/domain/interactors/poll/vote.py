from poll.domain.check.unique_vote import UniqueVotePollCheck
from poll.domain.model.poll.group.votes import OptionPollVotes
from poll.domain.model.poll.poll import Poll
from poll.domain.model.poll.vote import PollVote, OptionPollVote
from poll.domain.model.vote_result import VoteResult, VOTED, UNVOTED, CHANGED_VOTE
from poll.domain.repository.poll.get import GetPollRepository
from poll.domain.repository.poll.vote import VotePollRepository


class VotePollInteractor:
    def __init__(self, vote: VotePollRepository, get: GetPollRepository, check: UniqueVotePollCheck):
        self.repository_vote = vote
        self.get = get
        self.check = check

    def vote(self, vote: PollVote) -> VoteResult:
        poll = self.get.get_from_publication(vote.publication)
        if isinstance(vote, OptionPollVote):
            return self._vote_option(poll, vote)
        else:
            raise Exception("unexpected vote type")

    def _vote_option(self, poll: Poll, vote: OptionPollVote) -> VoteResult:
        previous_votes = self.repository_vote.get_votes(poll, vote.user)
        if previous_votes.is_empty():
            self.repository_vote.vote_option(vote)
            return VOTED
        else:
            assert isinstance(previous_votes, OptionPollVotes)  # force type hinting
            previous_vote = previous_votes.first()
            assert isinstance(previous_vote, OptionPollVote)  # force type hinting
            self.repository_vote.unvote_option(previous_vote)
            result = UNVOTED
            if previous_vote.option != vote.option:
                self.repository_vote.vote_option(vote)
                result = CHANGED_VOTE
            self.check.no_more_than_one_vote(previous_votes)
            return result
