from BoilerPlate.boilerplate import CliBoilerplate
from SimpleCheckout.models.order import Order
import art


class Checkout(CliBoilerplate):
    CLI_DESC: str = "Caixa simples em cli"
    cash: float = 0
    SLEEP_TIME: float = 1

    order: Order | None = None
    orders: list[Order] = []

    def __init__(self):
        super().__init__()

        self.menu_options: list = [
            self.new_order,
            self.show_all_orders,
            self.cash_in,
            self.cash_out,
        ]

    def new_order(self):
        """
            Cria uma nova lista de compras

            Steps:
                - Cria um novo id
                - Cria uma nova lista de compras
                - Inicia o loop das compras
                - fecha o loop de compras
        """
        order_id: int = len(self.orders) + 1
        self.order: Order = Order(order_id)
        self.order.add_item_to_order() # loop das compras
        self.close_order()

    def close_order(self):
        """
            Encerra uma lista de compras

            Steps:
                - Soma o total da lista de compras ao valor em caixa
                - Adiciona a lista de compras a lista com todas as listas do dia
                - Limpa a lista de compras
        """
        self.cash += self.order.total_in_order
        self.orders.append(self.order)
        del self.order

    def show_all_orders(self):
        """ Exibe o conteúdo de todas as listas de compras do dia """
        for order in self.orders:
            order.show_all_items()

    def cash_in(self):
        """
            Entrada de dinheiro no caixa

            Steps:
                - Recebe o valor para ser colocado ao caixa
                - Se o valor for invalido retorna ao menu
                - Soma o valor a ser adicionado ao que ja tem
        """
        self.generic_menu_msg("Entrada de dinheiro")
        amount: float = float(input("Digite a quantidade a ser adicionada ou enter para cancelar: "))

        if not amount:
            pass

        print(f"R${amount} adicionado ao caixa.")
        self.cash += amount

    def cash_out(self):
        """
            Retirada de dinheiro do caixa
            - Essa função é usada para o nome no menu inicial ficar correto
            - Se não possuir dinheiro no caixa retorna ao menu inicial
        """
        if self.cash == 0:
            print("\nVocê não possui dinheiro no caixa.")
        else:
            self.get_cash_out_option()

    def get_cash_out_option(self):
        """
            Retirada de dinheiro fo caixa

            Steps:
                - Recebe o valor para ser colocado ao caixa
                - Chama a função que verifica se o valor e valido
        """
        self.generic_menu_msg("Retirada de dinheiro")
        amount: float = float(input("Quantidade a ser removida ou 'enter' para cancelar: "))
        self.check_cash_out_option(amount)

    def check_cash_out_option(self, amount: float):
        """
            Verifica se o valor digitado é valido

            Steps:
                - Verifica se o valor é valido
                - Se não, volta ao menu inicial
                - Se sim, verifica se tem dinheiro o suficiente no caixa
                - Se houver dinheiro retira do caixa
        """
        if amount == "":
            pass

        if amount > self.cash:
            print("\nO caixa não tem dinheiro o suficiente!!!")
            self.cash_out()
        else:
            self.cash -= amount

    # ------------- Funções modificadas por necessidade do projeto --------------------
    def welcome_msg(self):
        """
            Tela de apresentação (nome e descrição) do cliapp
            Se tiver o art instalado exibe o nome usando o, se não, usa o inbuilt print
        """
        self.clean_terminal()
        art.tprint(f"{' ' * self.CLI_NAME_SPACE} {self.CLI_NAME}", "tarty1")

        # Calcula a largura e exibe a descriçao do cliapp
        width: int = self.receive_terminal_width(self.CLI_DESC)
        print(f"{' ' * width} {self.CLI_DESC}")
        print(f"Saldo R$: {self.cash:.2f}") # Adicionado o saldo

    def restart_cli(self):
        """ reinicia o cliapp quando o usuario digitar uma opção invalida """
        self.welcome_msg()
        # print('Opção invalida!!!') removido o print
        self.start_menu()


checkout = Checkout()

if __name__ == "__main__":
    checkout.main_loop()
