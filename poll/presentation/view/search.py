from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.query import QueryViewModel


class SearchPollView:
    def poll_result(self, query: QueryViewModel, poll_id: PollIdViewModel, full_poll: FullPollViewModel):
        raise NotImplementedError()

    def no_results(self, query: QueryViewModel):
        raise NotImplementedError()

    def no_query(self, query: QueryViewModel):
        raise NotImplementedError()
