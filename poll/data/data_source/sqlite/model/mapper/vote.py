from typing import Iterable

from poll.data.data_source.sqlite.component.poll.option import PollOptionSqliteComponent
from poll.data.data_source.sqlite.component.poll.publication import PollPublicationSqliteComponent
from poll.data.data_source.sqlite.component.user.user import UserSqliteComponent
from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.data.data_source.sqlite.model.poll.vote import OptionPollVoteData, PollVoteData
from poll.domain.model.poll.group.votes import OptionPollVotes, PollVotes
from poll.domain.model.poll.vote import OptionPollVote, PollVote


class PollVoteMapper:
    def __init__(self, user: UserSqliteComponent, publication: PollPublicationSqliteComponent):
        self.user = user
        self.publication = publication

    def unmap_vote(self, vote: PollVoteData) -> PollVote:
        poll_user = self.user.get_poll_user(vote.user)
        publication = self.publication.get_publication_from_id(vote.publication)
        return PollVote(
            poll_user,
            publication
        )

    def unmap_votes(self, votes: Iterable[PollVoteData]) -> PollVotes:
        return PollVotes([
            self.unmap_vote(vote)
            for vote in votes
        ])


class OptionPollVoteMapper:
    def __init__(self, user: UserSqliteComponent, option: PollOptionSqliteComponent,
                 publication: PollPublicationSqliteComponent):
        self.user = user
        self.option = option
        self.publication = publication

    def map_option_vote(self, vote: OptionPollVote, poll_user_id: PollUserData) -> OptionPollVoteData:
        publication = self.publication.get_id(vote.publication)
        poll = self.publication.get_poll(vote.publication)
        option_id = self.option.get_id(poll, vote.option)
        return OptionPollVoteData(
            poll_user_id,
            publication,
            option_id
        )

    def unmap_option_vote(self, vote: OptionPollVoteData) -> OptionPollVote:
        poll_user = self.user.get_poll_user(vote.user)
        publication = self.publication.get_publication_from_id(vote.publication)
        option = self.option.get_number(vote.option)
        return OptionPollVote(
            poll_user,
            publication,
            option
        )

    def unmap_option_votes(self, votes: Iterable[OptionPollVoteData]) -> OptionPollVotes:
        return OptionPollVotes([
            self.unmap_option_vote(vote)
            for vote in votes
        ])
