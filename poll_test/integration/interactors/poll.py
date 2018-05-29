import unittest

from poll.domain.check.exception import RuleViolationError
from poll.domain.model.poll.info import PollInfo
from poll.domain.model.poll.option import PollOptionInfo, PollOptionNumber
from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.poll.settings.anonymity import PERSONAL, PollAnonymity
from poll.domain.model.poll.settings.settings import PollSettings
from poll.domain.model.poll.settings.type import SINGLE_VOTE, PollType
from poll.domain.model.poll.user import PollUser
from poll.domain.model.poll.vote import OptionPollVote
from poll.domain.model.user.user import User
from poll.domain.exception import NotFoundError
from poll_test.integration.interactors.base import BaseIntegrationTest


ANY_POLL_TITLE = "poll title"

ANY_OWNER = PollUser(456456, "testowner", "Test Owner")
ANY_VOTER = PollUser(43453, "testvoter", "Test Voter")

ANY_POLL_OPTION_1 = PollOptionInfo("poll option 1")
ANY_POLL_OPTION_2 = PollOptionInfo("poll option 2")
ANY_POLL_OPTIONS = [ANY_POLL_OPTION_1, ANY_POLL_OPTION_2]

ANY_POLL_PUBLICATION = PollPublication("test publication id")
ANY_OTHER_POLL_PUBLICATION = PollPublication("test publication id 2")

ANY_VALID_OPTION_NUMBER = PollOptionNumber(1)
ANY_OTHER_VALID_OPTION_NUMBER = PollOptionNumber(2)

ANY_NON_EXISTENT_OPTION_NUMBER = PollOptionNumber(99)


class PollInteractorsTest(BaseIntegrationTest):
    def setUp(self):
        self._setup()

    def test_create_poll(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS

        self._create_poll(owner, poll_type, anonymity, title, *options)

    def test_cancel_poll(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS

        number = self._create_poll(owner, poll_type, anonymity, title, *options, complete=False)
        self.interactors.manage().cancel(owner, number)

    def test_publish_poll(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION
        other_publication = ANY_OTHER_POLL_PUBLICATION

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        poll = self.repository.get_from_user(owner, number)

        self._publish_poll(owner, number, publication)

        published_poll = self.repository.get_from_publication(publication)
        self.assertEqual(poll, published_poll)

        self._publish_poll(owner, number, other_publication)

        published_poll = self.repository.get_from_publication(other_publication)
        self.assertEqual(poll, published_poll)

    def test_publish_poll_with_already_existent_publication_id(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        self._publish_poll(owner, number, publication)
        with self.assertRaises(RuleViolationError):
            self._publish_poll(owner, number, publication)

    def test_vote(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION
        voter = ANY_VOTER
        option = ANY_VALID_OPTION_NUMBER

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        self._publish_poll(owner, number, publication)
        poll = self.repository.get_from_publication(publication)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

        self._vote_poll(voter, publication, option)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(1, len(votes.votes))

    def test_vote_invalid_option(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION
        voter = ANY_VOTER
        invalid_option = ANY_NON_EXISTENT_OPTION_NUMBER

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        self._publish_poll(owner, number, publication)
        poll = self.repository.get_from_publication(publication)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

        with self.assertRaises(NotFoundError) as e:
            self._vote_poll(voter, publication, invalid_option)

        self.assertEqual("poll option number", e.exception.name)
        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

    def test_remove_vote(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION
        voter = ANY_VOTER
        option = ANY_VALID_OPTION_NUMBER

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        self._publish_poll(owner, number, publication)
        poll = self.repository.get_from_publication(publication)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

        self._vote_poll(voter, publication, option)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(1, len(votes.votes))

        self._vote_poll(voter, publication, option)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

    def test_change_vote(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION
        voter = ANY_VOTER
        option = ANY_VALID_OPTION_NUMBER
        other_option = ANY_OTHER_VALID_OPTION_NUMBER

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        self._publish_poll(owner, number, publication)
        poll = self.repository.get_from_publication(publication)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

        self._vote_poll(voter, publication, option)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(1, len(votes.votes))
        vote = votes.first()
        assert isinstance(vote, OptionPollVote)  # force type hinting to subclass
        self.assertEqual(option, vote.option)

        self._vote_poll(voter, publication, other_option)

        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(1, len(votes.votes))
        vote = votes.first()
        assert isinstance(vote, OptionPollVote)  # force type hinting to subclass
        self.assertEqual(other_option, vote.option)

    def test_vote_invalid_poll(self):
        owner = ANY_OWNER
        poll_type = SINGLE_VOTE
        anonymity = PERSONAL
        title = ANY_POLL_TITLE
        options = ANY_POLL_OPTIONS
        publication = ANY_POLL_PUBLICATION
        invalid_publication = ANY_OTHER_POLL_PUBLICATION
        voter = ANY_VOTER
        option = ANY_VALID_OPTION_NUMBER

        number = self._create_poll(owner, poll_type, anonymity, title, *options)
        self._publish_poll(owner, number, publication)

        with self.assertRaises(NotFoundError) as e:
            self._vote_poll(voter, invalid_publication, option)

        self.assertEqual("poll publication", e.exception.name)

        poll = self.repository.get_from_publication(publication)
        votes = self.repository.get_votes(poll, voter)
        self.assertEqual(0, len(votes.votes))

    def _create_poll(self, owner: PollUser, poll_type: PollType, anonymity: PollAnonymity, title: str,
                     *options: PollOptionInfo, complete: bool = True) -> PollNumber:
        manage = self.interactors.manage()

        poll_info = PollInfo(owner, PollSettings(poll_type, anonymity), title, False)

        number = manage.new_poll(poll_info)

        for option in options:
            manage.add_option(owner, number, option)

        if complete:
            manage.complete(owner, number)

        return number

    def _publish_poll(self, user: User, number: PollNumber, publication: PollPublication):
        self.interactors.publish().publish(user, number, publication)

    def _vote_poll(self, voter: PollUser, publication: PollPublication, option: PollOptionNumber):
        poll_vote = OptionPollVote(voter, publication, option)
        self.interactors.vote().vote(poll_vote)


if __name__ == "__main__":
    unittest.main()
