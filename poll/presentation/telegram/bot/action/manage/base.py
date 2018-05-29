from bot.action.core.action import Action

from poll.presentation.presenter.manage import ManagePollPresenter
from poll.presentation.telegram.bot.mapper.message import MessageViewModelMapper


class BaseManageAction(Action):
    def __init__(self):
        super().__init__()
        self.manage = None  # type: ManagePollPresenter
        self.mapper_message = None  # type: MessageViewModelMapper

    def inject(self, manage: ManagePollPresenter, mapper_message: MessageViewModelMapper):
        self.manage = manage
        self.mapper_message = mapper_message

    def post_setup(self):
        self.cache.injector.manage(self)

    def _message(self, event):
        return self.mapper_message.unmap_message(event.message)
