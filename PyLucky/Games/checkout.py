import random

from BoilerPlate.boilerplate import CliBoilerplate


class Checkout(CliBoilerplate):
    chips_amount: int = 0
    CLI_DESC = "Compre fichas ou receba seu premio"
    CLI_NAME_SPACE: int = 16

    # Mensagems engraçadas do cassino
    go_out_msgs: list[str] = [
        "\nSaia da minha frente!",
        "\nPalhaço!",
        "\nVoce nao tem nada melhor para fazer?",
    ]

    def __init__(self):
        super().__init__()
        self.menu_options: list = [
            self.buy_chips,
            self.receive_prize,
            self.exit_cli,
        ]

        self.prize_msgs: list[str] = [
            "\nParabens!\nVoce recebeu ${amount}",
            "\nReceba seus ${amount} e saia logo daqui!",
            "\nSem dinheiro, volte outro dia!",
            "\nNunca te pagaremos otário!",
            "\nAcha mesmo que vamos te pagar hahaha",
        ]

    def buy_chips(self):
        try:
            self.welcome_msg()
            print(f"{'__' * 18} Menu {'__' * 18}")
            option: int = int(input("Gostaria de comprar quantas fichas?\n"))

            self.check_chips_amount(option)

        except KeyboardInterrupt:
            self.select_go_out_msg()

        except (ValueError, TypeError):
            self.select_go_out_msg()

    def check_chips_amount(self, amount: int):
        if amount > 0:
            self.chips_amount += amount

        else:
            self.select_go_out_msg()

    def receive_prize(self):
        # Retorna a mensagem quando solicita o seu dinheiro
        self.select_prize_msg()
        self.reset_the_chips()

    def select_prize_msg(self):
        msg: str = random.choice(self.prize_msgs)
        print(msg.format(amount=self.chips_amount)) # Garante que o valor do chips_amount esteja atualizado

    def select_go_out_msg(self):
        print(random.choice(self.go_out_msgs))

    def reset_the_chips(self):
        self.chips_amount = 0

    def show_chips_amount(self):
        """ Mostra a mensagem indicando quantas fichas o usuario tem """
        print(self.create_chips_amount_msg())

    def create_chips_amount_msg(self) -> str:
        # Cria a mensagem com a quantidade de fichas
        msg: str = f"Voce possui {self.chips_amount} fichas"

        if self.chips_amount < 1: # Se tiver menos de 1, pede para comprar fichas
            msg: str = msg + ", compre fichas no checkout!"

        return msg

    # Funcoes herdadas do BoilerPlate modificadas por necessidade do projeto
    def start_menu(self):
        """ Exibe a lista de funções do cliapp para o usuario selecionar """
        print(self.create_chips_amount_msg())

        self.generic_menu_msg("Menu")

        for index, option in enumerate(self.menu_options, 1):
            # Exibe o nome de forma customizada para esse projeto
            name: str = option.__name__.capitalize().replace('_', ' ').strip('cli')
            print(f"{index}- {name}")

        self.receive_start_menu_option()

    def exit_cli(self):
        # Sai do checkout, mas não do cassino
        pass

