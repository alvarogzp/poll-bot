from typing import Tuple

from poll.domain.interactors.bot.manage import BotManagePollInteractor
from poll.domain.interactors.bot.search import BotSearchPollInteractor
from poll.domain.interactors.poll.get import GetPollInteractor
from poll.domain.interactors.poll.publish import PublishPollInteractor
from poll.domain.interactors.poll.vote import VotePollInteractor
from poll.domain.model.poll.full.poll import FullPoll, FullOptionPoll
from poll.domain.model.poll.option import PollOptionNumber
from poll.domain.model.poll.poll import PollNumber
from poll.domain.model.poll.publication import PollPublication
from poll.domain.model.poll.user import PollUser
from poll.domain.model.poll.vote import OptionPollVote
from poll.domain.model.user.user import User
from poll_test.integration.interactors.base import BaseIntegrationTest


ANY_MESSAGE_ID = "sadfjaiosgfnaso"

ANY_VOTER = PollUser(342534, "voter", "Any Voter")

ANY_OWNER = PollUser(324, "testowner", "Test Owner")


class BotInteractorsTest(BaseIntegrationTest):
    def setUp(self):
        self._setup()
        poll_interactor = self.injector.poll_interactor()
        bot_interactor = self.injector.bot_interactor()
        self.action = BotAction(
            bot_interactor.manage(), bot_interactor.search(), poll_interactor.get(), poll_interactor.publish(),
            poll_interactor.vote()
        )

    def test_create_search_publish_vote_poll(self):
        owner = ANY_OWNER

        self._create_poll(owner)

        search_text = "#1"

        self._search_poll(owner, search_text)

        message_id = ANY_MESSAGE_ID
        result_id = "1"

        self._publish_poll(owner, result_id, message_id)

        voter = ANY_VOTER

        self._vote(voter, message_id, "2")
        self._vote(voter, message_id, "1")

        self._vote(owner, message_id, "1")

        self._vote(voter, message_id, "1")
        self._vote(voter, message_id, "3")

        self._vote(owner, message_id, "2")

    def _create_poll(self, user: PollUser, options: int = 3):
        self.action.start(user)
        self.action.message(user, "any title")
        for option in range(options):
            self.action.message(user, "option {option}".format(option=option+1))
        full_poll = self.action.done(user)
        self._print(full_poll)

    def _search_poll(self, user: User, text: str):
        full_poll = self.action.search(user, text)
        if full_poll:
            number, full_poll = full_poll
            self._print(full_poll)
            return number

    def _publish_poll(self, user: User, result_id: str, message_id: str):
        full_poll = self.action.sent(user, result_id, message_id)
        self._print(full_poll)

    def _vote(self, user: PollUser, message_id: str, data: str):
        full_poll = self.action.vote(user, message_id, data)
        self._print(full_poll)

    @staticmethod
    def _print(full_poll: FullPoll):
        assert isinstance(full_poll, FullOptionPoll)
        text = "----------\n{title}\n\n{options}\n\nTotal votes: {vote_count}\n----------".format(
            title=full_poll.info.title,
            options="\n".join(
                "{name} [{vote_count}]\n{votes}".format(
                    name=option.info.name,
                    vote_count=len(option.votes),
                    votes="\n".join(
                        " - {user}".format(user=vote.user.name)
                        for vote in option.votes
                    )
                )
                for option in full_poll.options.options
            ),
            vote_count=sum((len(option.votes) for option in full_poll.options.options))
        )
        print(text)


class BotAction:
    def __init__(self, interactor_manage: BotManagePollInteractor, interactor_search: BotSearchPollInteractor,
                 interactor_get: GetPollInteractor, interactor_publish: PublishPollInteractor,
                 interactor_vote: VotePollInteractor):
        self.interactor_manage = interactor_manage
        self.interactor_search = interactor_search
        self.interactor_get = interactor_get
        self.interactor_publish = interactor_publish
        self.interactor_vote = interactor_vote

    def start(self, user: User):
        self.interactor_manage.start(user)

    def message(self, user: PollUser, text: str):
        return self.interactor_manage.message(user, text)

    def done(self, user: User) -> FullPoll:
        number = self.interactor_manage.complete(user)
        return self.interactor_get.by_number(user, number)

    def search(self, user: User, text: str) -> Tuple[PollNumber, FullPoll]:
        return self.interactor_search.search(user, text)

    def sent(self, user: User, result_id: str, message_id: str) -> FullPoll:
        number = PollNumber(int(result_id))
        publication = PollPublication(message_id)
        self.interactor_publish.publish(user, number, publication)
        return self.interactor_get.by_publication(publication)

    def vote(self, user: PollUser, message_id: str, data: str) -> FullPoll:
        publication = PollPublication(message_id)
        option = PollOptionNumber(int(data))
        vote = OptionPollVote(user, publication, option)
        self.interactor_vote.vote(vote)
        return self.interactor_get.by_publication(publication)
