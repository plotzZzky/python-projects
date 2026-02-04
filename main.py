from CPFScript.main import cpf
from DjangoForge.main import forge
from FastapiForge.main import fastapi_forge
from FindCompanyInfo.main import find
from GitGet.main import gitget
from MonthlyReport.main import monthly_report
from ProjectCreator.main import menu as projectcreator
from PyDrawn.main import pydrawn
from PyEncrypt.main import pyencrypt
from PyLucky.main import pylucky
from PyNance.main import pynance
from PyRecord.main import pyrecord
from PySystem.main import pysystem
from SimpleCheckout.main import checkout
from SimpleScraper.main import simple_scrapper
from TeamReport.main import create_report
from Tpass.main import tpass
from YouSave.main import yousave
import art


class Menu:
    # Menu para executar um dos scripts desse projeto
    def __init__(self):
        self.apps: list = [
            "CpfScript",
            "DjangoForge",
            "FastapiForge",
            "FindCompanyInfo",
            "GitGet",
            "MonthlyReport",
            "ProjectCreator",
            "PyDrawn",
            "PyEncrypt",
            "PyLucky",
            "PyNance",
            "PyRecord",
            "PySystem",
            "SimpleCheckout",
            "SimpleScrapper",
            "TeamReport",
            "Tpass",
            "YouSave",
        ]

        self.funcs: list = [
            cpf.welcome_msg,
            forge.welcome_msg,
            fastapi_forge.welcome_msg,
            find.welcome_msg,
            gitget.welcome_msg,
            monthly_report.welcome,
            projectcreator.welcome_msg,
            pydrawn.welcome_msg,
            pyencrypt.welcome_msg,
            pylucky.welcome_msg,
            pynance.welcome_msg,
            pyrecord.welcome_msg,
            pysystem.welcome_msg,
            checkout.welcome_msg,
            simple_scrapper.welcome_msg,
            create_report,
            tpass.welcome,
            yousave.welcome_msg,
        ]

        self.print_space: str = f"{'-' * 36}"

    def welcome(self):
        # Tela de apresentação
        art.tprint(f'{" " * 13} Python', "tarty1")
        art.tprint(f'{" " * 13} Scripts', "tarty1")
        self.menu()

    def menu(self):
        # Menu com a lista de apps disponivel
        print(f"{self.print_space} Menu {self.print_space}\n")
        print("Selecione uma opção para executar o script:")

        for index, item in enumerate(self.apps, 1):
            print(f"{index}- {item}")
        self.get_option()

    def get_option(self):
        # Recebe a escolha do usuario e verifica se esta entre as opções disponiveis
        option: str = input("\nEscolha uma opção:\n")
        try:
            number: int = int(option)
            if 1 <= number <= len(self.apps):
                self.open_app(number)
            else:
                print("Opção incorreta!")
                self.welcome()
        except ValueError:
            print("Opção incorreta!\n")
            self.welcome()

    def open_app(self, option):
        # Executa o script selecionado pelo usuario
        try:
            self.funcs[option - 1]()
        except (KeyError, ValueError):
            pass
        self.welcome()


menu = Menu()
if __name__ == '__main__':
    menu.welcome()
