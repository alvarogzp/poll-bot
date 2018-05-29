from poll.domain.model.poll.info import PollInfo
from poll.presentation.model.mapper.settings import PollSettingsMapper
from poll.presentation.model.poll.info import PollInfoViewModel


class PollInfoMapper:
    def __init__(self, mapper_settings: PollSettingsMapper):
        self.mapper_settings = mapper_settings

    def map_poll_info(self, info: PollInfo) -> PollInfoViewModel:
        return PollInfoViewModel(
            self.mapper_settings.map_poll_settings(info.settings),
            info.title
        )
