from Classes.map import MapTableCreator
from Classes.visit import VisitTableCreator
from datetime import date
from pathlib import Path
import pandas as pd
import shutil


class Start:
    """ Appcli para gerar as planilhas usadas nas visitas"""
    APP_DESC: str = "App para gerar as tabelas de visitas "

    today: date = None
    folder_name: str = None

    companies: list = []

    def welcome_menu(self):
        print(f"{' ' * 35} {self.__class__.__name__}")
        print(self.APP_DESC)
        self.open_companies_list()

    def open_companies_list(self):
        """ Abre a lista com todas as empresas a serem visitadas """
        try:
            file_path: Path = Path('empresas.ods').absolute()
            self.create_companies_df(file_path)
        except FileNotFoundError:
            print("\nLista de empresas não encontrada!\n")

    def create_companies_df(self, file_path):
        df = pd.read_excel(file_path)
        dicts: list = df.to_dict(orient='records')

        """ Converte o df em uma lista de dicts """
        self.companies: list = [{key: company[key] for key in company} for company in dicts]
        self.create_today_folder()

    def create_today_folder(self):
        """ Cria a pasta para salvar as tabelas """
        self.today: str = self.get_today_date()
        self.folder_name: str = f"Tabelas/{self.today}"

        if not Path(self.folder_name).exists():
            Path(self.folder_name).mkdir()
            Path(f"{self.folder_name}/Cartas").mkdir()
            print("\nPastas geradas!")

        self.create_tables()

    def create_tables(self):
        _visit = VisitTableCreator(today=self.today, folder_name=self.folder_name, companies=self.companies)
        _map = MapTableCreator(today=self.today, folder_name=self.folder_name, companies=self.companies)

        _visit.open_visits_table()
        _map.open_map_table()
        self.rename_companies_table()

    @staticmethod
    def get_today_date() -> str:
        today: date = date.today()
        formated_today: list = str(today).split('-')
        return f"{formated_today[2]}_{formated_today[1]}_{formated_today[0]}"

    def rename_companies_table(self):
        """ Renomea e move a tabela de empresas para a pasta de hj """
        shutil.move('empresas.ods', f"{self.folder_name}/empresas.ods")
        Path(f"{self.folder_name}/empresas.ods").rename(f"{self.folder_name}/empresas_{self.today}.ods")


script = Start()

if __name__ == '__main__':
    script.welcome_menu()
