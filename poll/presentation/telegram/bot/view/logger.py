from bot.action.util.textformat import FormattedText
from bot.logger.logger import Logger

from poll.domain.logger import PollLogger
from poll.presentation.telegram.bot.formatter.log import LogFormatter


LOG_TAG_MIGRATION = FormattedText().bold("MIGRATION")


class TelegramPollLogger(PollLogger):
    def __init__(self, logger: Logger, log_formatter: LogFormatter):
        self.logger = logger
        self.log_formatter = log_formatter

    def repository_component_migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                                       about_to_migrate_to_version: int):
        self.logger.log(LOG_TAG_MIGRATION, self.log_formatter.message(
            self.log_formatter.about_to_migrate_to_version(about_to_migrate_to_version),
            self.log_formatter.component(component),
            self.log_formatter.migration_type(migration_type),
            self.log_formatter.migration_old_version(old_version),
            self.log_formatter.migration_new_version(new_version)
        ))
