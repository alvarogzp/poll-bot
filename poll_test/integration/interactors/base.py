import traceback
from unittest import TestCase

from bot.multithreading.work import Work
from bot.multithreading.worker import Worker
from bot.multithreading.worker.immediate import ImmediateWorker
from sqlite_framework.log.impl import BasicSqliteLogger

from poll.inject.injector.cache import InjectorCache
from poll.inject.injector.all.domain import DomainInjector


class BaseIntegrationTest(TestCase):
    def _setup(self):
        self.injector = self._build_injector()
        self.repository = self.injector.repository().poll_data_repository()
        self.interactors = self.injector.poll_interactor()

    def _build_injector(self) -> DomainInjector:
        return DomainInjector(
            InjectorCache(), True, ":memory:", BasicSqliteLogger(), ImmediateWorker(self._worker_error_handler)
        )

    @staticmethod
    def _worker_error_handler(error: BaseException, work: Work, worker: Worker):
        print("Error '{error}' on work '{work}' on worker '{worker}':".format(
            error=error, work=work.name, worker=worker.name
        ))
        traceback.print_exc()
