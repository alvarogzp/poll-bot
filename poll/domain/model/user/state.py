from poll.domain.model.base import Comparable


class State(Comparable):
    def __init__(self, state_id: int):
        super().__init__(state_id, State)
        self.id = state_id


INITIAL = State(0)

IDLE = State(1)
WAITING_TITLE = State(2)
WAITING_FIRST_OPTION = State(3)
WAITING_MORE_OPTIONS = State(4)


ADDING_OPTIONS_STATES = [WAITING_FIRST_OPTION, WAITING_MORE_OPTIONS]
INCOMPLETE_POLL_STATES = [WAITING_FIRST_OPTION, WAITING_MORE_OPTIONS]
READY_TO_COMPLETE_STATES = [WAITING_MORE_OPTIONS]
IDLE_STATES = [INITIAL, IDLE]


DEFAULT_STATE = INITIAL
