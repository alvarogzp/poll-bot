from bot.action.util.textformat import FormattedText

from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel
from poll.presentation.telegram.bot.view.base import BaseView
from poll.presentation.view.publish import PublishPollView


class PublishPoll(BaseView, PublishPollView):
    def poll_published(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        text = FormattedText().normal(
            "You have just published poll #{id} on a chat.\n"
            "The publication id is {publication}.\n"
            "Send /publication_disable to disable these notifications."
        ).start_format().normal(
            id=poll_id.id
        ).bold(
            publication=publication.id
        ).end_format()
        self._send_to_user(text.build_message(), user)
