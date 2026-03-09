from PyLucky.Games.game_base import GameBase
import random


class GuessNumber(GameBase):
    game_name = "Guess the number"
    game_desc: str = "Adivinhe um numero de 0-9 e receba um prêmio!\n"
    game_how: str = (
        "Voce possui duas chances, se acertar na primeira recebe três fichas "
        "e na segunda recebe 2 fichas"
    )

    random_number: int = 0
    user_number: int = 0

    # ----- Funções especificas desse jogo -----
    def trying_to_guess_the_number(self) -> bool:
        self.get_user_number()
        return self.compare_the_numbers()

    def receive_random_number(self):
        self.random_number: int = random.randint(0, 9)

    def get_user_number(self):
        self.user_number: int = int(input("\nEscolha um numero: "))

    def compare_the_numbers(self):
        if self.random_number == self.user_number:
            return True

        else:
            print(f"\n{self.user_number} nao e o numero certo!")
            return False

    # --- funções herdadas da classe pai e modificadas por necessidade do jogo ---
    def setup_the_game(self):
        self.receive_random_number()
        self.running_the_game()

    def play_the_game_in_loop(self):
        return self.trying_to_guess_the_number()