from pykeepass import PyKeePass, create_database
from pykeepass.exceptions import CredentialsError
import string
import random
import sys
import art


# Aplicativo de terminal para gerenciar senhas usando pykeepass, feito em python
class App:
    db = None
    entry = {}
    password: str = None

    # Variaveis usadas no menu de ações do banco de senhas
    menu_opt = []
    menu_act = []

    def welcome(self):
        # Apresentação inicial do programa
        print(f"{'-' * 104}")
        art.tprint(f'{" " * 30} TerminalPass', "tarty2")
        print(
            f"{' ' * 20} Gerenciador de senha via terminal feito em python com pykeepass {' ' * 20}\n"
        )
        self.menu_home()

    def menu_home(self):
        # Menu para verificar se deseja abrir um banco de senhas ou criar um novo
        print(f"{'-' * 49} Menu {'-' * 49}")
        print(
            f"1- Criar um novo banco de senhas \n2- Abrir um banco de senhas \n3- Fechar o programa\n"
        )
        option: str = input("Selecione uma opção:\n")
        self.check_menu_home_option(option)

    def check_menu_home_option(self, option: str):
        # Verifica a opção digita no menu_home e chama a função adequada
        if option == "1":
            self.create_new_db()
        elif option == "2":
            self.open_db()
        elif option == "3":
            self.close_app()
        else:
            print("\nOpção invalida!\n")
            self.menu_home()

    def create_new_db(self):
        # cria um novo banco de senhas como nome e senhas fornecidas pelo usuario via input
        name: str = input("Digite o nome do seu banco de senhas:\n")
        if name != "":
            self.password: str = input("Digite a senha do seu banco de senhas:\n")
            filename: str = f"{name}.kdbx"
            self.db = create_database(filename=filename, password=self.password)
            print("\n Seu novo banco de dados criado!\n")
            self.menu_home()
        else:
            print("Você precisa passr um title:\n")
            self.create_new_db()

    def open_db(self):
        # Abre o db escolhido pelo usuario
        try:
            name: str = input("\nDigite o nome do banco de senhas:\n")
            if name != "":
                filename: str = f"{name}.kdbx"
                pwd: str = input("\nDigite a senha do seu banco de senhas:\n")
                self.db = PyKeePass(filename, password=pwd)
                self.check_if_db_has_pwd()
            else:
                print("Digite um nome valido!")
                self.open_db()
        except (FileNotFoundError, FileExistsError):
            print("\nArquivo não encontrado!\n")
        except CredentialsError:
            print("\nSenha incorreta!\n")
        self.menu_home()

    def check_if_db_has_pwd(self):
        # Função que verifica se o banco de dados tem senhas salvas, e ajusta as opções do menu
        length: int = len(self.db.entries)
        if length != 0:
            self.menu_opt = [
                "Mostrar todas as entradas",
                "Ver senha de uma entrada",
                "Criar nova entrada",
                "Deletar uma entrada",
                "Fechar o banco de senhas",
            ]
        else:
            self.menu_opt = ["Criar nova entrada", "Fechar o banco de senhas"]
        self.menu_db_actions()

    def menu_db_actions(self):
        # Menu de operações no banco de dados
        print(f"{'-' * 35} Escolha uma operação {'-' * 35}")
        for index, item in enumerate(self.menu_opt, start=1):
            print(f"{index} - {item}")
        option = input("\nDigite uma opção:\n")
        self.check_menu_db_option(option)

    def check_menu_db_option(self, option):
        # verifica a opção do menu selecionada e chama a função correspondente
        length: int = len(self.db.entries)
        if length == 0:
            self.handle_empty_db(option)
        else:
            self.handle_non_empty_db(option)

    def handle_empty_db(self, option):
        # Verifica e chama a função correspondente (usada se o db está vazio)
        options = {
            "1": lambda: self.show_pwd(self.create_new_pwd()),
            "2": self.close_db,
        }

        selected_option = options.get(option)
        if selected_option:
            selected_option()
        else:
            print("Opção incorreta!")

        self.menu_db_actions()

    def handle_non_empty_db(self, option):
        # Verifica e chama a função correspondente (usada se o db não está vazio)
        options = {
            "1": self.show_all_entries,
            "2": lambda: self.show_pwd(self.select_entry()),
            "3": lambda: self.show_pwd(self.create_new_pwd()),
            "4": lambda: self.delete_pwd(self.select_entry()),
            "5": self.close_db,
        }

        selected_option = options.get(option)
        if selected_option:
            selected_option()
        else:
            print("Opção incorreta!")
        self.menu_db_actions()

    def select_entry(self):
        # Mostra todas as entradas (através da função show_all_entries) e permite selecionar um ataraves do input
        self.show_all_entries()
        try:
            number: int = int(input("Selecione uma entrada:\n"))
            if number == 0:
                print("Opção não existe!!")
                self.menu_db_actions()
            else:
                entry = self.db.entries[number - 1]
                return entry
        except (ValueError, IndexError):
            print("Opção não existe!!")
            self.menu_db_actions()

    def show_all_entries(self):
        # Mostra todas as entradas no banco de senhas
        n: int = 1
        print(f"{'-' * 35} Todas as entradas {'-' * 35}")
        for entrie in self.db.entries:
            print(f"{n}- {entrie.title}")
            n += 1
        print()

    def show_pwd(self, entry=None):
        # Mostra todas as inforamções de uma entrada, incluindo a senha
        if entry is None:
            self.get_pwd()
        else:
            self.entry = entry
        title: str = self.entry.title
        username: str = self.entry.username
        pwd: str = self.entry.password
        print(f"\ntitle = {title} - username = {username} - password = {pwd}\n")
        self.check_if_db_has_pwd()

    def get_pwd(self):
        # Obtem uma entrada do banco de senhas
        title: str = input(f"Digite uma opção:\n")
        self.entry = self.db.find_entries(title=title, first=True)

    def create_new_pwd(self):
        # cria uma nova senha no banco de senhas aberto
        title: str = input("Digite um nome para sua entrada:\n")
        username: str = input("\nDigite o username:\n")
        if title != "":
            pwd: str = self.check_pwd()
            group = self.db.find_groups(name="Root", first=True)
            new_entry = self.db.add_entry(group, title, username, pwd)
            self.db.save()
            self.show_pwd(new_entry)
        else:
            print("Você precisa passr um title:\n")
            self.create_random_pwd()

    def check_pwd(self):
        # verifica se o usario quer uma senha randomica ou criar a sua
        pwd: str = input("\nDigite a sua senha ou S para criar uma senha randomica:\n")
        if pwd.lower() == "s":
            password = self.create_random_pwd()
            return password
        else:
            return pwd

    @staticmethod
    def create_random_pwd():
        # Gera uma nova senha randomica
        characters = string.ascii_letters + string.digits
        amount: int = int(input("Digite o numero de digitos da sua nova senha:\n"))
        result = "".join(random.choice(characters) for _ in range(int(amount)))
        return result

    def delete_pwd(self, pwd):
        # Deleta uma entrada no banco de senhas
        title: str = pwd.title
        self.db.delete_entry(pwd)
        print(f"Entrada {title} deletada!")
        self.menu_db_actions()

    def close_db(self):
        # Fecha o banco de senhas
        self.menu_home()

    @staticmethod
    def close_app():
        # Fecha o programa
        sys.exit()


tpass = App()

if __name__ == "__main__":
    tpass.welcome()
