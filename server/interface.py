from pyfiglet import figlet_format
from rich.console import Console
from rich.theme import Theme


class Interface:
    def __init__(self) -> None:
        self.themes = Theme({
            'logo': 'bold green1',
            'sys': 'i bold red1',
            'adm': 'i green1',
            'clt': 'bold bright_white',
        })

        self.console = Console(theme=self.themes, log_path=False)
        self.logo = figlet_format("CRYPTO CHAT", font='larry3d')

    def show_msg(self, message):
        self.console.log(message)

    def show_logo(self):
        self.console.print(self.logo, style='logo')


ui = Interface()
