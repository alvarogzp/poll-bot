from poll.presentation.telegram.bot.action.manage.base import BaseManageAction


class StartCommandAction(BaseManageAction):
    def process(self, event):
        message = self._message(event)
        self.manage.start(message)


class DoneCommandAction(BaseManageAction):
    def process(self, event):
        message = self._message(event)
        self.manage.done(message)


class CancelCommandAction(BaseManageAction):
    def process(self, event):
        message = self._message(event)
        self.manage.cancel(message)
