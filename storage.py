from tkinter import messagebox
from typing import Callable, List, Any, Dict, Tuple
from item import Item
from exception import ExceptionInvalidName, ExceptionInvalidQuantity

class ProductAction:
    """Classe base para ações sobre produtos."""
    
    def __init__(self, storage: 'Storage', action: Callable[[], None]) -> None:
        self.storage: 'Storage' = storage
        self.action: Callable[[], None] = action

    def execute(self) -> None:
        raise NotImplementedError("Método execute deve ser implementado nas subclasses")

class AddProduct(ProductAction):
    def __init__(self, storage: 'Storage', action: Callable[[], None], *args: Any) -> None:
        super().__init__(storage, action)
        self.args: Tuple[Any, ...] = args

    def execute(self) -> None:
        try:
            newProduct = Item(self.storage._Storage__currentIndex, *self.args, self.storage.items)
            self.storage.items.append(newProduct.toListable())
            self.storage._Storage__updateNumItens()
            self.storage._Storage__currentIndex += 1
            messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
            self.action()
        except ExceptionInvalidName:
            print("Nome inválido\n")
        except ExceptionInvalidQuantity:
            print("Quantidade de produto inválida\n")

class EditProduct(ProductAction):
    def __init__(self, storage: 'Storage', action: Callable[[], None], id: int, name: str, description: str, quantity: int) -> None:
        super().__init__(storage, action)
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.quantity: int = quantity

    def execute(self) -> None:
        self.storage.items[self.id][1] = self.name
        self.storage.items[self.id][2] = self.description
        self.storage.items[self.id][3] = self.quantity
        messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
        self.action()

class DeleteProduct(ProductAction):
    def __init__(self, storage: 'Storage', action: Callable[[], None], name: str) -> None:
        super().__init__(storage, action)
        self.name: str = name

    def execute(self) -> None:
        selectedIndex = next(
            (i for i, item in enumerate(self.storage.items) if item[1] == self.name), None
        )
        if selectedIndex is not None:
            self.storage.items.pop(selectedIndex)
            self.storage._Storage__updateNumItens()
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
            self.action()

# Atualizando a classe Storage para usar as classes de polimorfismo
class Storage:
    def __init__(self, dataSource: Dict[str, Any]) -> None:
        self.__dataSource: Dict[str, Any] = dataSource 
        self.__items: List[List[Any]] = dataSource["storage"]
        self.__currentIndex: int = (
            dataSource["storage"][-1][0] + 1 if len(dataSource["storage"]) > 0 else 1
        )

    def __updateNumItens(self) -> None:
        """Atualiza a quantidade de itens no dataSource"""
        self.__dataSource["num_itens_storage"] = len(self.__items)

    @property
    def items(self) -> List[List[Any]]:
        return self.__items  # Retorna os itens armazenados corretamente

    # Métodos de manipulação de produtos
    def addProduct(self, *args: Any, action: Callable[[], None]) -> None:
        AddProduct(self, action, *args).execute()

    def editProduct(self, id: int, name: str, description: str, quantity: int, action: Callable[[], None]) -> None:
        EditProduct(self, action, id, name, description, quantity).execute()

    def deleteProduct(self, name: str, action: Callable[[], None]) -> None:
        DeleteProduct(self, action, name).execute()