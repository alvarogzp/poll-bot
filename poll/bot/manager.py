from bot.action.core.action import ActionGroup
from bot.action.core.command import CommandAction
from bot.action.core.filter import MessageAction, TextMessageAction, NoPendingAction, PendingAction
from bot.action.standard.about import AboutAction, VersionAction
from bot.action.standard.admin import RestartAction, EvalAction, AdminActionWithErrorMessage, HaltAction
from bot.action.standard.admin.config_status import ConfigStatusAction
from bot.action.standard.admin.fail import FailAction
from bot.action.standard.admin.instance import InstanceAction
from bot.action.standard.admin.state import StateAction
from bot.action.standard.answer import AnswerAction
from bot.action.standard.asynchronous import AsynchronousAction
from bot.action.standard.benchmark import BenchmarkAction, WorkersAction
from bot.action.standard.info.action import UserInfoAction
from bot.action.standard.internationalization import InternationalizationAction
from bot.action.standard.logger import LoggerAction
from bot.action.standard.perchat import PerChatAction
from bot.bot import Bot

from poll import project_info


class BotManager:
    def __init__(self):
        self.bot = Bot(project_info.name)

    def setup_actions(self):
        self.bot.set_action(
            ActionGroup(
                LoggerAction(reuse_max_length=2000, reuse_max_time=1, reuse_max_number=10).then(

                    MessageAction().then(
                        PerChatAction().then(

                            InternationalizationAction().then(
                                TextMessageAction().then(

                                    CommandAction("about").then(
                                        AboutAction(
                                            project_info.name,
                                            authors=project_info.authors_credits,
                                            is_open_source=project_info.is_open_source,
                                            url=project_info.url,
                                            license_name=project_info.license_name,
                                            license_url=project_info.license_url,
                                            donation_addresses=project_info.donation_addresses
                                        )
                                    ),

                                    CommandAction("version").then(
                                        VersionAction(
                                            project_info.name,
                                            project_info.url + "/releases"
                                        )
                                    ),

                                    CommandAction("me", is_personal=True).then(
                                        UserInfoAction(always_sender=True)
                                    ),

                                    CommandAction("benchmark").then(
                                        AdminActionWithErrorMessage().then(
                                            AsynchronousAction("benchmark").then(
                                                BenchmarkAction()
                                            )
                                        )
                                    ),
                                    CommandAction("restart").then(
                                        AdminActionWithErrorMessage().then(
                                            RestartAction()
                                        )
                                    ),
                                    CommandAction("halt").then(
                                        AdminActionWithErrorMessage().then(
                                            HaltAction()
                                        )
                                    ),
                                    CommandAction("eval").then(
                                        AdminActionWithErrorMessage().then(
                                            EvalAction()
                                        )
                                    ),
                                    CommandAction("state").then(
                                        AdminActionWithErrorMessage().then(
                                            StateAction()
                                        )
                                    ),
                                    CommandAction("config").then(
                                        AdminActionWithErrorMessage().then(
                                            ConfigStatusAction()
                                        )
                                    ),
                                    CommandAction("instance").then(
                                        AdminActionWithErrorMessage().then(
                                            InstanceAction()
                                        )
                                    ),
                                    CommandAction("workers").then(
                                        AdminActionWithErrorMessage().then(
                                            WorkersAction()
                                        )
                                    ),
                                    CommandAction("fail").then(
                                        AdminActionWithErrorMessage().then(
                                            FailAction()
                                        )
                                    )

                                )
                            )
                        )
                    ),

                    NoPendingAction().then(
                        MessageAction().then(
                            PerChatAction().then(
                                TextMessageAction().then(
                                    CommandAction("ping").then(
                                        AnswerAction("Up and running!")
                                    )
                                )
                            )
                        )
                    ),

                    PendingAction().then(
                        MessageAction().then(
                            PerChatAction().then(
                                TextMessageAction().then(
                                    CommandAction("ping").then(
                                        AnswerAction("I'm back! Sorry for the delay...")
                                    )
                                )
                            )
                        )
                    )

                )
            )
        )

    def run(self):
        self.bot.run()
