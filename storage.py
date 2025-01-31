from tkinter import messagebox
from item import Item
from exception import *

class ProductAction:
    """Classe base para ações sobre produtos."""
    
    def __init__(self, storage, action):
        self.storage = storage
        self.action = action

    def execute(self):
        raise NotImplementedError("Método execute deve ser implementado nas subclasses")

class AddProduct(ProductAction):
    def __init__(self, storage, action, *args):
        super().__init__(storage, action)
        self.args = args

    def execute(self):
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
    def __init__(self, storage, action, id, name, description, quantity):
        super().__init__(storage, action)
        self.id = id
        self.name = name
        self.description = description
        self.quantity = quantity

    def execute(self):
        self.storage.items[self.id][1] = self.name
        self.storage.items[self.id][2] = self.description
        self.storage.items[self.id][3] = self.quantity
        messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
        self.action()

class DeleteProduct(ProductAction):
    def __init__(self, storage, action, name):
        super().__init__(storage, action)
        self.name = name

    def execute(self):
        selectedIndex = next(
            (i for i, item in enumerate(self.storage.items) if item[1] == self.name), None
        )
        self.storage.items.pop(selectedIndex)
        self.storage._Storage__updateNumItens()
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        self.action()

# Atualizando a classe Storage para usar as classes de polimorfismo
class Storage:
    def __init__(self, dataSource):
        self.__dataSource = dataSource 
        self.__items = dataSource["storage"]
        self.__currentIndex = (
            dataSource["storage"][-1][0] + 1 if len(dataSource["storage"]) > 0 else 1
        )

    def __updateNumItens(self):
        """Atualiza a quantidade de itens no dataSource"""
        self.__dataSource["num_itens_storage"] = len(self.__items)

    @property
    def items(self):
        return self.__items  # Retorna os itens armazenados corretamente

    # Métodos de manipulação de produtos
    def addProduct(self, *args, action):
        AddProduct(self, action, *args).execute()

    def editProduct(self, id, name, description, quantity, action):
        EditProduct(self, action, id, name, description, quantity).execute()

    def deleteProduct(self, name, action):
        DeleteProduct(self, action, name).execute()