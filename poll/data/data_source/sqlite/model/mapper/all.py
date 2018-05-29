from poll.data.data_source.sqlite.component.poll.option import PollOptionSqliteComponent
from poll.data.data_source.sqlite.component.poll.publication import PollPublicationSqliteComponent
from poll.data.data_source.sqlite.component.poll.vote.option import PollVoteOptionSqliteComponent
from poll.data.data_source.sqlite.component.user.user import UserSqliteComponent
from poll.data.data_source.sqlite.model.mapper.info import PollInfoMapper
from poll.data.data_source.sqlite.model.mapper.option import FullPollOptionMapper
from poll.data.data_source.sqlite.model.mapper.vote import OptionPollVoteMapper, PollVoteMapper


class SqliteModelMappers:
    def __init__(self, user: UserSqliteComponent, option: PollOptionSqliteComponent,
                 publication: PollPublicationSqliteComponent, option_vote: PollVoteOptionSqliteComponent):
        self.info = PollInfoMapper(user)
        self.option_vote = OptionPollVoteMapper(user, option, publication)
        vote = PollVoteMapper(user, publication)
        self.option = FullPollOptionMapper(option_vote, vote)
