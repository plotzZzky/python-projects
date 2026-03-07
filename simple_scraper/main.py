from urllib3 import request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from  pathlib import Path
import subprocess
import shutil
import sys


class SimpleScraper:
    """ Ferramenta simples para fazer scraping em paginas da web """
    APP_NAME: str = None
    APP_DESC: str = "Appcli simples para fazer scraping de paginas da web.\n"

    url: str = "google.com"
    method: str = "GET"

    site_name: str = ""
    folder_path: Path = Path()
    folder_src: Path = Path()

    def __init__(self):
        self.APP_NAME: str = self.__class__.__name__ # precisa do self para o nome

        self.options = [
            {"name": "Ver a pagina", "func": self.show_html_page},
            {"name": "Ver o head", "func": self.show_head_html_page},
            {"name": "Ver o body", "func": self.show_body_html_page},
            {"name": "Salvar a pagina em html", "func": self.save_page_in_html},
            {"name": "Salvar o body pagina em txt", "func": self.save_body_page_in_txt},
            {"name": "Apagar a pagina do cahe", "func": self.delete_html_page},
            {"name": "Limpar o cache", "func": self.clear_all_cache},
            {"name": "Passar outra url", "func": self.show_app_name},
            {"name": "Sair", "func": self.exit_cli},
        ]

    def show_app_name(self):
        try:
            import art # colocado aqui para evitar o erro ao iniciar o cliapp
            art.tprint(f"{self.APP_NAME}", font="cybermedium")

        except ModuleNotFoundError:
            print(f"- - - - - - - - - {self.APP_NAME} - - - - - - - - ")

        print(self.APP_DESC)
        self.receive_url_and_method()

    def receive_url_and_method(self):
        # Recebe a url do usuario ou utiliza a padrão para tests
        self.url: str = input("Digite a url: ") or self.url
        self.method: str = input("Digite o metodo http: ") or self.method

        self.create_paths() # Cria os paths da pagina
        self.show_menu()

    def show_menu(self):
        print(f"\n _ _ _ _ _ _ _ _ _ _ _ Menu _ _ _ _ _ _ _ _ _ _ _" )

        for index, option in enumerate(self.options, 1): # Mostra todas as opções, mas com index 1 ao invest de 0
            print(f"{index}- {option['name']}")

        print(f"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")

        self.check_menu_option()

    def check_menu_option(self):
        try:
            option = int(input("\nSeleciona uma opção: "))

            if option > len(self.options): # Se o valor solicitado for maior que o numero de opçãoes reinicia o menu
                raise ValueError

            if option == 8: # Se for a exit, executa sem a função generica
                self.options[option - 1]['func']()

            self.generic_menu_function(self.options[option - 1])

        except (ValueError, TypeError):
            print("\nOpção invalida!\n")
            self.show_menu()

    def generic_menu_function(self, function):
        """
            Função generica de execução deas funções

            Steps:
                - Exibe a mensagem de execução
                - Executa a função
                - Exibe o menu
         """
        subprocess.call("clear")
        print(f"\nExecutando {function['name'].lower()}...")

        function['func']()

        input("\nFeito! "
              "Enter para continuar..."
              )
        self.show_menu()

    def show_html_page(self):
        page = self.parse_page_with_bs4()
        print(page.prettify())

    def show_head_html_page(self):
        page = self.parse_page_with_bs4()
        print(page.head.prettify())

    def show_body_html_page(self):
        page = self.parse_page_with_bs4()
        print(page.body.prettify())

    def save_page_in_html(self):
        page = self.parse_page_with_bs4()

        with open(f"{self.folder_path}/page.html", "w") as f:
            f.write(page.prettify())

    def save_body_page_in_txt(self):
        page = self.parse_page_with_bs4()

        with open(f"{self.folder_path}/{self.url}.txt", "w") as f:
            f.write(page.body.prettify())

    def delete_html_page(self):
        cached_page = Path(f"{self.folder_path}/page.html")

        if cached_page.exists(): # Se a pagina existir remove a toda a pasta do projeto
            shutil.rmtree(self.folder_path)

    @staticmethod
    def clear_all_cache():
        path: Path = Path("pages")
        shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def exit_cli():
        print("\nSaindo...")
        sys.exit()

    # Utils
    def create_paths(self):
        self.site_name: str = self.return_site_name()
        self.folder_path: Path = Path(f"pages/{self.site_name}/")
        self.folder_src: Path = Path(f"{self.folder_path}/src")

    def return_site_name(self) -> str:
        """ Retorna apenas o nome do site sem o resta da url """
        url = self.url

        if not self.url.startswith(('http://', 'https://')): # Necessário para evitar bugs com o urlparse
            url = 'https://' + self.url

        url = urlparse(url)
        domain = url.netloc.lstrip('www.') # remove o www
        page_name: str = domain.split('.')[0]

        return page_name

    def check_page_in_cache(self):
        """ Verifica se já possui a pagina salva no cache """
        cached_page = Path(f"{self.folder_path}/page.html")

        if cached_page.exists():
            return self.open_page_in_cache(cached_page)

        else:
            return self.get_request_page().data

    @staticmethod
    def open_page_in_cache(path: Path):
        file = open(path, 'r').read()
        return file

    def get_request_page(self):
        response = request(self.method, self.url)
        return response

    def parse_page_with_bs4(self):
        response = self.check_page_in_cache()
        soup = BeautifulSoup(response, "html.parser")
        self.save_page_in_cache(soup)
        return soup

    def save_page_in_cache(self, page: BeautifulSoup):
        """ Salva o conteudo da pagina no cache """
        self.delete_html_page()

        filename: Path = Path(f"{self.folder_path}/page.html")
        self.create_page_folders()

        with open(filename, "w") as f:
            f.write(page.prettify())

    def create_page_folders(self):
        """ Cria as pastas pages/sitename e pages/sitename/src """
        if not self.folder_src.exists():
            self.folder_src.mkdir(parents=True, exist_ok=True)

        else:
            shutil.rmtree(self.folder_src)


simple_scrapper = SimpleScraper()

if __name__ == "__main__":
    simple_scrapper.show_app_name()
