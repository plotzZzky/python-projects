class GetData:
    # Classe que recebe e calcula o rendimento e as despesas
    about_incomes = (
            "Valores recebidos neste mês atraves de salarios, investimentos e passivos"
        )
    sobre_gastos_essenciais = (
            "Gastos recorentes e essencias para sua vida economica."
        )
    sobre_gastos_pessoais = (
            "Gastos recorentes e importantes para sua vida, mas não essenciais podendo ser "
            "reduzidas ou cortados em situações de emergencia"
        )
    sobre_economias = "Valores guardados para metas ou emergencias"

    @staticmethod
    def get_value(placeholder: str = 'Digite um valor') -> int:
        # Modelo generico de input para receber os valores
        while True:
            try:
                value: int = int(input(placeholder))
                return value
            except (ValueError, TypeError):
                print(f"O valor deve ser em numeros inteiros!!!\n")

    def get_income(self):
        print(self.about_incomes)

        self.salario = self.get_value("Digite o valor liquido do seu salario:\n")
        self.investimentos = self.get_value(
            "Digite o valor liquido do lucro dos seus investimentos:\n"
        )
        self.passivos = self.get_value("Digite o valor liquido da sua renda passiva:\n")
        self.outras_rendas = self.get_value(
            "Digite o valor liquido recebido de outras formas de renda:\n"
        )

        self.rendimentos = (
            self.salario + self.investimentos + self.passivos + self.outras_rendas
        )

        print(f"Seu rendimento nesse mês foi de {self.rendimentos}\n")
        self.get_essential_expenses()

    def get_essential_expenses(self):
        print(self.sobre_gastos_essenciais)

        try:
            self.aluguel = self.get_value("Digite o valor gasto com aluguel:\n")
            self.transporte = self.get_value("Digite o valor gasto com transporte:\n")
            self.servicos = self.get_value(
                "Digite o valor gasto com serviços de luz, agua, gas etc.:\n"
            )
            self.alimentacao = self.get_value(
                "Digite o valor gasto com alimentção do dia a dia, "
                "não inclua idas ocasionais a restaurantes e comidas especias:\n"
            )
            self.saude = self.get_value(
                "Digite o valor gasto com saude, medicos e farmacia:\n"
            )
            self.educacao = self.get_value("Digite o valor gasto com educação:\n")

            self.gastos_essenciais = sum([
                self.telefonia, self.aluguel, self.transporte, self.saude,
                self.servicos, self.alimentacao, self.educacao
            ])

            print(f"O total de gastos essenciais foi de {self.gastos_essenciais}")
            self.get_personal_expenses()

        except (ValueError, TypeError):
            print(f"O valor deve ser em numeros inteiros")
            self.get_essential_expenses()

    def get_personal_expenses(self):
        print(self.sobre_gastos_pessoais)

        try:
            self.cartao = self.get_value(
                "Digite o valor gasto com cartão de credito:\n"
            )
            self.telefonia = self.get_value(
                "Digite o valor gasto com telefonia e internet:\n"
            )
            self.hobby = self.get_value("Digite o valor gasto com hobby:\n")
            self.viagens_e_passeios = self.get_value(
                "Digite o valor gasto com viagens e passeios:\n"
            )
            self.compras = self.get_value(
                "Digite o valor gasto com compras não essenciais:\n"
            )
            self.refeicoes_especiais = self.get_value(
                "Digite o valor gasto refeições especias como idas a restaurantes e outros:\n"
            )

            self.gastos_pessoais = (
                self.cartao
                + self.telefonia
                + self.hobby
                + self.viagens_e_passeios
                + self.compras
                + self.refeicoes_especiais
            )

            print(f"O total de gastos pessoais foi de {self.gastos_pessoais}")
            self.get_investments_and_savings()

        except (ValueError, TypeError):
            print(f"O valor deve ser em numeros inteiros")
            self.get_personal_expenses()

    def get_investments_and_savings(self):
        print(self.sobre_economias)

        try:
            self.poupanca = self.get_value(
                "Digite o valor destinado a poupança esse mes:\n"
            )
            self.reserva = self.get_value(
                "Digite o valor destinado a reserva de emergencia esse mes:\n"
            )
            self.novos_investimentos = self.get_value(
                "Digite o valor destinado a novos investimentos:\n"
            )

            self.economias = self.poupanca + self.reserva + self.novos_investimentos

            print(f"O total economizado esse mês foi de {self.economias}")
            self.get_percentagem()

        except (ValueError, TypeError):
            print(f"O valor deve ser em numeros interos")
            self.get_investments_and_savings()

    # Função que calcula a porcentagem, usada para simplicar codigo ja que ela é usada varias vezes
    def calculate_percentagem(self, value):
        return round((value / self.rendimentos) * 100, 1)

    def get_percentagem(self):
        self.saldo = self.rendimentos - (
            self.gastos_essenciais + self.gastos_pessoais + self.economias
        )
        print(f"Seu saldo nesse mês foi de de R$ {self.saldo}")
        if self.saldo > 0:
            print(f"Seu saldo foi positivo, muito bom!\n")
        else:
            print(f"Seu saldo foi negativo, Precisa rever seus gastos!\n")

        # porcentagem da receita gasto com alugueis
        self.porcentagem_aluguel = self.calculate_percentagem(self.aluguel)
        print(
            f"A porcentagem do gasto com aluguel nesse mês foi de {self.porcentagem_aluguel}%"
        )

        # Porcentagem da receita destinados aos gastos essenciais
        self.porcentagem_gastos_essenciais = self.calculate_percentagem(
            self.gastos_essenciais
        )
        print(
            f"A porcentagem dos gastos essenciais nesse mês foi de {self.porcentagem_gastos_essenciais}%"
        )

        # Porcentagem da receita destinada aos gastos pessoais
        self.porcentagem_gastos_pessoais = self.calculate_percentagem(
            self.gastos_pessoais
        )
        print(
            f"A porcentagem dos gastos pessoais nesse mês foi de {self.porcentagem_gastos_pessoais}%"
        )

        # porcentagem da receita destina a poupança e reservas de emergencia
        self.porcentagem_poupanca = self.calculate_percentagem(self.economias)
        print(f"A porcentagem da poupança nesse mês {self.porcentagem_poupanca}%\n")

        print("Veja os graficos para mais detalhes!")

    # Função para testar o app sem precisar preencher os campos
    def test(self):
        print("\nPreenchendo os campos com valores genericos para teste...\n")

        self.salario = 3500
        self.investimentos = 150
        self.passivos = 0
        self.outras_rendas = 0

        self.rendimentos = (
            self.salario + self.investimentos + self.passivos + self.outras_rendas
        )
        print(f"Seu rendimento nesse mes foi de R$ {self.rendimentos}")

        self.aluguel = 1500
        self.transporte = 150
        self.saude = 100
        self.servicos = 300
        self.alimentacao = 300
        self.educacao = 0
        self.gastos_essenciais = (
            self.aluguel
            + self.transporte
            + self.saude
            + self.servicos
            + self.alimentacao
            + self.educacao
        )
        print(f"Seus gastos essencias foram de R$ {self.gastos_essenciais}")

        self.cartao = 100
        self.telefonia = 150
        self.hobby = 200
        self.viagens_e_passeios = 200
        self.compras = 300
        self.refeicoes_especiais = 300
        self.gastos_pessoais = (
            self.telefonia
            + self.hobby
            + self.viagens_e_passeios
            + self.compras
            + self.refeicoes_especiais
        )
        print(f"Seus gastos pessoais não essencias foram de R$ {self.gastos_pessoais}")

        self.poupanca = 0
        self.reserva = 100
        self.novos_investimentos = 0

        self.economias = self.poupanca + self.reserva + self.novos_investimentos
        print(f"Sua economia foi de R$ {self.economias}")

        self.get_percentagem()
