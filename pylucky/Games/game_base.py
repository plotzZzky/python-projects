import art


class GameBase:
    # Base
    checkout = None

    # Sobre o jogo (Precisa alterar!!!)
    game_name: str = "GameBase"
    game_desc: str = "Adivinhe o numero e ganhe uma recompensa"
    game_how: str = "Adivinhe o numero e ganhe uma recompensa"
    game_cost: int = 1
    mult_prize: int = 2 # Fator de multiplicaçao do premio
    max_shift: int = 3

    # Mensagems do jogo (Nao alterar!!!)
    game_about_msg : str = (
        f"-> {game_how}\n"
        f"-> Cada rodada custa {game_cost} fichas"
    )
    no_chips_msg: str = (
        "Voce nao possui fichas o suficiente para jogar!\nAperte qualquer botao para voltar para o menu principal"
    )
    new_game_msg: str = ""
    won_game_msg: str = "\nYou win!"
    lose_game_msg: str = "\nYou lose the game!\n"

    def __init__(self, checkout):
        self.checkout = checkout

    def wellcome(self):
        # tela de boas vindas
        art.tprint(f"{' ' * 4} {self.game_name}", "tarty2")
        print(self.game_desc)

        print(f"{'__' * 18} Regras {'__' * 17}")
        print(self.game_about_msg)

        print(f"{'__' * 18} Jogo {'__' * 18}")

        self.check_minimal_chips_amount()

    def check_minimal_chips_amount(self):
        # Verifica se o usuario possui o minimo de fichas para jogar
        if self.checkout.chips_amount > self.game_cost:
            # Se possuir inicia o menu para jogar
            self.start_game_menu()

        else:
            # Se nao, exibe a mensagem e volta ao menu iniciar
            input(self.no_chips_msg)

    def start_game_menu(self):
        try:
            msg = f"Deseja gastar {self.game_cost} das suas {self.checkout.chips_amount} fichas para jogar?(Y/N)\n"
            option: str = str(input(msg))
            self.check_start_menu_option(option)

        except KeyboardInterrupt:
            print("Bye...\n")
            exit()

        except (ValueError, TypeError):
            pass

    def check_start_menu_option(self, option: str):
        # Se o usuario selecionar y inicia o jogo
        if option == "y":
            self.debit_chips()
        # Se nao, volta ao menu inicial

    def debit_chips(self):
        # Cobra a taxa para jogar
        self.checkout.chips_amount -= self.game_cost
        self.setup_the_game()

    def setup_the_game(self):
        # Cria o setup do jogo
        self.running_the_game()

    def running_the_game(self):
        # Roda o loop do game
        game_shifts = list(range(self.max_shift, 0, -1))

        for value in game_shifts:
            print(f"\nRodada {value} de {self.max_shift}")
            if self.play_the_game_in_loop():
                self.user_won_the_game(value)
                pass

        self.user_lose_the_game()

    def play_the_game_in_loop(self):
        # Roda o jogo nas classes herdeiras
        pass

    def user_won_the_game(self, value: int):
        prize: int = value * self.mult_prize # Calcula o premio

        self.return_prize(prize)
        self.show_won_game_msg(prize)

        self.check_minimal_chips_amount()

    def return_prize(self, prize: int):
        # Acrescenta o premio para o usuario
        self.checkout.chips_amount += prize

    def show_won_game_msg(self, prize: int):
        print(self.won_game_msg)
        print(f"recompensa {prize} fichas\n")

    def user_lose_the_game(self):
        print(self.lose_game_msg)
        self.check_minimal_chips_amount()
