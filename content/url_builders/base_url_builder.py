from abc import ABC, abstractmethod


class BaseUrlBuilder(ABC):

    @abstractmethod
    def get_url_to_open(self) -> str:
        """Return full page url: 'https://your-host.ru/'"""
        pass
