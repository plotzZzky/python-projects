from BoilerPlate.boilerplate import CliBoilerplate
from PyLucky.Games.guess_number import GuessNumber
from PyLucky.Games.checkout import Checkout


class PyLucky(CliBoilerplate):
    CLI_DESC: str = "Cassino simples feito em python\n"
    CLI_NAME_SPACE: int = 18
    
    checkout = Checkout()
    guess_number = GuessNumber(checkout)

    def __init__(self):
        super().__init__()

        self.menu_options: list = [
            {"name": "Checkout", "func": self.checkout.start_cli_app},
            {"name": "Sair do cassino", "func": self.exit_cli},
        ]

        self.menu_options_with_chips: list = [  # Lista com os jogos que so aparece se o usuario tiver saldo
            {"name": "Checkout", "func": self.checkout.start_cli_app},
            {"name": "Guess the number", "func": self.guess_number.wellcome},
            {"name": "Sair do cassino", "func": self.exit_cli},
        ]

    def check_chips_amount_on_start(self):
        # So exibe os jogos se ja tiver comprado as fichas
        if self.checkout.chips_amount > 0:
            self.menu_options = self.menu_options_with_chips

        self.checkout.show_chips_amount()

    # --- Funçoes herdadas do boilerplate modificadas por necessidade do projeto ---
    def main_loop(self):
        # removido a funçao que adicona o exit_menu
         self.start_cli_app()

    def start_menu(self):
        """ Exibe a lista de funções do cliapp para o usuario selecionar """
        self.check_chips_amount_on_start() # Verifica se possui saldo de fichas

        self.generic_menu_msg("Menu")

        for index, option in enumerate(self.menu_options, 1):
            # Exibe o nome de forma customizada para esse projeto
            name: str = option['name']
            print(f"{index}- {name}")

        self.receive_start_menu_option()

    def check_start_menu_option(self, option: int):
        """
            Verifica a opção selecionada pelo usuario e chama ela.
            Se for a exit executa ela, se não, executa a função generica como argumento
        """
        try:
            # se a opição for
            if option == len(self.menu_options) - 1:
                self.menu_options[option]["func"]() # Necessario para usar dict no menu_options

            else:
                self.generic_function(
                    lambda: self.menu_options[option]["func"]() # Necessario para usar dict no menu_options
                )

        except (ValueError, IndexError):
            self.restart_cli()


pylucky = PyLucky()

if __name__ == "__main__":
    pylucky.main_loop()
