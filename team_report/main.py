# Esse script gera um conjunto de graficos, para demostrar o desempenho de uma equipe ao executar um conjunto de tarefas
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import date
from pathlib import Path
import sys
import csv


class GenerateData:
    # Classe "generica" que recebe os dados e os formata para ser usado por outras classes que geram os graficos
    values: list = []
    file = None

    path = Path(__file__).parent.resolve()

    def open_file(self):
        try:
            f = open(f"{self.path}/relatorio.csv")
            self.file = csv.reader(f, delimiter=";")
            f.close()
            self.get_data()
        except FileNotFoundError:
            print("Relatorio não encontrado!")
            if __name__ == '__main__':
                sys.exit()

    def get_data(self):
        n = 0
        for row in self.file:
            if n != 0:
                # Formata o nome do colaborador, mantendo apenas o nome sem o sobrenome
                name = row[1].split(" ")[0]

                all_tasks = int(row[13])

                # Quantidade ja completada de tarefas
                completed_tasks = int(row[4])

                incomplete_tasks = int(row[13])

                # Lista com valores de completas e incompletas para ser usada nos graficos pizza
                values = [completed_tasks, incomplete_tasks]

                # Porcentagem das tarefas concluidas
                completion_percentage = (completed_tasks / all_tasks) * 100

                # Dados formatados para ser usado no grafico
                data_dict = {
                    "name": name,
                    "values": values,
                    "meta": completion_percentage,
                }
                self.values.append(data_dict)
            else:
                n += 1  # Ignora o cabeçalho da tabela


class GraphPie:
    # Classe que gera os graficos pizza medindo a performance da equipe
    def __init__(self, data):
        strdate = str(date.today()).split("-")
        today = f"{strdate[2]}/{strdate[1]}/{strdate[0]}"

        state = "Etapa do projeto"
        self.title = f'Desempenho da equipe na fase "{state}", no dia {today}'
        self.labels = ["Concluidas", "Faltantes"]
        self.values = data.values  # Valores gerados pela classe GenerateData

        self.META = 65  # Meta da porcentagem de tarefas concluidas na data atual
        self.fig = None

    def create_subplot(self):
        # Criação dos subplots (2 linhas, 4 colunas)
        self.fig = make_subplots(
            rows=2,
            cols=4,
            specs=[
                [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
                [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
            ],
            horizontal_spacing=0.01,
            vertical_spacing=0.01,
        )
        self.create_pies()

    # Gera os graficos pizza
    def create_pies(self):
        row = 1
        col = 1

        for item in self.values:
            # Se o colaborador atingir a meta a cor do grafico sera azul, se não, vermelha
            color = "blue" if item["meta"] > self.META else "red"
            name = item["name"].capitalize()  # Nome do colaborador

            self.generic_pie(item["values"], color, name, row, col)

            col += 1
            if col == 5:
                row = 2
                col = 1

        self.add_title()

    def generic_pie(self, values, color, name, row, col):
        self.fig.add_trace(
            go.Pie(
                name="",
                labels=self.labels,
                values=values,
                marker=dict(colors=[color, "lightgrey"]),
                title=dict(text=name, font=dict(size=26, family="Calibri")),
                showlegend=False,  # Remove a leganda lateral
            ),
            row=row,
            col=col,
        )

    def add_title(self):
        # Atualiza o layout para adicionar títulos
        self.fig.update_layout(
            title=self.title,
            title_x=0.5,
            title_y=0.99,
            font=dict(
                family="Calibri",
                size=26,
                color="black",
            ),
        )
        self.show_graph()

    def show_graph(self):
        # Exibe os graficos
        self.fig.show()


generate_data = GenerateData()
pie = GraphPie(generate_data)


def create_report():
    generate_data.open_file()
    pie.create_subplot()


if __name__ == "__main__":
    create_report()
