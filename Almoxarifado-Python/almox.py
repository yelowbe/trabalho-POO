from tkinter import messagebox


class warehouse:

    def __init__(self,num_itens):
            self.__num_itens = num_itens
            

    @property
    def num_itens(self):
        return self.__num_itens

    @num_itens.setter
    def num_itens(self, value):
        if not len(value) >= 0:
            return messagebox.showerror("Erro", "Quantidade invalida,itens menor que 0")
        else:
            self.__name = value

    

    def toListable(self):
        return [self.__id, self.__name, self.__description, self.__quantity, ">"]
