from src.ControllerDir.Controller import Controller
from src.ControllerDir.TelegramController import TelegramController
import click


@click.command()
@click.argument('mode', type=str, default='console')
def main(mode: str):
    controller = None
    if mode == 'console':
        controller = Controller()
    elif mode == 'telegram':
        controller = TelegramController()

    controller.run()


if __name__ == '__main__':
    main()

