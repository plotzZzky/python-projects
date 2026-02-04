from pathlib import Path
import pandas as pd
import locale
from datetime import datetime
from odf.table import Table, TableRow, TableCell
from odf.opendocument import load
from odf.text import P


class MonthlyReport:
    # Quantidade de empresas na pesquisa
    PMS_AMOUNT: int = 67
    PIMPF_AMOUNT: int = 77

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    date = datetime.now()
    month = date.strftime("%B")

    doc = None
    table = None

    pms_overdue: list = []
    pimpf_overdue: list = []

    pms_percent: str = 0
    pimpf_percent: str = 0

    save_folder_path: str = "relatorios/"
    saved_file = None


    def welcome(self):
        """ Menu inicial do appcli """
        msg: str = f"{'_' * 20} Relatorio das Mensais {'_' * 20}"
        print(msg)
        self.start_script()

    def start_script(self):
        self.open_model_tabel()

        if Path(self.saved_file).exists(): # verifica se a planilha foi salva
            result = self.success_final_message(self.saved_file)
        else:
            result = self.fail_final_message()

        return result

    def open_model_tabel(self):
        """ Abre o modelo do relatorio a ser preenchido e salva no model """
        try:
            file_path: Path = Path('./modelos/Relatorio.ods')
            self.doc = load(file_path)
            self.table = self.doc.getElementsByType(Table)[0]

            self.retrieve_all_overdue_companies()

        except FileNotFoundError:
            print("Lista com as empresas não encontradas!")

    def retrieve_all_overdue_companies(self):
        """ Recebe a lista com as empresas em atraso """
        self.pms_overdue: list = self.open_overdue_table("pms", 'ISO-8859-1')
        self.pimpf_overdue: list = self.open_overdue_table("pimpf", "utf-8")

        self.fill_model_with_pimpf_overdue_companies()

    def fill_model_with_pimpf_overdue_companies(self):
        """ Seleciona as empresas em atraso para preencher a tabela """
        start_line: int = 2

        for index, company in enumerate(self.pimpf_overdue):
            pimpf_line: int = start_line + index
            self.fill_pimpf_company_line(pimpf_line, company)

        self.fill_model_with_pms_overdue_companies()

    def fill_model_with_pms_overdue_companies(self):
        """ Seleciona as empresas em atraso para preencher a tabela """
        start_line: int = 15

        for index, company in enumerate(self.pms_overdue):
            pms_line: int = start_line + index
            self.fill_pms_company_line(company, pms_line)

        self.retrieve_researches_percents()

    def retrieve_researches_percents(self):
        """ Calcula a porcentagem de cada pesquisa """
        self.pms_percent = self.calculate_research_percent(self.PMS_AMOUNT, self.pms_overdue)
        self.pimpf_percent = self.calculate_research_percent(self.PIMPF_AMOUNT, self.pimpf_overdue)

        self.save_research_percents()

    def save_research_percents(self):
        """ Salva as porcentagens das pesquisas na tabela """
        title = self.date.strftime("%m/%y")
        self.insert_research_percent_on_table(37, title)
        self.insert_research_percent_on_table(38, self.pimpf_percent)
        self.insert_research_percent_on_table(39, self.pms_percent)

        self.check_if_save_folder_exist()

    def check_if_save_folder_exist(self):
        if not Path(self.save_folder_path).exists():
            Path.mkdir(Path(self.save_folder_path))

        self.save_new_table()

    def save_new_table(self):
        """ Salva a nova tabela """
        new_name: str = f"{self.save_folder_path}relatorio_mensais_{self.month}.ods"
        self.doc.save(new_name)
        self.saved_file = new_name

    @staticmethod
    def success_final_message(new_name: str):
        result_msg: str = f"{new_name} gerada com sucesso!"
        print(result_msg)
        return result_msg

    @staticmethod
    def fail_final_message():
        result_msg: str = f"Não foi possivel gerar a tabela!"
        print(result_msg)
        return result_msg

    @staticmethod
    def open_overdue_table(filename: str, encoding: str):
        """ Abre a tabela com a lista de empresass faltantes e retorna o valor """
        try:
            file_path: Path = Path(f"./{filename}.csv")

            if file_path.exists():
                df = pd.read_csv(file_path, encoding=encoding, delimiter=";")
                return df.to_dict(orient='records')

            raise FileExistsError # se o arquivo não existe retorna o error

        except (FileNotFoundError, FileExistsError):
            print(f"Não foi possivel acessar a tabela {filename}!")

    def fill_pms_company_line(self, company, index: int):
        """ Gera a linha com os dados da empresa """
        name: str = company['Razão Social']
        cnpj: str = f"{company['CNPJ (Raiz)']}/000{company['CNPJ (Sufixo)']}-{company['CNPJ (DV)']}"
        self.fill_company_row([cnpj, name], index)

    def fill_pimpf_company_line(self, index: int, company):
        """ Gera a linha com os dados da empresa """
        name: str = company["Razão Social"]
        cnpj: str = company["CNPJ"]
        self.fill_company_row([cnpj, name], index)

    def fill_company_row(self, company, row_index):
        """ Preenche a linha com o valor da empresa """
        row = self.return_row(row_index)

        for index, value in enumerate(company):
            cell = self.return_cell(row, index)
            self.fill_cell(cell, value)

    def return_row(self, index):
        """ Retorna uma linha da tabela pelo index """
        rows = self.table.getElementsByType(TableRow)
        return rows[index]

    @staticmethod
    def return_cell(row, cel_index):
        """ Retorna uma celula da linha pelo index """
        cells = row.getElementsByType(TableCell)
        return cells[cel_index]

    def fill_cell(self, cell, value):
        """ Coloca um novo valor da celula """
        self.clean_cell(cell)
        new_value = P(text=value)
        cell.addElement(new_value)

    @staticmethod
    def clean_cell(cell):
        """ Remove todos os valores da celula """
        while cell.childNodes:
            cell.removeChild(cell.childNodes[0])

    @staticmethod
    def calculate_research_percent(all_companies: int, overdue: list):
        """ Calcula a porcentagem de coleta da pesquisa """
        done: int = all_companies - len(overdue)
        percent: float = (done / all_companies) * 100
        return f"{round(percent)}%"

    def insert_research_percent_on_table(self, row_index: int, new_value):
        """ Atualiza os valores na linha com base no conteúdo das células """
        row = self.return_row(row_index)
        values: list = self.return_values_from_row(row, new_value)

        # insere os valores da lista na tabela
        for index, value in enumerate(values):
            cell = self.return_cell(row, index)
            self.fill_cell(cell, value)

    @staticmethod
    def return_values_from_row(row, new_value):
        """ Retorna os valores da linha atual em uma lista """
        values: list = []

        for cel in row.getElementsByType(TableCell):
            para = cel.getElementsByType(P)
            value = ''.join([p.firstChild.data for p in para if p.firstChild is not None]) # recebe o valor da celula

            if value: # evita que inclua valores em branco
                values.append(value)

        values.insert(1, str(new_value)) # Insere o new_value na segunda posição
        return values[0:-1] # retorna a lista sem o ultimo item


if __name__ == '__main__':
    monthly_report = MonthlyReport()
    monthly_report.welcome()