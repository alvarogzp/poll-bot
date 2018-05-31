from bot.api.api import Api

from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel
from poll.presentation.telegram.bot.logger import TelegramPollLogger
from poll.presentation.telegram.bot.view.base import BaseView
from poll.presentation.view.publish import PublishPollView


class PublishPoll(BaseView, PublishPollView):
    def __init__(self, api: Api, logger: TelegramPollLogger):
        super().__init__(api)
        self.logger = logger

    def poll_published(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        self.logger.published_poll(user, poll_id, publication)
