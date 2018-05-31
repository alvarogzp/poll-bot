from bot.action.util.textformat import FormattedText
from bot.logger.logger import Logger

from poll.domain.logger import PollLogger
from poll.presentation.telegram.bot.formatter.log.repository import RepositoryLogFormatter


LOG_TAG_MIGRATION = FormattedText().bold("MIGRATION")


class TelegramPollLogger(PollLogger):
    def __init__(self, logger: Logger, repository_log_formatter: RepositoryLogFormatter):
        self.logger = logger
        self.repository_log_formatter = repository_log_formatter

    def repository_component_migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                                       about_to_migrate_to_version: int):
        self.logger.log(
            LOG_TAG_MIGRATION,
            self.repository_log_formatter.repository_component_migration(
                component, migration_type, old_version, new_version, about_to_migrate_to_version
            )
        )
