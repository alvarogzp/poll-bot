from poll.domain.model.poll.settings.anonymity import PollAnonymity
from poll.domain.model.poll.settings.type import PollType
from poll.domain.model.user.settings import UserSettings
from poll.domain.model.user.user import User


class UserSettingsRepository:
    def set_user_poll_type(self, user: User, poll_type: PollType):
        raise NotImplementedError()

    def set_user_poll_anonymity(self, user: User, anonymity: PollAnonymity):
        raise NotImplementedError()

    def get_user_settings(self, user: User) -> UserSettings:
        raise NotImplementedError()
