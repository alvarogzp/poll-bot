from poll.domain.model.poll.settings.anonymity import PollAnonymity
from poll.domain.model.poll.settings.type import PollType
from poll.domain.model.user.settings import UserSettings
from poll.domain.model.user.user import User
from poll.domain.repository.user.settings import UserSettingsRepository


class UserSettingsInteractor:
    def __init__(self, settings: UserSettingsRepository):
        self.settings = settings

    def set_poll_type(self, user: User, poll_type: PollType):
        self.settings.set_user_poll_type(user, poll_type)

    def set_poll_anonymity(self, user: User, anonymity: PollAnonymity):
        self.settings.set_user_poll_anonymity(user, anonymity)

    def get(self, user: User) -> UserSettings:
        return self.settings.get_user_settings(user)
