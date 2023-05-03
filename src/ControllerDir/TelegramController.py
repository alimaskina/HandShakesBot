from src.SocialNetworkDir.SocialNetwork import SocialNetwork
from src.ConfigDir.Config import Config
from src.ViewDir.VIEWs import ViewFactory
import telebot


class TelegramController:
    def __init__(self):
        self.__config = Config()
        self.__social_network = SocialNetwork()
        self.__view = ViewFactory().create_view('telegram_bot')
        self.bot = telebot.TeleBot(self.__config.get_tg_token())

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

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def hello(message):
            self.__view.hello(bot=self.bot, chat_id=message.chat.id)

        @self.bot.message_handler(content_types=['text'])
        def handle_callback_query(message):
            splited = message.text.split()
            if len(splited) != 2:
                error_message = "Такой команды нет :( \nВыберите команду в меню."
                self.__view.raise_error(error_message, bot=self.bot, chat_id=message.chat.id)
                return
            pltf, cmd = message.text.split()
            self.__set_platform(pltf)
            self.__view.describe_command(cmd, self.bot, message.chat.id)
            if cmd == 'get_common_friends':
                self.bot.register_next_step_handler(message, self._handle_find_common_friends)
            elif cmd == 'get_friends_chain':
                self.bot.register_next_step_handler(message, self._handle_build_friends_chain)
            else:
                error_message = "Такой команды нет :( \nВыберите команду в меню."
                self.__view.raise_error(error_message, bot=self.bot, chat_id=message.chat.id)

        self.bot.polling()

    def _handle_find_common_friends(self, message):
        nicknames = message.text.split()
        check_result = self.__check_command('get_common_friends', nicknames)
        if check_result:
            self.bot.send_message(message.chat.id, check_result)
            return
        common_friends = self.__social_network.get_common_friends(nicknames)
        self.__view.return_common_friends(common_friends, bot=self.bot, chat_id=message.chat.id)

    def _handle_build_friends_chain(self, message):
        nicknames = message.text.split()
        check_result = self.__check_command('get_friends_chain', nicknames)
        if check_result:
            self.bot.send_message(message.chat.id, check_result)
            return
        friends_chain = self.__social_network.get_friends_chain(nicknames[0], nicknames[1])
        self.__view.return_friends_chain(friends_chain, bot=self.bot, chat_id=message.chat.id)