from abc import ABC, abstractmethod

from acceptance_core_py.core.actions import waiting_actions


class BasePage(ABC):

    @abstractmethod
    def wait_for_ready(self):
        pass
