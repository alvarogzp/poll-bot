from poll.presentation.telegram.bot.action.manage.base import BaseManageAction


class PollMessageAction(BaseManageAction):
    def process(self, event):
        message = self._message(event)
        self.manage.message(message)
