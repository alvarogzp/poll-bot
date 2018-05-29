from sqlite_framework.component.component import SqliteStorageComponent

from poll.domain.exception import NotFoundError


class BasePollSqliteStorageComponent(SqliteStorageComponent):
    @staticmethod
    def _next_number(last_number: int) -> int:
        if last_number is not None:
            return last_number + 1
        return 1

    @staticmethod
    def _check_not_none(value, name: str = "key", hint=None):
        if value is None:
            raise NotFoundError(name, hint)
