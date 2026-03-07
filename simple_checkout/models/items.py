
class Item:
    """ Classe dos item do estoque """
    def __init__(self, item_id: int, name: str, price: float):
        self.item_id: int = item_id
        self.name: str = name
        self.price: float = price


all_items: list = [
    Item(1,"Arroz", 4.00),
    Item(2,"Azeite", 5.00),
    Item(3, "Batata", 3.00),
    Item(4, "Frango", 15.00),
    Item(5,"Feijão", 5.00),
    Item(6, "Macarrão", 3.50),
]


def get_items(item_id: int) -> Item | None:
    """
        Retorna o item baseado no id ou None

        Args:
            item_id (int) - Id do item a ser selecionado

        Return:
            Item (Item | None) - o item selecionado pelo usuário ou None
    """
    for item in all_items:
        if item.id == item_id:
            return item

    return None
