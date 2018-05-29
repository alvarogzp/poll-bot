from poll.presentation.model.poll.option import PollOptionIdViewModel


OPTION_ID_PREFIX = "option:"


class PollOptionIdViewModelMapper:
    @staticmethod
    def map_option(option: PollOptionIdViewModel) -> str:
        return OPTION_ID_PREFIX + option.id

    @staticmethod
    def unmap_option(option: str) -> PollOptionIdViewModel:
        if not option.startswith(OPTION_ID_PREFIX):
            raise Exception("illegal poll option '{option}'".format(option=option))
        option_id = option[len(OPTION_ID_PREFIX):]
        return PollOptionIdViewModel(
            option_id
        )
