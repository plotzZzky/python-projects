from SimpleCheckout.models.items import Item, get_items
import subprocess


class Order:
    """
        Classe base para cada lista de compras
        - Possui a lista de items e o valor total da compra
        - Faz as compras e adiciona na lista de items
        - Exibe os items e os valores

        Args:
            order_id (int) - O id dessa lista de compras
    """
    total_in_order: float = 0
    items: list[Item] = []

    def __init__(self, order_id: int):
        self.id: int = order_id
        self.items: list[Item] = [] # Limpa a lista para evitar bugs

    def add_item_to_order(self):
        """
            Loop para adicionar um novo item no carrinho

            Steps:
                - Recebe o id do item ou enter para sair do loop
                - Verifica se o id é um numero de id valido
                - Se sim, busca na lista um id com esse id e adiciona na lista de compras
                - Se não, sai do loop
        """
        item_id: int | str = input("Digite o id do item ou 'enter' para sair: ")

        if item_id != "":
            self.check_item_id(int(item_id))
            self.add_item_to_order() # Loop

        else:
            self.clean_terminal()
            self.show_all_items()
            self.receive_customer_cash()

    def check_item_id(self, item_id: int):
        """
            Verifica se possui um item como o id passado

            Args:
                item_id (int) - O id do item a ser adicionado na lista de compras

            Steps:
                - Recebe o id do item
                - Verifica se existe
                - Se não, avisa que não encontrou
                - Se sim, adiciona o item a lista de compras
        """
        new_item: Item = get_items(item_id)

        if not new_item:
            print("Item não encontrado!")

        else:
            self.add_item(new_item)

    def add_item(self, item: Item):
        """
            Adiciona o item a lista de compras

            Args:
                item (Item) - Item para ser adicionado

            Steps:
                - Adiciona o novo item a lista
                - Limpa o terminal
                - Exibe a lista com todos os items
                - Exibe a mensagem de novo item adicionado
        """
        if item:
            self.items.append(item)
            self.clean_terminal()
            self.show_all_items()
            print(f"\n{item.name} adicionado ao carinho!")

    def show_all_items(self):
        """
            Exibe a lista com todos os items

            Steps:
            - Gera o nome do pedido
            - Exibe o cabeçalho com o nome
            - Organiza a lista de compras por ordem alfabética
            - Para cada item da lista exibe chama a função show_item_name_and_price
            - Exibe o total
        """
        name: str = f"Pedido {self.id:02d}"
        print(f"\n{'-' * 32} {name} {'-' * 32}")
        self.total_in_order = 0

        for item in sorted(self.items, key=lambda i: i.name.lower()): # Calcula o total
            self.show_item_name_and_price(item)

        self.show_total()

    def show_item_name_and_price(self, item):
        """
            Adiciona o item ao total e exibe o nome e preço do item

            Args:
                item (Item) - Item para ser exibido

            Steps:
                - Soma o preço do item ao total
                - Formata o preço para ficar no formato x.00
                - Exibe o item.name e o item.price com a formatação adequada
        """
        self.total_in_order += item.price
        price: str = f"{item.price:.2f}"
        print(f"{item.name:<63} R${price:>7}")

    def show_total(self):
        """ Exibe o valor total das compras """
        total: str = f"{self.total_in_order:.2f}"
        print(f"\n{'Total':<62} R$ {total:>7}")
        print(f"{'-' * 74}")

    def receive_customer_cash(self):
        """
            Recebe o valor do usuário

            Steps:
                - Recebe o valor recebido
                - Calcula o troco
                - Se o valor for suficiente exibe o troco
                - Se não, exibe a mensagem de erro
        """
        customer_cash: float = float(input("\nDigite o valor recebido: "))
        change: float = customer_cash - self.total_in_order  # Calcula o troco

        if change >= 0:
            self.show_change_amount(change)

        else:
            print("\nO valor recebido não é suficiente!")
            self.receive_customer_cash()

    @staticmethod
    def show_change_amount(change):
        """ Exibe o valor do troco """
        print(f"\nO troco é R$ {change:.2f}")

    @staticmethod
    def clean_terminal():
        subprocess.call("clear")
