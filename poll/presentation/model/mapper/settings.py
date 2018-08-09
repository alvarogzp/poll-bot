from poll.domain.model.poll.settings.anonymity import PERSONAL, ANONYMOUS, ANONYMOUS_AND_ONLY_TO_CREATOR, PollAnonymity
from poll.domain.model.poll.settings.settings import PollSettings
from poll.domain.model.poll.settings.type import PollType, SINGLE_VOTE, MULTI_VOTE, MULTI_VOTE_LIMITED, OPEN, RANGE
from poll.presentation.model.poll.settings import PollTypeViewModel, PollAnonymityViewModel, PollSettingsViewModel


POLL_TYPES = {
    SINGLE_VOTE: "single vote",
    MULTI_VOTE: "doodle",
    MULTI_VOTE_LIMITED: "limited doodle",
    OPEN: "board",
    RANGE: "choose in a range"
}

POLL_ANONYMITIES = {
    PERSONAL: "personal",
    ANONYMOUS: "anonymous",
    ANONYMOUS_AND_ONLY_TO_CREATOR: "anonymous and only creator can see results"
}


class PollTypeMapper:
    @staticmethod
    def map_poll_type(poll_type: PollType) -> PollTypeViewModel:
        return PollTypeViewModel(
            POLL_TYPES[poll_type]
        )


class PollAnonymityMapper:
    @staticmethod
    def map_poll_anonymity(anonymity: PollAnonymity) -> PollAnonymityViewModel:
        return PollAnonymityViewModel(
            POLL_ANONYMITIES[anonymity]
        )


class PollSettingsMapper:
    def __init__(self, mapper_poll_type: PollTypeMapper, mapper_poll_anonymity: PollAnonymityMapper):
        self.mapper_type = mapper_poll_type
        self.mapper_anonymity = mapper_poll_anonymity

    def map_poll_settings(self, settings: PollSettings) -> PollSettingsViewModel:
        return PollSettingsViewModel(
            self.mapper_type.map_poll_type(settings.type),
            self.mapper_anonymity.map_poll_anonymity(settings.anonymity)
        )
