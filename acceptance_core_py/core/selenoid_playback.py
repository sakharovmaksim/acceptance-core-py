import os


class SelenoidPlayback:
    local: str = "local"
    remote: str = "remote"

    def __init__(self):
        self.__playback_type: str = self.define_playback_type()

    @property
    def command_executor_url(self) -> str:
        """Возвращает хост, который нужно указать в конфиге Selenium клиента"""
        if self.__playback_type == self.remote:
            return "http://selenoid0.qa.ftt.local:4444/wd/hub"
        if self.__playback_type == self.local:
            return "http://localhost:4444/wd/hub"
        return self.__playback_type

    def define_playback_type(self) -> str:
        """Возвращает константу с типом окружения или то, что пользователь указал в pytest-конфиге"""
        playback_from_env = os.environ.get("SELENOID_PLAYBACK_TYPE", "LOCAL")
        if playback_from_env == "REMOTE":
            return self.remote
        if playback_from_env == "LOCAL":
            return self.local
        return playback_from_env
