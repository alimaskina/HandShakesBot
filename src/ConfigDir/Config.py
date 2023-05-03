import os
from yaml import load, FullLoader
from dotenv import load_dotenv, find_dotenv


class Config:
    """Class which know about configurations in config.yml. It is a singleton."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)

            with open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml', 'r') as f:
                config = load(f, Loader=FullLoader)
            cls._instance = super().__new__(cls)
            cls._instance.__dict__ = config

            load_dotenv(find_dotenv())
            cls._instance.__vktoken__ = os.getenv('VK_TOKEN')
            cls._instance.__tgtoken__ = os.getenv('TG_TOKEN')

        return cls._instance

    def get_vk_version(self):
        """Return version of vk_api from config.yaml."""
        return self._instance.__dict__['VK']['VK_VERSION']

    def get_vk_token(self):
        """Return token of vk_api"""
        return self._instance.__vktoken__

    def get_tg_token(self):
        """Return token of tg_bot"""
        return self._instance.__tgtoken__

    def get_platforms(self):
        """Return supported platforms (vk, facebook, etc) from config.yaml."""
        return self._instance.__dict__['PLATFORMS']

    def get_cash_path(self):
        """Return path with cash-file from config.yaml."""
        return self._instance.__dict__['CASH']['CASH_PATH']

    def get_cash_period(self):
        """Return period of caching from config.yaml."""
        return self._instance.__dict__['CASH']['CASH_PERIOD']

    def get_commands(self):
        """Return supported user commands from config.yaml."""
        return self._instance.__dict__['COMMANDS']

    def get_view_type(self):
        """Return type of view (console, web, etc) from config.yaml."""
        return self._instance.__dict__['VIEW']['VIEW_TYPE']

    def get_searcher_type(self):
        """Return type of algorithm which is used for searching a friends chain from config.yaml."""
        return self._instance.__dict__['SEARCHER']
