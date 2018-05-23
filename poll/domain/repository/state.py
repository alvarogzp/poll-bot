from poll.domain.model.user.state import State
from poll.domain.model.user.user import User


class UserStateRepository:
    def set_state(self, user: User, state: State):
        raise NotImplementedError()

    def get_state(self, user: User) -> State:
        raise NotImplementedError()
