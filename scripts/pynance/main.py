# Esse script importa e inicia as classes que estão nos demais arquivos
import sys

from PyNance.data import GetData
from PyNance.graph import GraphClass
import art


class PynanceMenu:
    data = GetData()  # classe para preencher as informações dos graficos
    pies = GraphClass(data)

    def welcome(self):
        art.tprint(f'{" " * 5} PyNance', "tarty1")
        print(f"{'=' * 80}")
        print("Script python para ajudar a gerenciar sua vida fineceira")
        print("Todos os valores devem ser preenchidos com valores inteiros ignorando os centavos\n")
        self.menu()

    def menu(self):
        print(
            "Selecione uma opção:\n"
            "1- Preencher com valores genericos para teste.\n"
            "2- Preencher manualmente\n"
            "3- Sair"
        )
        try:
            option: str = input().lower()
            self.check_menu_option(option)
        except KeyboardInterrupt:
            print("Saindo...")

    def check_menu_option(self, option: str = None):
        if option == "1":
            self.data.test()
            self.pies.create_graph()
        elif option == "2":
            self.data.get_income()
            self.pies.create_graph()
        else:
            self.exit()

    @staticmethod
    def exit():
        print("Saindo...")
        if __name__ == '__main__':
            sys.exit()


pynance = PynanceMenu()

if __name__ == "__main__":
    pynance.welcome()
