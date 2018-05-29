from bot.action.core.action import Action

from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.presenter.publish import PublishPollPresenter
from poll.presentation.telegram.bot.mapper.publication import PublicationViewModelMapper
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class ChosenPollAction(Action):
    def __init__(self):
        super().__init__()
        self.publish = None  # type: PublishPollPresenter
        self.mapper_user = None  # type: UserViewModelMapper
        self.mapper_publication = None  # type: PublicationViewModelMapper

    def inject(self, publish: PublishPollPresenter, mapper_user: UserViewModelMapper,
               mapper_publication: PublicationViewModelMapper):
        self.publish = publish
        self.mapper_user = mapper_user
        self.mapper_publication = mapper_publication

    def post_setup(self):
        self.cache.injector.chosen(self)

    def process(self, event):
        chosen_result = event.chosen_result
        user = self.mapper_user.unmap_user(chosen_result.from_)
        poll_id = PollIdViewModel(chosen_result.result_id)
        publication = self.mapper_publication.unmap_publication(chosen_result)
        self.publish.publish(user, poll_id, publication)
