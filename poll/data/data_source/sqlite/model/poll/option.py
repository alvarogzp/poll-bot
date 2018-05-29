from poll.domain.model.poll.option import PollOption, PollOptionNumber, PollOptionInfo


class FullPollOptionData:
    def __init__(self, option_id: PollOption, number: PollOptionNumber, info: PollOptionInfo):
        self.id = option_id
        self.number = number
        self.info = info
