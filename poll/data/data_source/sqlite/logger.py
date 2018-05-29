from sqlite_framework.log.logger import SqliteLogger

from poll.domain.logger import PollLogger


class PollLoggerAdapter(SqliteLogger):
    def __init__(self, logger: PollLogger):
        self.logger = logger

    def migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                  about_to_migrate_to_version: int):
        self.logger.repository_component_migration(
            component, migration_type, old_version, new_version, about_to_migrate_to_version
        )
