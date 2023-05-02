import vk_api
import abc
from src.ConfigDir.Config import Config


class APIFactory:
    """This class creates SocialNetworkApi-objects."""
    def __init__(self):
        self.__config = Config()

    def create_api(self, social_network_type):
        """Return an SocialNetworkApi-object for given social network type."""
        if social_network_type == 'vk':
            return VkApi(token=self.__config.get_vk_token(), version=self.__config.get_vk_version())
        else:
            raise ValueError('Unsupported API type')


class SocialNetworkApi(metaclass=abc.ABCMeta):
    """An interface for APIs."""
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_friends_ids(self, user_id):
        """Return a list of friends of user with user_id."""
        pass

    @abc.abstractmethod
    def get_user_name(self, user_id):
        """Return a name of user with user_id."""
        pass

    @abc.abstractmethod
    def is_existing(self, user_nickname):
        """Return true if user with user_nickname exists."""
        pass

    @abc.abstractmethod
    def get_user_id(self, user_nickname):
        """Return id of user with user_nickname."""
        pass


class VkApi(SocialNetworkApi):
    """This is an object which can work with API of VK."""
    def __init__(self, token, version):
        super().__init__()
        self.version = version
        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()

    def is_existing(self, user_nickname):
        user_info = self.vk.users.get(user_ids=user_nickname, v=self.version)
        return len(user_info) != 0

    def get_user_id(self, user_nickname):
        user_info = self.vk.users.get(user_ids=user_nickname, v=self.version)
        return int(user_info[0]['id'])

    def get_user_name(self, user_id):
        user_info = self.vk.users.get(user_ids=user_id, v=self.version)
        return user_info[0]['first_name'] + ' ' + user_info[0]['last_name']

    def get_friends_ids(self, user_nickname):
        user_id = self.get_user_id(user_nickname=user_nickname)
        try:  # если профиль не закрыт
            friends_ids = self.vk.friends.get(user_id=user_id, v=self.version)['items']
        except Exception:
            friends_ids = []
        return friends_ids
