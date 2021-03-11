import logging
from urllib.parse import urlsplit

from acceptance_core_py.helpers.utils import strings_utils


class TestingProjectUrlData:
    """Расположение данных: <scheme>://<netloc>/<path>?<query>#<fragment>"""

    def __init__(self, origin_url: str):
        self.__urlsplit_obj = urlsplit(origin_url)
        self.__origin_url: str = origin_url

    @property
    def origin_url(self) -> str:
        """Вернет то, что было передано в __init__() без всякой обработки"""
        result = self.__origin_url
        logging.info(f"Got testing project '{self.__origin_url=}'")
        return result

    @property
    def scheme(self) -> str:
        """Пример возвращаемого значения: 'https'"""
        result = self.__urlsplit_obj.scheme
        logging.debug(f"Got testing project scheme '{result}'")
        return result

    @property
    def netlock(self) -> str:
        """Пример возвращаемого значения: 'test.ao.mx7.ru'"""
        result = self.__urlsplit_obj.netloc
        logging.debug(f"Got testing project netlock '{result}'")
        return result

    @property
    def scheme_and_netloc(self) -> str:
        """Пример возвращаемого значения: 'https://test.ao.mx7.ru'"""
        result = self.scheme + "://" + self.netlock
        logging.info(f"Got testing project scheme and netloc URL '{result}'")
        return result

    def is_valid(self) -> bool:
        """Возвращает True, если урл не пустой и не содержит стандартное для браузера значение"""
        return bool(self.__origin_url) and not strings_utils.is_string_found_in(
            "data:", self.__origin_url
        )
