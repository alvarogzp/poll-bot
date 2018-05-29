from poll.domain.model.poll.user import PollUser


class PollVoteViewModel:
    def __init__(self, user: PollUser):
        self.user = user


class OptionPollVoteViewModel(PollVoteViewModel):
    def __init__(self, user: PollUser):
        super().__init__(user)
