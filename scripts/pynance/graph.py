import plotly.graph_objs as go
from plotly.subplots import make_subplots


class GraphClass:
    # Classe que gera a tabela e mostra ela
    title: str = "Graficos do seu orçamento"
    fig = None

    def __init__(self, data):
        self.data = data

    def create_graph(self):
        # Criação dos subplots
        self.fig = make_subplots(
            rows=2,
            cols=2,
            horizontal_spacing=0.01,
            vertical_spacing=0.02,
            specs=[
                [{"type": "pie"}, {"type": "pie"}],
                [{"type": "pie"}, {"type": "pie"}],
            ],
        )

        self.create_simple_pie()

    # Gera o graficos pizza com todas informações grais do orçamento
    def create_simple_pie(self):
        name: str = "Gráfico geral das despesas"
        labels: list = ["Gastos essencias", "Gastos pessoais", "Economias", "saldo"]
        colors: list = ["red", "orange", "blue", "green"]
        values: list = [
            self.data.gastos_essenciais,
            self.data.gastos_pessoais,
            self.data.economias,
            self.data.saldo,
        ]

        self.create_generic_pie(name, values, labels, colors, 1, 1)
        self.create_detailed_pie()

    # Gera o graficos pizza com todas informações detalhadas do orçamento
    def create_detailed_pie(self):
        name: str = "Gráfico detalhado das despesas"
        values_data: list = [
            {"value": self.data.aluguel, "label": "Aluguel"},
            {"value": self.data.transporte, "label": "Transporte"},
            {"value": self.data.saude, "label": "Saúde"},
            {"value": self.data.servicos, "label": "Serviços"},
            {"value": self.data.alimentacao, "label": "Alimentação"},
            {"value": self.data.educacao, "label": "Educação"},
            {"value": self.data.cartao, "label": "Cartão"},
            {"value": self.data.telefonia, "label": "Telefonia"},
            {"value": self.data.hobby, "label": "Hobby"},
            {"value": self.data.viagens_e_passeios, "label": "Viagens e passeios"},
            {"value": self.data.compras, "label": "Compras"},
            {"value": self.data.refeicoes_especiais, "label": "Refeições especiais"},
            {"value": self.data.saldo, "label": "Saldo"},
        ]
        values: list = []
        labels: list = []
        for item in values_data:
            if item["value"] > 0:
                values.append(item["value"])
                labels.append(item["label"])

        self.create_generic_pie(name, values, labels, [], 1, 2)
        self.create_income_pie()

    # cria o grafico que mostra o percentual das fontes de renda
    def create_income_pie(self):
        name: str = "Gráfico das fontes de renda"
        colors: list = ["green", "blue", "yellow", "orange"]
        values: list = []
        labels: list = []
        values_data: list = [
            {"value": self.data.salario, "label": "Salário"},
            {"value": self.data.investimentos, "label": "Investimentos"},
            {"value": self.data.passivos, "label": "Passivos"},
            {"value": self.data.outras_rendas, "label": "Outras rendas"},
        ]
        for item in values_data:
            if item["value"] > 0:
                values.append(item["value"])
                labels.append(item["label"])

        self.create_generic_pie(name, values, labels, colors, 2, 1)

        # Mostar o grafico apenas se o valor do aluguel for maior que 0
        if self.data.aluguel > 0:
            self.create_rent_pie()
        else:
            self.add_title()

    # Cria o grafico do porcentual gasto com aluguel
    def create_rent_pie(self):
        name: str = "Gráfico porcentagem da despesa com aluguel"
        saldo: int = self.data.rendimentos - self.data.aluguel
        values: list = [self.data.aluguel, saldo]
        labels: list = ["Aluguel", "Saldo"]
        colors: list = ["red", "blue"]

        self.create_generic_pie(name, values, labels, colors, 2, 2)
        self.add_title()

    # Função generica para criação dos graficos
    def create_generic_pie(self, name, values, labels, colors, row, col):
        self.fig.add_trace(
            go.Pie(
                name="",
                labels=labels,
                values=values,
                marker=dict(
                    colors=colors,
                ),
                title=dict(text=name, font=dict(size=26, family="Calibri")),
                showlegend=False,  # Esconde a legenda do gráfico
                textinfo="percent",
                textfont=dict(size=16),
            ),
            row=row,
            col=col,
        )

    def add_title(self):
        # Atualizando o layout para adicionar títulos
        self.fig.update_layout(
            title=self.title,
            title_x=0.5,
            title_y=1,
            font=dict(
                family="Calibri",
                size=26,
                color="black",
            ),
            margin=dict(t=40, b=0),
            height=1200,
        )

        self.show_graph()

    def show_graph(self):
        # Exibe os graficos
        self.fig.show()
