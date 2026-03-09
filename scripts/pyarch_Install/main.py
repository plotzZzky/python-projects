#!/usr/bin/env python
import subprocess


class PyArchInstall:
    """
        Script para automatizar a instalação de pacotes no archlinux
        Esse script precisa ser executado como sudo!!! sudo ./boilerplate.py
    """
    APP_DESC: str = "Script para automatizar a instalação de pacotes no archlinux"

    official_packages: list = [
        "libreoffice-still",
        "code",
        "pycharm-community-edit",
        "telegram-desktop",
        "krita",
        "keepassxc"
        "xfce4-goodies",
        "elementary-wallpapers",
    ]

    aur_packages: list = [
        "brave-bin",
        "xfce4-docklike-plugin-ng-git"
    ]

    def welcome(self):
        print(f"{' ' * 20} {self.__class__.__name__}")  # retorna o nome da classe
        print(self.APP_DESC)
        print("Começando...")

        self.start_install()

    def start_install(self):
        self.install_from_official_repos()
        self.install_from_aur()
        self.exit_installer()

    def install_from_official_repos(self):
        for package in self.official_packages:
            self.install_package(package, "pacman")

    def install_from_aur(self):
        for package in self.aur_packages:
            self.install_package(package, "yay")

    @staticmethod
    def exit_installer():
        input("\nPrecione qualquer tecla para sair...")  # força o terminal a ficar aberto

    @staticmethod
    def install_package(package: str, installer: str):
        try:
            command: list = [installer, "-Sy", package]
            subprocess.run(command,  input="S\n", text=True, check=True)

        except subprocess.CalledProcessError:
            print(f"Não foi possivel instalar o pacote {package}!")


app = PyArchInstall()

if __name__ == '__main__':
    app.welcome()
