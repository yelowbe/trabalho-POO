from tkinter import messagebox


class Item:

    def __init__(self, id, name, description, quantity, items):
        if len(name) == 0:
            return messagebox.showerror("Erro", "Nome inválido")
        elif quantity < 1 and not (type(quantity) == int):
            return messagebox.showerror("Erro", "Quantidade inválida")
        elif any(item[1] == name for item in items):
            return messagebox.showerror("Erro", "Esse produto já existe")
        else:
            self.__id = id
            self.__name = name
            self.__description = description
            self.__quantity = quantity
            self.__items = items


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) == 0:
            return messagebox.showerror("Erro", "Nome inválido")
        elif any(item[1] == value for item in self.__items):
            return messagebox.showerror("Erro", "Esse produto já existe")
        else:
            self.__name = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if value < 1 and not (type(value) == int):
            return messagebox.showerror("Erro", "Quantidade inválida")
        else:
            self.__quantity = value

    def toListable(self):
        return [self.__id, self.__name, self.__description, self.__quantity, ">"]
