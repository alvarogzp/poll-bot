from poll.domain.interactors.bot.search import BotSearchPollInteractor
from poll.presentation.model.mapper.full.poll import FullPollMapper
from poll.presentation.model.mapper.poll import PollNumberMapper
from poll.presentation.model.query import QueryViewModel
from poll.presentation.view.search import SearchPollView


class SearchPollPresenter:
    def __init__(self, view: SearchPollView, interactor_search: BotSearchPollInteractor,
                 mapper_poll_number: PollNumberMapper, mapper_full_poll: FullPollMapper):
        self.view = view
        self.interactor_search = interactor_search
        self.mapper_poll_number = mapper_poll_number
        self.mapper_full_poll = mapper_full_poll

    def search(self, query: QueryViewModel):
        if not query.query:
            self.view.no_query(query)
        else:
            result = self.interactor_search.search(query.user, query.query)
            if result is not None:
                number, full_poll = result
                poll_id = self.mapper_poll_number.map_poll_number(number)
                full_poll = self.mapper_full_poll.map_full_poll(full_poll)
                self.view.poll_result(query, poll_id, full_poll)
            else:
                self.view.no_results(query)
