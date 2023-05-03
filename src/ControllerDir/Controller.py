from src.SocialNetworkDir.SocialNetwork import SocialNetwork
from src.ConfigDir.Config import Config
from src.ViewDir.VIEWs import ViewFactory


class Controller:
    """Connects ViewDir and SocialNetworkDir (Model)."""
    def __init__(self):
        self.__social_network = SocialNetwork()
        self.__view = ViewFactory().create_view('console')
        self.__config = Config()

    def __set_platform(self, platform):
        """Check and set platform SocialNetworkDir works with."""
        if platform not in self.__config.get_platforms():
            return f"Пока соцсеть {platform} не поддерживается :("

        self.__social_network.set_api(platform)

    def __check_command(self, check_cmd, check_args):
        """Check command and user's nicknames."""
        if check_cmd not in self.__config.get_commands():
            return f"Пока команда {check_cmd} не поддерживается :("
        for user_nickname in check_args:
            user_check = self.__social_network.is_user_existing(user_nickname)
            if user_check:
                return f"Пользователь {user_check} не существует :("

    def __process_commands(self, pltf, cmd, args):
        """Processing user's command."""
        set_platf_res = self.__set_platform(pltf)
        if set_platf_res:
            self.__view.raise_error(set_platf_res)
            return

        check_result = self.__check_command(cmd, args)
        if check_result:
            self.__view.raise_error(check_result)
            return

        match cmd:
            case 'get_common_friends':
                common_friends = self.__social_network.get_common_friends(args)
                self.__view.return_common_friends(common_friends)
            case 'get_friends_chain':
                friends_chain = self.__social_network.get_friends_chain(args[0], args[1])
                self.__view.return_friends_chain(friends_chain)
            case 'get_potential_friends':
                pass
            case 'get_groups_of_friends':
                pass

    def run(self):
        """Main work cycle."""
        self.__view.hello()
        try:
            while True:
                pltf, cmd, args = self.__view.ask_command_line()
                self.__process_commands(pltf, cmd, args)

        except KeyboardInterrupt:
            self.__social_network.cash_data()

