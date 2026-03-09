from ProjectCreator.creators import PythonCreator, JsCreator
import sys


class MenuClass:
    """ Classe do Menu inicial """
    APP_NAME: str = 'Menu'
    APP_DESC: str = "Ferramenta para criar projetos base em python ou javascript"

    project_name: str = ""

    def __init__(self):
        # O init é necessario para usar o self
        self.menu_options = [
            self.create_python_project,
            self.create_js_project,
            lambda: self.check_exit_menu_option('Y'),  # Chama a função para fechar o app
        ]

    def welcome(self):
        print(f"{' ' * 35} {self.APP_NAME}")
        print(self.APP_DESC)
        self.start_menu()

    def start_menu(self):
        print(f"{'--' * 18} Menu {'--' * 18}")
        options = [
            'Criar projeto Python',
            'Criar projeto Js',
            'Sair'
        ]

        for index, option in enumerate(options, 1):
            print(f"{index}- {option}")

        self.check_start_menu_option()

    def check_start_menu_option(self):
        try:
            option: int = int(input("\nSelecione uma opção:\n")) - 1
            self.menu_options[option]()  # chama a função selecionada

        except (ValueError, IndexError):
            print('\nOpção invalida!!!!!\n')
            self.start_menu()
        except KeyboardInterrupt:
            print("\nSaindo...")

    def create_python_project(self):
        creator_py.create_python_project()
        print("Projeto Python criado!")
        self.exit_menu()

    def create_js_project(self):
        creator_js.create_js_project()
        print("Projeto JavaScript criado!")
        self.exit_menu()

    def exit_menu(self):
        try:
            option: str = input("\nSair?(Y/N)\n").upper()
            self.check_exit_menu_option(option)
        except KeyboardInterrupt:
            sys.exit()

    def check_exit_menu_option(self, option: str):
        if option == 'Y':
            if __name__ == '__main__':
                print("Saindo...")
                sys.exit()
        else:
            self.start_menu()


creator_py = PythonCreator()
creator_js = JsCreator()
menu = MenuClass()

if __name__ == '__main__':
    menu.welcome()
