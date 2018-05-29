from typing import Sequence

from bot.api.api import Api

from poll.presentation.model.poll.full.poll import FullPollViewModel
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.query import QueryViewModel
from poll.presentation.telegram.bot.formatter.poll.inline.result import PollInlineResultFormatter
from poll.presentation.telegram.bot.view.base import BaseView
from poll.presentation.view.search import SearchPollView


class SearchPoll(BaseView, SearchPollView):
    def __init__(self, api: Api, inline_result_formatter: PollInlineResultFormatter):
        super().__init__(api)
        self.inline_result_formatter = inline_result_formatter

    def poll_result(self, query: QueryViewModel, poll_id: PollIdViewModel, full_poll: FullPollViewModel):
        inline_result = self.inline_result_formatter.inline_result(poll_id, full_poll)
        self._answer_query(
            inline_query_id=query.id,
            results=[inline_result],
            cache_time=5,  # as the poll result can be modified by voting, use minimum caching only to reduce bot load
            is_personal=True
        )

    def no_results(self, query: QueryViewModel):
        self._answer_query(
            inline_query_id=query.id,
            results=[],
            cache_time=10,  # reduce cache time as user could create new polls that make the query return results
            is_personal=True,
            switch_pm_text="No polls found, try creating a new one!",
            switch_pm_parameter="no_results"
        )

    def no_query(self, query: QueryViewModel):
        self._answer_query(
            inline_query_id=query.id,
            results=[],
            cache_time=3600,  # it is safe to cache the no-query result for more than the default of 5 minutes
            switch_pm_text="Create a new poll",
            switch_pm_parameter="empty_query"
        )

    def _answer_query(self,
                      inline_query_id: str,
                      results: Sequence,
                      cache_time: int = None,
                      is_personal: bool = None,
                      next_offset: str = None,
                      switch_pm_text: str = None,
                      switch_pm_parameter: str = None):
        result = {
            "inline_query_id": inline_query_id,
            "results": results
        }
        if cache_time is not None:
            result["cache_time"] = cache_time
        if is_personal is not None:
            result["is_personal"] = is_personal
        if next_offset is not None:
            result["next_offset"] = next_offset
        if switch_pm_text is not None:
            result["switch_pm_text"] = switch_pm_text
        if switch_pm_parameter is not None:
            result["switch_pm_parameter"] = switch_pm_parameter
        self.api.answerInlineQuery(**result)
