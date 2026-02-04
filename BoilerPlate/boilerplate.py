import subprocess
from time import sleep
import os


class CliBoilerplate:
    """
        Description:
            CliBoilerplate para simplificar a criação de cliapps com menu.

        Use:
            Crie uma classe filha dessa e adicione as funções desejadas como no exemplo em base.py
    """
    CLI_DESC: str = "Um BoilerPlate simples de cliapp feito em python\n" # descrição do cliapp
    CLI_NAME_SPACE: int = 8 # Espaso antes do nome na mensagem de boas vindas

    SLEEP_TIME: float = 2

    def __init__(self):
        # O init é necessario para usar o self
        self.CLI_NAME: str = self.__class__.__name__

        self.menu_options: list = [ # Lista com o nome das funções do cliapp
            self.example_function,
        ]

    def main_loop(self):
        """ Inicia o loop do cliapp (necessario para evitar adicionar o exit a cada loop) """
        # Adiciona a função exit para não precisar fazer isso na classe herdeira
        self.menu_options.append(self.exit_cli)
        self.start_cli_app()

    def start_cli_app(self):
        """ Inicia o cliapp """
        self.welcome_msg()
        self.start_menu()

    def welcome_msg(self):
        """
            Tela de apresentação (nome e descrição) do cliapp
            Se tiver o art instalado exibe o nome usando o, se não, usa o inbuilt print
        """
        self.clean_terminal()

        try:
            import art # colocado aqui para evitar o erro ao iniciar o cliapp
            art.tprint(f"{' ' * self.CLI_NAME_SPACE} {self.CLI_NAME}", "tarty1")

        except ModuleNotFoundError:
            width: int = self.receive_terminal_width(self.CLI_NAME)
            print(f"{' ' * width} {self.CLI_NAME}")

        # Calcula a largura e exibe a descriçao do cliapp
        width: int = self.receive_terminal_width(self.CLI_DESC)
        print(f"{' ' * width} {self.CLI_DESC}")

    def start_menu(self):
        """ Exibe a lista de funções do cliapp para o usuario selecionar """
        self.generic_menu_msg("Start Menu")

        for index, option in enumerate(self.menu_options, 1):
            name: str = option.__name__.replace("_", " ").capitalize().strip("cli") # Nome formatado da função
            print(f"{index}- {name}")

        self.receive_start_menu_option()

    def receive_start_menu_option(self):
        """ Recebe a opção selecionado pelo usuario no start_menu """
        try:
            option: int = int(input("\nSelecione uma opção:\n")) - 1
            self.check_start_menu_option(option)

        except ValueError:
            # reinicia o cliapp se o valor for invalido
            self.restart_cli()

        except KeyboardInterrupt:
            # Apresenta a mensagem de saida se o usaurio sair do cliapp (ctrl + c)
            self.exit_cli()

    def check_start_menu_option(self, option: int):
        """
            Verifica a opção selecionada pelo usuario e chama ela.
            Se for a exit executa ela, se não, executa a função generica como argumento
        """
        try:
            # se a opição for
            if option == len(self.menu_options) - 1:
                self.menu_options[option]()

            else:
                self.generic_function(
                    lambda: self.menu_options[option]()
                )

        except (ValueError, IndexError):
            self.restart_cli()

    def generic_function(self, commands):
        """
            Função generica para simplicar o codigo, eliminado a necessidade de adicionar as funções clean_terminal
            e start_menu() para cada nova função.

            Args:
                commands : Lista de comandos passados via *args
        """
        self.welcome_msg()
        commands()
        input("\nEnter para continuar...")
        self.start_cli_app()

    def generic_menu_msg(self, msg: str):
        """ Mensagem basica de apresentaçao para os menus """
        width: int = self.receive_terminal_width(msg)
        print(f"\n {'_' * width} {msg} {'_' * width} ")

    @staticmethod
    def example_function():
        """ Função para teste"""
        print("\nExample function")

    def exit_cli(self):
        """ 
            Fecha o cli
            - Por padrao espera 2 segundos para o usuario ler o retorno e fecha
            - Se pressionar ctr + c fecha na hora
        """
        try:
            print("\nBye...")
            sleep(self.SLEEP_TIME)
            
        except KeyboardInterrupt:
            pass
            
        self.clean_terminal()
        exit()

    def restart_cli(self):
        """ reinicia o cliapp quando o usuario digitar uma opção invalida """
        self.welcome_msg()
        print('Opção invalida!!!')
        self.start_menu()

    @staticmethod
    def clean_terminal():
        subprocess.call("clear")

    @staticmethod
    def receive_terminal_width(msg: str) -> int:
        """
            - Calcula a largura do terminal
            - Calcula a largura do terminal menos a mensagem formatada
            - Retorna a largura dividida por 2
        """
        size = os.get_terminal_size()
        terminal_width = size.columns
        msg_len: int = len(msg) + 4 # space + symbols + space + msg + space + symbols + space
        width = int((terminal_width - msg_len) / 2)
        return width


cliapp = CliBoilerplate()

if __name__ == "__main__":
    cliapp.main_loop()
