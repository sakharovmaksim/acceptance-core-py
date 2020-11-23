from acceptance_core_py.helpers import env
from content.url_builders.base_url_builder import BaseUrlBuilder


class MainPageUrlBuilder(BaseUrlBuilder):
    def get_url_to_open(self) -> str:
        main_page_url = env.get_base_url()
        return main_page_url
