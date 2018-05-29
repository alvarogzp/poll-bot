from poll.domain.model.poll.poll import PollNumber
from poll.presentation.model.poll.poll import PollIdViewModel


class PollNumberMapper:
    @staticmethod
    def map_poll_number(number: PollNumber) -> PollIdViewModel:
        return PollIdViewModel(
            str(number.number)
        )

    @staticmethod
    def unmap_poll_number(poll_id: PollIdViewModel) -> PollNumber:
        return PollNumber(
            int(poll_id.id)
        )
