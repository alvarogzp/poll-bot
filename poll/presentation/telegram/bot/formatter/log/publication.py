from bot.action.util.textformat import FormattedText

from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel
from poll.presentation.telegram.bot.formatter.log.base import BaseLogFormatter
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class PublicationLogFormatter(BaseLogFormatter):
    def __init__(self, mapper_user: UserViewModelMapper):
        self.mapper_user = mapper_user

    def published_poll(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        return self._message(
            self._publication_as_title(publication),
            self._user(user),
            self._poll_id(poll_id)
        )

    def _user(self, user: UserViewModel, label: str = "From"):
        user = self.mapper_user.map_user(user)
        return super()._user(user, label)

    @staticmethod
    def _poll_id(poll_id: PollIdViewModel):
        return FormattedText().normal("Poll id: {id_prefix}{id}").start_format()\
            .bold(id_prefix="#", id=poll_id.id).end_format()

    @staticmethod
    def _publication_as_title(publication: PublicationViewModel):
        return FormattedText().normal("{publication}").start_format()\
            .bold(publication=publication.id).end_format()
