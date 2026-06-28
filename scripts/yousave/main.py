from pytube import YouTube, exceptions
from pathlib import Path
import sys
import art


class YouSave:
    """ Script para salvar videos do youtube"""
    video_name: str = ''
    streams = []
    home: Path = Path.home()
    filename: str = ''

    def welcome(self):
        art.tprint(f'{" " * 11} YouSave', "tarty1")
        print(f'{"_ " * 44}\n')
        self.get_content()

    def get_content(self):
        try:
            url: str = input("Digite o url do video:\n")
            self.streams = YouTube(url).streams
            self.show_options_for_download()

        except exceptions.RegexMatchError:  # url invalida
            print('Url invalida!\n')
            self.get_content()

        except KeyboardInterrupt:
            print("Saindo...")

    def show_options_for_download(self):
        """ Lista todas as opções para download """
        print("\nOpções para download:")

        for index, item in enumerate(self.streams, 1):
            file_type: str = item.type
            file: str = item.mime_type
            res: str = f", resolution={item.resolution}" if item.resolution else ''
            value: str = f"{index}- tipo={file_type}, formato={file}{res}"
            print(value)

        self.select_option_for_download()

    def select_option_for_download(self):
        try:
            option: str = input("\nSelecione a opção:\n").lower()
            folder: str = self.check_folder()
            self.streams[int(option) - 1].download(output_path=folder)  # faz o download do arquivo selecionado
            self.show_result()
        except (IndexError, ValueError):
            print("Opção invalida!\n")
            self.show_options_for_download()

    def check_folder(self) -> str:
        """ Verifica se a pasta existe """
        folder: str = f"{self.home}/yousave"

        if not Path(folder).exists():
            Path(folder).mkdir()

        return folder

    def show_result(self):
        print(f"Video {self.video_name} salva com sucesso!")
        self.exit_menu()

    def exit_menu(self):
        option: str = input("Baixar mais videos?(Y/N)\n").lower()
        if option == 'y':
            self.get_content()
        else:
            sys.exit()


yousave = YouSave()
if __name__ == '__main__':
    yousave.welcome()
