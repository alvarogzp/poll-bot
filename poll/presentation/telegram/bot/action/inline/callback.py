from bot.action.core.action import Action

from poll.presentation.presenter.vote import VotePollPresenter
from poll.presentation.telegram.bot.mapper.action import PublicationActionViewModelMapper
from poll.presentation.telegram.bot.mapper.option import PollOptionIdViewModelMapper


class PublishedPollAction(Action):
    def __init__(self):
        super().__init__()
        self.vote = None  # type: VotePollPresenter
        self.mapper_action = None  # type: PublicationActionViewModelMapper
        self.mapper_option = None  # type: PollOptionIdViewModelMapper

    def inject(self, vote: VotePollPresenter, mapper_action: PublicationActionViewModelMapper,
               mapper_option: PollOptionIdViewModelMapper):
        self.vote = vote
        self.mapper_action = mapper_action
        self.mapper_option = mapper_option

    def post_setup(self):
        self.cache.injector.action(self)

    def process(self, event):
        query = event.query
        action = self.mapper_action.unmap_publication_action(query)
        option = self.mapper_option.unmap_option(query.data_)
        self.vote.vote(action, option)
