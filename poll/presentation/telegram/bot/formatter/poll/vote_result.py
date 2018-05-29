from poll.domain.model.poll.option import PollOptionInfo
from poll.domain.model.vote_result import VoteResult, VOTED, CHANGED_VOTE, UNVOTED


class VoteResultFormatter:
    @staticmethod
    def format_option_vote_result(result: VoteResult, option: PollOptionInfo) -> str:
        option = option.name
        if result == VOTED:
            return "You voted for '{option}'".format(option=option)
        if result == CHANGED_VOTE:
            return "You changed your vote to '{option}'".format(option=option)
        if result == UNVOTED:
            return "You removed your vote"
