from poll.domain.model.poll.option import PollOptionNumber
from poll.presentation.model.poll.option import PollOptionIdViewModel


class PollOptionNumberMapper:
    @staticmethod
    def map_poll_option_number(option: PollOptionNumber) -> PollOptionIdViewModel:
        return PollOptionIdViewModel(
            str(option.number)
        )

    @staticmethod
    def unmap_poll_option_number(option_id: PollOptionIdViewModel) -> PollOptionNumber:
        return PollOptionNumber(
            int(option_id.id)
        )
