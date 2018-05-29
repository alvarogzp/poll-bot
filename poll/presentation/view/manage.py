from poll.domain.model.poll.option import PollOptionInfo
from poll.presentation.model.message import MessageViewModel
from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.poll.info import PollInfoViewModel
from poll.presentation.model.poll.option import PollOptionIdViewModel
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.poll.settings import PollSettingsViewModel


class ManagePollView:
    def started(self, message: MessageViewModel, settings: PollSettingsViewModel):
        raise NotImplementedError()

    def poll_created(self, message: MessageViewModel, poll_id: PollIdViewModel, info: PollInfoViewModel):
        raise NotImplementedError()

    def option_added(self, message: MessageViewModel, option_id: PollOptionIdViewModel, info: PollOptionInfo):
        raise NotImplementedError()

    def message_ignored(self, message: MessageViewModel):
        raise NotImplementedError()

    def poll_completed(self, message: MessageViewModel, poll_id: PollIdViewModel, full_poll: FullPollViewModel):
        raise NotImplementedError()

    def poll_cancelled(self, message: MessageViewModel, poll_id: PollIdViewModel):
        raise NotImplementedError()

    def nothing_to_complete(self, message: MessageViewModel):
        raise NotImplementedError()

    def nothing_to_cancel(self, message: MessageViewModel):
        raise NotImplementedError()

    def back_to_idle(self, message: MessageViewModel):
        raise NotImplementedError()
