from bot.action.util.textformat import FormattedText
from bot.logger.logger import Logger

from poll.domain.logger import PollLogger
from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel
from poll.presentation.telegram.bot.formatter.log.publication import PublicationLogFormatter
from poll.presentation.telegram.bot.formatter.log.repository import RepositoryLogFormatter


LOG_TAG_MIGRATION = FormattedText().bold("MIGRATION")
LOG_TAG_PUBLICATION = FormattedText().normal("PUBLICATION")


class TelegramPollLogger(PollLogger):
    def __init__(self, logger: Logger, repository_log_formatter: RepositoryLogFormatter,
                 publication_log_formatter: PublicationLogFormatter):
        self.logger = logger
        self.repository_log_formatter = repository_log_formatter
        self.publication_log_formatter = publication_log_formatter

    def repository_component_migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                                       about_to_migrate_to_version: int):
        self.logger.log(
            LOG_TAG_MIGRATION,
            self.repository_log_formatter.repository_component_migration(
                component, migration_type, old_version, new_version, about_to_migrate_to_version
            )
        )

    def published_poll(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        self.logger.log(
            LOG_TAG_PUBLICATION,
            self.publication_log_formatter.published_poll(user, poll_id, publication)
        )
