import json
import time
import os
from src.ConfigDir.Config import Config
from src.SocialNetworkDir.APIs import APIFactory
from src.SocialNetworkDir.ChainSearcher import ChainSearcherFactory


class SocialNetwork:
    """Class which is responsible for all internal logic."""
    def __init__(self):
        self.__social_network_type = None
        self.__api = None
        self.__cash_path = ''
        self.__friends_ids = dict()
        self.__friends_names = dict()
        self.__config = Config()
        self.pull_data()

    def set_api(self, social_network_type):
        """Setter for api. This is where the social network we work with is installed."""
        self.__social_network_type = social_network_type
        self.__api = APIFactory().create_api(social_network_type=social_network_type)
        self.__cash_path = f"{self.__social_network_type}_{self.__config.get_cash_path()}"
        self.pull_data()

    def cash_data(self):
        """Cashing data about users."""
        if self.__cash_path == '':
            return
        for_load = {'friends_ids': self.__friends_ids, 'friends_names': self.__friends_names}
        with open(self.__cash_path, 'w') as outfile:
            json.dump(for_load, outfile)

    def pull_data(self):
        """Pull data about users from cash."""
        if self.__cash_path and os.path.exists(self.__cash_path):
            with open(self.__cash_path, 'r') as infile:
                data = json.load(infile)
            if 'friends_ids' in data and 'friends_names' in data:
                self.__friends_ids = data['friends_ids']
                self.__friends_names = data['friends_names']

    def __del__(self):
        try:
            self.cash_data()
        except NameError:
            pass

    def is_user_existing(self, user_nickname):
        """Return true if user with user_nickname exists."""
        if not self.__api.is_existing(user_nickname):
            return user_nickname

    def get_common_friends(self, user_nicknames):
        """Takes list of user nicknames and return their common friends."""
        common_friends_ids = set(self.__get_friends_ids(user_nicknames[0]))
        for user_nickname in user_nicknames[1:]:
            user_friends = set(self.__get_friends_ids(user_nickname))
            common_friends_ids = common_friends_ids.intersection(user_friends)
        common_friends = [self.__get_user_name(friend_id) for friend_id in common_friends_ids]
        return common_friends

    def __get_friends_ids(self, user_nickname):
        """Takes user's nickname and return his friend's ids."""
        friends_info = self.__friends_ids.get(user_nickname)
        if not friends_info or time.time() - friends_info['update_time'] > self.__config.get_cash_period():
            self.__friends_ids[user_nickname] = {"friends_ids": self.__api.get_friends_ids(user_nickname),
                                                 "update_time": time.time()}
        return self.__friends_ids[user_nickname]["friends_ids"]

    def __get_user_name(self, user_id):
        """Takes user's id and return his name."""
        user_info = self.__friends_names.get(user_id)
        if not user_info or time.time() - user_info['update_time'] > self.__config.get_cash_period():
            self.__friends_names[user_id] = {"friends_names": self.__api.get_user_name(user_id),
                                             "update_time": time.time()}
        return self.__friends_names[user_id]["friends_names"]

    def get_friends_chain(self, user_nickname1, user_nickname2):
        """Return a list of user ids which is a chain between user_nickname1 and user_nickname2."""
        user_id1 = self.__api.get_user_id(user_nickname1)
        user_id2 = self.__api.get_user_id(user_nickname2)
        chain_searcher = ChainSearcherFactory(get_friends_func=self.__get_friends_ids).create_searcher()
        friends_ids_chain = chain_searcher.get_chain(user_id1, user_id2)
        if not friends_ids_chain:
            return None
        friends_chain = [self.__get_user_name(friend_id) for friend_id in friends_ids_chain]
        return friends_chain
