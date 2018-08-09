from bot.storage.data_source.data_source import StorageDataSource

from poll.domain.model.poll.full.poll import FullPoll
from poll.domain.model.poll.group.votes import PollVotes
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import Poll, PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.poll.vote import PollVote, OptionPollVote, OpenPollVote
from poll.domain.model.user.state import State
from poll.domain.model.user.user import User


class PollDataSource(StorageDataSource):
    def init(self):
        raise NotImplementedError()

    def context_manager(self):
        raise NotImplementedError()

    def get_last_poll_from_user(self, user: User) -> PollNumber:
        raise NotImplementedError()

    def get_info(self, poll: Poll) -> PollInfo:
        raise NotImplementedError()

    def get_option_info(self, poll: Poll, option: PollOptionNumber) -> PollOptionInfo:
        raise NotImplementedError()

    def get_from_user(self, user: User, poll: PollNumber) -> Poll:
        raise NotImplementedError()

    def get_from_publication(self, publication: PollPublication) -> Poll:
        raise NotImplementedError()

    def get_full_poll(self, poll: Poll) -> FullPoll:
        raise NotImplementedError()

    def new_poll(self, info: PollInfo) -> PollNumber:
        raise NotImplementedError()

    def add_option(self, poll: Poll, option: PollOptionInfo) -> PollOptionNumber:
        raise NotImplementedError()

    def complete(self, poll: Poll):
        raise NotImplementedError()

    def delete(self, poll: Poll):
        raise NotImplementedError()

    def publish(self, user: User, poll: PollNumber, publication: PollPublication):
        raise NotImplementedError()

    def exists_publication(self, publication: PollPublication) -> bool:
        raise NotImplementedError()

    def vote_option(self, vote: OptionPollVote):
        raise NotImplementedError()

    def vote_open(self, vote: OpenPollVote):
        raise NotImplementedError()

    def unvote_option(self, vote: OptionPollVote):
        raise NotImplementedError()

    def unvote_poll(self, vote: PollVote):
        raise NotImplementedError()

    def get_votes(self, poll: Poll, user: User) -> PollVotes:
        raise NotImplementedError()

    def set_state(self, user: User, state: State):
        raise NotImplementedError()

    def get_state(self, user: User) -> State:
        raise NotImplementedError()
