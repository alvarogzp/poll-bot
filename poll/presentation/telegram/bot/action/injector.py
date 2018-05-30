from bot.action.core.action import Action

from poll.data.data_source.sqlite.sqlite import DATABASE_FILENAME
from poll.inject.injector.all.all import Injector


class InjectorAction(Action):
    def post_setup(self):
        api = self.api.no_async
        debug = self.config.debug()
        database_filename = DATABASE_FILENAME
        self.state.setup()
        worker = self.scheduler.io_worker
        logger = self.cache.logger
        injector = Injector(api, debug, database_filename, worker, logger)
        self.cache.injector = injector.telegram().action()
