from bot.action.util.format import UserFormatter
from bot.action.util.textformat import FormattedText

from poll.presentation.model.poll.poll import PollIdViewModel
from poll.presentation.model.publication.publication import PublicationViewModel
from poll.presentation.model.user import UserViewModel
from poll.presentation.telegram.bot.mapper.user import UserViewModelMapper


class LogFormatter:
    def __init__(self, mapper_user: UserViewModelMapper):
        self.mapper_user = mapper_user

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

    def published_poll(self, user: UserViewModel, poll_id: PollIdViewModel, publication: PublicationViewModel):
        return self._message(
            self._publication_as_title(publication),
            self._user(user),
            self._poll_id(poll_id)
        )

    def _user(self, user: UserViewModel, label: str = "From"):
        user = self.mapper_user.map_user(user)
        return FormattedText().normal("{label}: {user}").start_format()\
            .normal(label=label).bold(user=UserFormatter(user).full_data).end_format()

    @staticmethod
    def _poll_id(poll_id: PollIdViewModel):
        return FormattedText().normal("Poll id: {id_prefix}{id}").start_format()\
            .bold(id_prefix="#", id=poll_id.id).end_format()

    @staticmethod
    def _publication_as_title(publication: PublicationViewModel):
        return FormattedText().normal("{publication}").start_format()\
            .bold(publication=publication.id).end_format()

    @staticmethod
    def _message(*message_parts: FormattedText):
        return FormattedText().newline().join(message_parts)
