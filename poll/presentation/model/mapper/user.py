from poll.domain.model.poll.user import PollUser
from poll.presentation.model.user import UserViewModel


class UserMapper:
    def unmap_user(self, user: UserViewModel) -> PollUser:
        return PollUser(
            user.id,
            user.username,
            self._name(user)
        )

    @staticmethod
    def _name(user: UserViewModel):
        return " ".join(filter(None, (user.first_name, user.last_name)))
