from acceptance_core_py.helpers import env
from testing_projects_common.url_builders.base_url_builder import BaseUrlBuilder


class MainPageUrlBuilder(BaseUrlBuilder):
    def get_url_to_open(self) -> str:
        main_page_url = env.get_testing_project_url_data().origin_url
        return main_page_url
