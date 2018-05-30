from bot.action.util.textformat import FormattedText


class LogFormatter:
    def repository_component_migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                                       about_to_migrate_to_version: int):
        return self._message(
            self._about_to_migrate_to_version(about_to_migrate_to_version),
            self._component(component),
            self._migration_type(migration_type),
            self._migration_old_version(old_version),
            self._migration_new_version(new_version)
        )

    @staticmethod
    def _about_to_migrate_to_version(version: int):
        return FormattedText().normal("Migrating to version {version}").start_format()\
            .bold(version=version).end_format()

    @staticmethod
    def _component(component: str):
        return FormattedText().normal("Component: {name}").start_format()\
            .bold(name=component).end_format()

    @staticmethod
    def _migration_type(migration_type: str):
        return FormattedText().normal("Type: {type}").start_format()\
            .bold(type=migration_type).end_format()

    @staticmethod
    def _migration_old_version(old_version: int):
        return FormattedText().normal("From version: {version}").start_format()\
            .bold(version=old_version).end_format()

    @staticmethod
    def _migration_new_version(new_version: int):
        return FormattedText().normal("To version: {version}").start_format()\
            .bold(version=new_version).end_format()

    @staticmethod
    def _message(*message_parts: FormattedText):
        return FormattedText().newline().join(message_parts)
