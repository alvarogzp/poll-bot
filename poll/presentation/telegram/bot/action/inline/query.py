from bot.action.core.action import Action

from poll.presentation.presenter.search import SearchPollPresenter
from poll.presentation.telegram.bot.mapper.query import QueryViewModelMapper


class SearchPollAction(Action):
    def __init__(self):
        super().__init__()
        self.search = None  # type: SearchPollPresenter
        self.mapper_query = None  # type: QueryViewModelMapper

    def inject(self, search: SearchPollPresenter, mapper_query: QueryViewModelMapper):
        self.search = search
        self.mapper_query = mapper_query

    def post_setup(self):
        self.cache.injector.search(self)

    def process(self, event):
        query = self.mapper_query.unmap_query(event.query)
        self.search.search(query)
