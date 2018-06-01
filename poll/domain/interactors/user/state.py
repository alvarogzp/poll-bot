from poll.domain.model.user.state import State
from poll.domain.model.user.user import User
from poll.domain.repository.user.state import UserStateRepository


class UserStateInteractor:
    def __init__(self, state: UserStateRepository):
        self.state = state

    def set_state(self, user: User, state: State):
        self.state.set_state(user, state)

    def get_state(self, user: User):
        return self.state.get_state(user)
