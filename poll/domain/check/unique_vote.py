from poll.domain.check.exception import RuleViolationError
from poll.domain.model.poll.group.votes import PollVotes


class UniqueVotePollCheck:
    @staticmethod
    def no_more_than_one_vote(votes: PollVotes):
        if len(votes) > 1:
            vote = votes.first()
            raise RuleViolationError(
                "unexpected number of votes for user {user} in poll {poll} (publication id)"
                .format(user=vote.user.id, poll=vote.publication.id)
            )
