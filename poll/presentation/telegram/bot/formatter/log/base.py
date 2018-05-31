from bot.action.util.format import UserFormatter
from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject


class BaseLogFormatter:
    def _user(self, user: ApiObject, label: str = "From"):
        return FormattedText().normal("{label}: {user}").start_format()\
            .normal(label=label).bold(user=UserFormatter(user).full_data).end_format()

    @staticmethod
    def _message(*message_parts: FormattedText):
        return FormattedText().newline().join(message_parts)
