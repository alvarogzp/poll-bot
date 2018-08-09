from bot.multithreading.worker import Worker
from bot.storage.api import StorageApi
from bot.storage.async.scheduler import StorageScheduler
from bot.storage.factory import StorageApiFactory

from poll.data.data_source.data_source import PollDataSource
from poll.domain.model.poll.full.poll import FullPoll
from poll.domain.model.poll.group.votes import PollVotes
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import PollNumber, Poll
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.poll.vote import PollVote, OptionPollVote, OpenPollVote
from poll.domain.model.user.state import State
from poll.domain.model.user.user import User
from poll.domain.repository.poll.get import GetPollRepository
from poll.domain.repository.poll.manage import ManagePollRepository
from poll.domain.repository.poll.publish import PublishPollRepository
from poll.domain.repository.poll.vote import VotePollRepository
from poll.domain.repository.state import UserStateRepository


class PollDataRepository(StorageApi, GetPollRepository, ManagePollRepository, PublishPollRepository,
                         VotePollRepository, UserStateRepository):
    def __init__(self, data_source: PollDataSource, scheduler: StorageScheduler):
        super().__init__(data_source, scheduler)
        self.data_source = data_source  # fix type hinting

    def get_last_poll_from_user(self, user: User) -> PollNumber:
        return self._with_result(
            lambda: self.data_source.get_last_poll_from_user(user),
            "get_last_poll_from_user"
        )

    def get_info(self, poll: Poll) -> PollInfo:
        return self._with_result(
            lambda: self.data_source.get_info(poll),
            "get_info"
        )

    def get_option_info(self, poll: Poll, option: PollOptionNumber) -> PollOptionInfo:
        return self._with_result(
            lambda: self.data_source.get_option_info(poll, option),
            "get_option_info"
        )

    def get_from_user(self, user: User, poll: PollNumber) -> Poll:
        return self._with_result(
            lambda: self.data_source.get_from_user(user, poll),
            "get_from_user"
        )

    def get_from_publication(self, publication: PollPublication) -> Poll:
        return self._with_result(
            lambda: self.data_source.get_from_publication(publication),
            "get_from_publication"
        )

    def get_full_poll(self, poll: Poll) -> FullPoll:
        return self._with_result(
            lambda: self.data_source.get_full_poll(poll),
            "get_full_poll"
        )

    def new_poll(self, info: PollInfo) -> PollNumber:
        return self._with_result(
            lambda: self.data_source.new_poll(info),
            "new_poll"
        )

    def add_option(self, poll: Poll, option: PollOptionInfo) -> PollOptionNumber:
        return self._with_result(
            lambda: self.data_source.add_option(poll, option),
            "add_option"
        )

    def complete(self, poll: Poll):
        self._with_result(
            lambda: self.data_source.complete(poll),
            "complete"
        )

    def delete(self, poll: Poll):
        self._with_result(
            lambda: self.data_source.delete(poll),
            "delete"
        )

    def publish(self, user: User, poll: PollNumber, publication: PollPublication):
        self._with_result(
            lambda: self.data_source.publish(user, poll, publication),
            "publish"
        )

    def exists_publication(self, publication: PollPublication) -> bool:
        return self._with_result(
            lambda: self.data_source.exists_publication(publication),
            "exists_publication"
        )

    def vote_option(self, vote: OptionPollVote):
        self._with_result(
            lambda: self.data_source.vote_option(vote),
            "vote_option"
        )

    def vote_open(self, vote: OpenPollVote):
        self._with_result(
            lambda: self.data_source.vote_open(vote),
            "vote_open"
        )

    def unvote_option(self, vote: OptionPollVote):
        self._with_result(
            lambda: self.data_source.unvote_option(vote),
            "unvote_option"
        )

    def unvote_poll(self, vote: PollVote):
        self._with_result(
            lambda: self.data_source.unvote_poll(vote),
            "unvote_poll"
        )

    def get_votes(self, poll: Poll, user: User) -> PollVotes:
        return self._with_result(
            lambda: self.data_source.get_votes(poll, user),
            "get_votes"
        )

    def set_state(self, user: User, state: State):
        self._with_result(
            lambda: self.data_source.set_state(user, state),
            "set_state"
        )

    def get_state(self, user: User) -> State:
        return self._with_result(
            lambda: self.data_source.get_state(user),
            "get_state"
        )


class PollDataRepositoryFactory(StorageApiFactory):
    @classmethod
    def repository(cls, data_source: PollDataSource, worker: Worker):
        scheduler = cls._get_scheduler_for(worker, data_source)
        return PollDataRepository(data_source, scheduler)
