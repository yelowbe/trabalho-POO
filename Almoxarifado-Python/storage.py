from tkinter import messagebox
from item import Item


class Storage:

    def __init__(self,  dataSource):
        
        self.__dataSource = dataSource 
        self.__items = dataSource["storage"]
        
        self.__currentIndex = (
            dataSource["storage"][len(dataSource["storage"]) - 1][0] + 1 if len(dataSource["storage"]) > 0 else 1
        )

    def __updateNumItens(self):
        """Atualiza a quantidade de itens no dataSource"""
        self.__dataSource["num_itens_storage"] = len(self.__items)
    
    # decoradores
    def canEditProduct(func):
        def wrapper(self, id, name, description, quantity, action):

            if len(name) == 0:
                return messagebox.showerror("Erro", "Nome inválido")
            elif quantity < 1 and not (type(quantity) == int):
                return messagebox.showerror("Erro", "Quantidade inválida")
            elif any(item[2] == name for item in self.__items):
                return messagebox.showerror("Erro", "Esse produto já existe")
            else:
                func(self, id, name, description, quantity, action)

        return wrapper

    # métodos
    @property
    def items(self):
        return self.__items

    def addProduct(self, *args, action):
        newProduct = Item(self.__currentIndex, *args, self.__items)
        self.__items.append(newProduct.toListable())
        self.__updateNumItens()
        self.__currentIndex = self.__currentIndex + 1
        messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
        action()

    @canEditProduct
    def editProduct(self, id, name, description, quantity, action):
        self.__items[id][1] = name
        self.__items[id][2] = description
        self.__items[id][3] = quantity

        messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
        action()

    def deleteProduct(self, name, action):
        selectedIndex = next(
            (i for i, item in enumerate(self.__items) if item[1] == name), None
        )
        self.__items.pop(selectedIndex)
        self.__updateNumItens()
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        action()
