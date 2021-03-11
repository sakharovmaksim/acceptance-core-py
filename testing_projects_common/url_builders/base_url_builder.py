from abc import ABC
from abc import abstractmethod


class BaseUrlBuilder(ABC):
    """Базовый билдер урла для страниц. От него должны наследоваться все билдеры урлов в проекте"""

    @abstractmethod
    def get_url_to_open(self) -> str:
        """Возвращает полный урл страницы, которую нужно открыть: 'https://your-host.ru/'"""
        pass
