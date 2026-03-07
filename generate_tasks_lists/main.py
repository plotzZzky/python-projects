import pandas as pd
from pathlib import Path
from odf.table import Table, TableRow, TableCell
from odf.opendocument import load
from odf.text import P


class CreateCompaniesTable:
    """ Script que gera listas individuais de tarefas para cada colaborador """
    APP_DESC: str = "Esse script que cria as tabelas de empresas por colaborador\n"

    companies: list = []
    staff_members: dict = {} # disc com os menbros da equipe
    save_folder_path: Path = "Equipe"

    doc = None
    table = None

    def welcome_menu(self):
        print(f"{' ' * 35} {self.__class__.__name__}")
        print(self.APP_DESC)
        self.open_companies_list()

    def open_companies_list(self):
        try:
            file_path: Path = Path('./empresas.ods')
            self.create_companies_df(file_path)
        except FileNotFoundError:
            print("Lista com as empresas não encontradas!")

    def create_companies_df(self, file_path: Path):
        df = pd.read_excel(file_path)
        dicts: list = df.to_dict(orient='records')

        """ Cria uma lista de dicts com chave o nome do colaborador e valor a lista de empresas dele """
        self.companies: list = [{key: company[key] for key in company} for company in dicts]

        self.assign_companies_to_staff_member()

    def assign_companies_to_staff_member(self):
        """ Atribui cada empresa ao dict do colaborador """
        for company in self.companies:
            name = company['Responsável pela Abordagem'].split(' ')[0]

            if name not in self.staff_members:
                self.staff_members[name] = []
            self.staff_members[name].append(company)

        self.create_staff_table()

    def create_staff_table(self):
        for name in self.staff_members:
            self.open_base_table()
            self.fill_staff_table(name)

    def open_base_table(self):
        try:
            file_path: Path = Path("Modelos/base_table.ods")
            self.doc = load(file_path)
            self.table = self.doc.getElementsByType(Table)[0]
        except FileNotFoundError:
            print('\nTabela base não encontrada\n')

    def fill_staff_table(self, member_name: str):
        # Preenche o modelo a tabela base com as tarefas de cada funcionario
        for index, company in enumerate(self.staff_members[member_name], 1):
            address: str = f"{company['Municipio']}, {company['Bairro da UC']}, {company['Endereço da UC']}"
            model: str = f"-{company['Modelo']}" if pd.notna(company['Modelo']) else ""
            form: str = f"{company['Pesquisa']}{model}"
            fill_email: str = f"{company['Razão Social']}, CNPJ: {company['CNPJ']} - ({form})"

            self.receive_and_fill_cell(index, 0, fill_email)
            self.receive_and_fill_cell(index, 1, company['CNPJ'])
            self.receive_and_fill_cell(index, 2, company['Razão Social'])
            self.receive_and_fill_cell(index, 3, company['PO Sel.'])
            self.receive_and_fill_cell(index, 4, form)
            self.receive_and_fill_cell(index, 5, company['Telefone do Contato'])
            self.receive_and_fill_cell(index, 6, company['E-mail do Contato'])
            self.receive_and_fill_cell(index, 7, address)

        self.check_if_save_folder_exist(member_name)

    def receive_and_fill_cell(self, row_index, column_index, value):
        row = self.get_or_create_row(row_index)
        cell = self.get_or_create_cell(row, column_index)
        self.fill_cell(cell, value)

    def get_or_create_row(self, row_index):
        rows = self.table.getElementsByType(TableRow)
        if row_index >= len(rows):
            row = TableRow()
            self.table.addElement(row)
            return row
        return rows[row_index]

    @staticmethod
    def get_or_create_cell(row, column_index):
        cells = row.getElementsByType(TableCell)
        if column_index >= len(cells):
            cell = TableCell()
            row.addElement(cell)
            return cell
        return cells[column_index]

    def fill_cell(self, cell, value):
        self.clean_cell(cell)
        new_value: P = P(text=value)
        cell.addElement(new_value)

    @staticmethod
    def clean_cell(cell):
        while cell.childNodes:
            cell.removeChild(cell.childNodes[0])
            
    def check_if_save_folder_exist(self, member_name: str):
        if not Path(self.save_folder_path).exists():
            Path.mkdir(Path(self.save_folder_path))

        self.save_new_table(member_name)

    def save_new_table(self, member_name: str):
        new_name: str = f"{self.save_folder_path}/Empresas_{member_name}.ods"
        self.doc.save(new_name)
        print(f"{new_name} gerada com sucesso!")


script = CreateCompaniesTable()

if __name__ == '__main__':
    script.welcome_menu()
