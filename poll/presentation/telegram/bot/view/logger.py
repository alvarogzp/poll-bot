from bot.action.util.textformat import FormattedText
from bot.api.api import Api
from bot.logger.logger import Logger

from poll.domain.logger import PollLogger
from poll.presentation.telegram.bot.formatter.log import LogFormatter
from poll.presentation.telegram.bot.view.base import BaseView


LOG_TAG_MIGRATION = FormattedText().bold("MIGRATION")


class TelegramPollLogger(BaseView, PollLogger):
    def __init__(self, api: Api, logger: Logger, log_formatter: LogFormatter):
        super().__init__(api)
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
