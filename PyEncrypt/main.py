import cryptography.fernet
from cryptography.fernet import Fernet
from pathlib import Path
import tarfile
import sys
import art
import os


class PyEncrypt:
    """
        Script para criptograr e descriptografar arquivos e pastas
        - Permite criar e salvar uma chave de criptografia em uma (~./pygraphy/)
    """
    home: Path = Path().home()
    folder: str = f"{home}/.pygraphy/"
    key = None

    def welcome(self):
        """ Tela de boas vindas """
        art.tprint(f'{" " * 9} PyGraphy', "tarty1")
        self.start_menu()

    def start_menu(self):
        """ Menu inicial """
        try:
            print(f"{'_' * 40} Menu {'_' * 40}")
            print(
                "1- Criar nova chave\n"
                "2- Criptografar arquivo\n"
                "3- Descritografar arquivo\n"
                "4- Sair"
            )
            option: str = input("\nDigite uma opção:\n")

            self.check_option(option)
        except KeyboardInterrupt:
            print("Saindo...")

    def check_option(self, option: str):
        """ Abre a opção selecionada no menu """
        try:
            option: int = int(option) - 1
            options: list = [
                self.create_new_key,
                self.check_if_is_folder,
                self.decrypt_file,
                self.exit,
            ]
            options[option]()
        except (IndexError, ValueError, TypeError):
            print("Opção invalida!\n")
            self.start_menu()

    def create_new_key(self):
        """ Cria uma nova chave de criptografia """
        key = Fernet.generate_key()
        keyname: str = input("Digite o nome da chave:\n")
        path = self.check_if_app_folder_exist()
        key_path = f"{path}/{keyname}.key"

        with open(key_path, 'wb') as new_key:
            new_key.write(key)

        print(f"Nova chave {keyname}.key criada!")
        self.start_menu()

    def crypt_file(self, filename: str):
        """ Criptografa um arquivo """
        try:
            with open(filename, "rb") as file:
                file_data: bytes = file.read()

            key = self.open_key()
            encrypted_data: bytes = key.encrypt(file_data)

            new_filename: str = f"{filename}.cript"
            self.save_data_on_file(new_filename, encrypted_data)
            self.start_menu()

        except (FileExistsError, FileNotFoundError):
            print("Arquivo não encontrado!")
            self.check_if_is_folder()

    def decrypt_file(self):
        """ Decriptografa um arquivo """
        try:
            filename: str = input("Digite o caminho do arquivo criptografado:\n")

            with open(filename, 'rb') as file:
                file_data = file.read()

            key = self.open_key()
            content = key.decrypt(file_data)

            new_filename: str = filename.split('.cript')[0]
            self.save_data_on_file(new_filename, content)
            self.start_menu()

        except (FileExistsError, FileNotFoundError):
            print("Arquivo não encontrado!")
            self.decrypt_file()
        except cryptography.fernet.InvalidToken:
            print("Chave invalida!")
            self.decrypt_file()

    def check_if_is_folder(self):
        """ Verifica se o alvo é uma pasta ou arquivo """
        file: str = input("Digite o caminho para o arquivo:\n")

        if Path(file).is_dir():
            file: str = self.create_tar_folder(file)
        self.crypt_file(file)

    def check_if_app_folder_exist(self) -> Path:
        """ Verifica se a pasta do script existe """
        path = Path(self.folder)

        if not path.exists():
            Path.mkdir(path)
        return path

    def open_key(self):
        """ Abre a chave do usuario """
        keyname: str = input('Digite o nome da key:\n')
        if '.key' not in keyname:  # Verifica se o usario passou a apenas o nome sem a extensão
            keyname: str = keyname + '.key'

        path: str = f"{self.folder}{keyname}"
        try:
            file = open(path, 'rb').read()
            key = Fernet(file)
            return key
        except (FileExistsError, FileNotFoundError):
            print(f"Key não encontrada\n")
            self.open_key()

    @staticmethod
    def create_tar_folder(filename) -> str:
        """ Cria um tar.gz file da pasta para criptografar """
        tarfile_name: str = f"{filename}.tar.gz"

        with tarfile.open(tarfile_name, 'w:gz') as file:
            file.add(filename, arcname=os.path.basename(filename))

        return tarfile_name

    @staticmethod
    def save_data_on_file(filename: str, data: bytes):
        with open(filename, "wb") as file:
            file.write(data)

    @staticmethod
    def exit():
        print("Saindo...")
        if __name__ == '__main__':
            sys.exit()


pyencrypt = PyEncrypt()

if __name__ == '__main__':
    pyencrypt.welcome()
