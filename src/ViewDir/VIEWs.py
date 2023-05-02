import abc
import telebot
from src.ConfigDir.Config import Config


class ViewFactory:
    """This class creates ViewDir-objects."""

    def create_view(self, view_type):
        """Return a ViewDir-object for given view type."""

        if view_type == 'console':
            return ConsoleView()
        elif view_type == 'telegram_bot':
            return TelegramView()
        else:
            raise ValueError(f'Unsupported view type: {view_type}')


class View(metaclass=abc.ABCMeta):
    """An interface for ViewDir."""

    @abc.abstractmethod
    def hello(self, **kwargs):
        """Greets the user and explains the rules."""
        pass

    @abc.abstractmethod
    def ask_command_line(self, **kwargs):
        """Reads command from user's interface."""
        pass

    @abc.abstractmethod
    def return_common_friends(self, common_friends, **kwargs):
        """Takes list of common friens and return it in user's interface."""
        pass

    @abc.abstractmethod
    def return_friends_chain(self, friends_chain, **kwargs):
        """Takes list of friens in chain and return it in user's interface."""
        pass

    @abc.abstractmethod
    def raise_error(self, data, **kwargs):
        """Takes error message and return it in user's interface."""
        pass


class ConsoleView(View):
    """This object can work with console."""

    def __init__(self):
        self.__config = Config()

    def hello(self):
        print("Привет, друг!", '\n')
        print("Сейчас сервис поддерживает следующие команды: ")
        for platform in self.__config.get_platforms():
            for cmd in self.__config.get_commands():
                print('  -> ', platform, cmd, end='')
                print(', вызов осуществляется так:', platform, self.__config.get_commands()[cmd])
        print()
        print("Подсказка: никнейм указывается без '@' ")
        print()

    def ask_command_line(self):
        while True:
            cmd_line = list(input('Введи нужную тебе команду по образцу: ').split())
            if len(cmd_line) >= 3:
                break
            print("Не соответсвует образцу :(")

        return cmd_line[0], cmd_line[1], cmd_line[2:]

    def return_common_friends(self, common_friends, **kwargs):
        print('Запрос выполнен!', end=' ')
        if len(common_friends) > 0:
            print('Общие друзья:', end=' ')
            print(*common_friends, sep=', ')
        else:
            print('Общих друзей нет :(')

    def return_friends_chain(self, friends_chain, **kwargs):
        print('Запрос выполнен!', end=' ')
        if friends_chain:
            print('Одна из кратчайших цепочек:', end=' ')
            print(*friends_chain, sep=' -> ')
        else:
            print('Цепочки нет :(')

    def raise_error(self, error_message, **kwargs):
        print('Ошибка.', end=' ')
        print(error_message)


class TelegramView(View):
    """This object can work with Telegram."""

    def __init__(self):
        self.__config = Config()

    def __create_main_keyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for platform in self.__config.get_platforms():
            for cmd in self.__config.get_commands():
                button = telebot.types.KeyboardButton(text=f'{platform} {cmd}')
                keyboard.add(button)

        return keyboard

    def hello(self, **kwargs):
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']
        keyboard = self.__create_main_keyboard()

        text = "Привет! Я бот для работы с графом друзей в соцсетях.\nВыбери команду в меню."
        bot.send_message(chat_id, text, reply_markup=keyboard)

    def ask_command_line(self):
        pass

    def describe_command(self, cmd, bot, chat_id):
        if cmd == 'get_common_friends':
            bot.send_message(chat_id, "Введите никнэймы пользователей ВК, чтобы найти их общих друзей. \nВажно: "
                                      "указывайте без '@'")
        elif cmd == 'get_friends_chain':
            bot.send_message(chat_id, "Введите никнэймы двух пользователей ВК, чтобы построить цепочку друзей. "
                                      "\nВажно: указывайте без '@'")

    def return_common_friends(self, common_friends, **kwargs):
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']
        bot.send_message(chat_id, "Запрос выполнен! ")
        if len(common_friends) > 0:
            bot.send_message(chat_id, 'Общие друзья: ' + ', '.join(common_friends))
        else:
            bot.send_message(chat_id, "Общих друзей нет :(")

    def return_friends_chain(self, friends_chain, **kwargs):
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']
        bot.send_message(chat_id, "Запрос выполнен! ")
        if isinstance(friends_chain, list) and len(friends_chain) > 0:
            bot.send_message(chat_id, 'Одна из кратчайших цепочек: ' + ' -> '.join(friends_chain))
        else:
            bot.send_message(chat_id, "Цепочки нет :(")

    def raise_error(self, error_message, **kwargs):
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']
        bot.send_message(chat_id, f'Ошибка! {error_message}')