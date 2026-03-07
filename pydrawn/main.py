import random
import sys


class PyDrawn:
    APP_DESC: str = "--> Cliapp simples de sorteio feito em python <--\n"

    drawn_rounds: int = 0
    drawn_options: list = ['João', 'Ze', 'Maria', 'Ana']

    winners: list = []

    no_repeat: bool = False
    number_only: bool = False

    def __init__(self):
        self.menu_options = [
            {"name": "Sorteio simples da lista", "func": self.simple_drawn},
            {"name": "Sorteio sem repetição da lista", "func": self.no_repeat_drawn},
            {"name": "Sorteio simples de numero", "func": self.simple_only_number},
            {"name": "Sorteio de numero sem repetição", "func": self.no_repeat_only_number},
            {"name": "Sair", "func": self.exit_cli},
        ]

    def welcome_msg(self):
        try:
            import art # type: ignore

            art.tprint("PyDrawn", "small")

        except ImportError:
            print(f"{'-' * 16} Welcome to PyDrawn {'-' * 16}")

        print(self.APP_DESC)
        self.show_menu_options()

    def show_menu_options(self):
        print(f"{'-' * 23} Menu {'-' * 23}")

        for index, item in enumerate(self.menu_options):
            print(f"{index + 1}. {item['name']}")

        self.select_menu_option()

    def select_menu_option(self):
        try:
            option: int = int(input("\nSelecione uma opção: "))
            self.menu_options[option - 1]["func"]()

        except (IndexError, ValueError):
            self.show_menu_options()

        except KeyboardInterrupt:
            self.exit_cli()

    def simple_drawn(self):
        self.receive_drawn_values()
        self.drawn_rounds_func()

    def no_repeat_drawn(self):
        self.no_repeat = True
        self.receive_drawn_values()
        self.drawn_rounds_func()

    def simple_only_number(self):
        self.number_only = True
        self.receive_drawn_values()
        self.drawn_rounds_func()

    def no_repeat_only_number(self):
        self.number_only = True
        self.no_repeat = True
        self.receive_drawn_values()
        self.drawn_rounds_func()

    def receive_drawn_values(self):
        self.drawn_rounds: int = int(input("Digite o numero de sorteados: ")) or 1

        if self.number_only:
            length: int = int(input("Digite a quantidade opções: ")) or 10
            self.drawn_options = list(range(1, length + 1))

    def drawn_rounds_func(self):
        print(f"\n {'.' * 20} Sorteio {'.' * 20} ")

        for index in range(self.drawn_rounds):
            if self.drawn_options:
                print(f"\n - - - - - Round {index+1} - - - - - ")
                self.select_drawn_number()

            else:
                break

        self.show_all_winners()

    def select_drawn_number(self):
        value: int = self.select_random_value()
        self.select_winner(value)

    def select_winner(self, value: int):
        winner = self.drawn_options[value - 1] or None
        self.winners.append(winner)

        if self.no_repeat:
            self.remove_winner(value) # Remove o vencedor da lista

        self.show_winner(value, winner)  # Exibe os resultados

    @staticmethod
    def show_winner(value: int, winner: str):
        print(f"O numero selecionado foi {value}")

        # Try usado para evitar exibir o numero vencedor duas vezes se na lista tiver numeros
        try:
            int(winner)

        except TypeError:
            print("O vencedor foi", winner)

    def show_all_winners(self):
        result: str = ""

        if len(self.winners) > 2:
            *others, penultimate_winner, last_winner = sorted(self.winners)
            result: str = (
                    f"{', '.join(map(str, others)) + '' if others else ''}" +
                    f", {penultimate_winner} e {last_winner}."
            )

        print(f"\nOs vencedores foram {result}")

    def remove_winner(self, index: int):
        """ Se o sorteio não permitir vencedores repetidos tira o da lista """
        if not self.number_only:
            del self.drawn_options[index - 1]

        else:
            for x, option in enumerate(self.drawn_options):
                if option == self.drawn_options[index - 1]:
                    del self.drawn_options[x]

    def select_random_value(self):
        """ Sorteia um pseudo numero aleatorio """
        try:
            value: int = random.randint(1, len(self.drawn_options))
            return value

        except IndexError:
            print("A lista acabou\n")
            self.exit_cli()

    @staticmethod
    def exit_cli():
        print("\nBye!")
        sys.exit()


pydrawn = PyDrawn()
if __name__ == "__main__":
    pydrawn.welcome_msg()
