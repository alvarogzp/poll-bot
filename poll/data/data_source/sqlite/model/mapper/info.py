from poll.data.data_source.sqlite.component.user.user import UserSqliteComponent
from poll.data.data_source.sqlite.model.poll.info import PollInfoData
from poll.data.data_source.sqlite.model.poll.user import PollUserData
from poll.domain.model.poll.info import PollInfo


class PollInfoMapper:
    def __init__(self, user: UserSqliteComponent):
        self.user = user

    @staticmethod
    def map_poll_info(info: PollInfo, poll_user_id: PollUserData) -> PollInfoData:
        return PollInfoData(
            poll_user_id,
            info.settings,
            info.title,
            info.complete
        )

    def unmap_poll_info(self, info: PollInfoData) -> PollInfo:
        owner = self.user.get_poll_user(info.owner)
        return PollInfo(
            owner,
            info.settings,
            info.title,
            info.complete
        )
