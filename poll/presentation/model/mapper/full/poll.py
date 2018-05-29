from poll.domain.model.poll.full.poll import FullOptionPoll, FullPoll
from poll.presentation.model.mapper.full.option import FullPollOptionMapper
from poll.presentation.model.mapper.info import PollInfoMapper
from poll.presentation.model.poll.full.poll import FullOptionPollViewModel, FullPollViewModel


class FullOptionPollMapper:
    def __init__(self, mapper_poll_info: PollInfoMapper, mapper_full_poll_option: FullPollOptionMapper):
        self.mapper_poll_info = mapper_poll_info
        self.mapper_full_poll_option = mapper_full_poll_option

    def map_full_option_poll(self, poll: FullOptionPoll) -> FullOptionPollViewModel:
        return FullOptionPollViewModel(
            self.mapper_poll_info.map_poll_info(poll.info),
            self.mapper_full_poll_option.map_full_poll_option_iter(poll.options)
        )


class FullPollMapper:
    def __init__(self, mapper_full_option_poll: FullOptionPollMapper):
        self.mapper_full_option_poll = mapper_full_option_poll

    def map_full_poll(self, poll: FullPoll) -> FullPollViewModel:
        if isinstance(poll, FullOptionPoll):
            return self.mapper_full_option_poll.map_full_option_poll(poll)
        raise NotImplementedError()
