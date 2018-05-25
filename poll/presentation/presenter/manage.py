from poll.domain.interactors.bot.manage import BotManagePollInteractor
from poll.domain.interactors.poll.get import GetPollInteractor
from poll.domain.model.poll.option import PollOptionNumber
from poll.domain.model.poll.poll import PollNumber
from poll.presentation.model.mapper.full.poll import FullPollMapper
from poll.presentation.model.mapper.info import PollInfoMapper
from poll.presentation.model.mapper.option import PollOptionNumberMapper
from poll.presentation.model.mapper.poll import PollNumberMapper
from poll.presentation.model.mapper.settings import PollSettingsMapper
from poll.presentation.model.mapper.user import UserMapper
from poll.presentation.model.message import MessageViewModel
from poll.presentation.view.manage import ManagePollView


class ManagePollPresenter:
    def __init__(self, view: ManagePollView, manage: BotManagePollInteractor, get: GetPollInteractor,
                 mapper_user: UserMapper, mapper_poll_number: PollNumberMapper,
                 mapper_poll_option_number: PollOptionNumberMapper, mapper_poll_settings: PollSettingsMapper,
                 mapper_poll_info: PollInfoMapper,
                 mapper_full_poll: FullPollMapper):
        self.view = view
        self.manage = manage
        self.get = get
        self.mapper_user = mapper_user
        self.mapper_poll_number = mapper_poll_number
        self.mapper_poll_settings = mapper_poll_settings
        self.mapper_poll_option_number = mapper_poll_option_number
        self.mapper_poll_info = mapper_poll_info
        self.mapper_full_poll = mapper_full_poll

    def start(self, message: MessageViewModel):
        settings = self.manage.start(message.user)
        settings = self.mapper_poll_settings.map_poll_settings(settings)
        self.view.started(message, settings)

    def message(self, message: MessageViewModel):
        user = self.mapper_user.unmap_user(message.user)
        number = self.manage.message(user, message.text)
        if isinstance(number, PollNumber):
            info = self.get.info(user, number)
            number = self.mapper_poll_number.map_poll_number(number)
            info = self.mapper_poll_info.map_poll_info(info)
            self.view.poll_created(message, number, info)
        elif isinstance(number, PollOptionNumber):
            info = self.get.option_info(user, self.get.last(user), number)
            number = self.mapper_poll_option_number.map_poll_option_number(number)
            self.view.option_added(message, number, info)
        elif number is None:
            self.view.message_ignored(message)

    def done(self, message: MessageViewModel):
        user = message.user
        number = self.manage.complete(user)
        if isinstance(number, PollNumber):
            full_poll = self.get.by_number(user, number)
            number = self.mapper_poll_number.map_poll_number(number)
            full_poll = self.mapper_full_poll.map_full_poll(full_poll)
            self.view.poll_completed(message, number, full_poll)
        else:
            self.view.nothing_to_complete(message)

    def cancel(self, message: MessageViewModel):
        user = message.user
        cancelled_poll = self.manage.cancel(user)
        if isinstance(cancelled_poll, PollNumber):
            cancelled_poll = self.mapper_poll_number.map_poll_number(cancelled_poll)
            self.view.poll_cancelled(message, cancelled_poll)
        elif cancelled_poll:
            self.view.back_to_idle(message)
        else:
            self.view.nothing_to_cancel(message)
