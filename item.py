from tkinter import messagebox
from typing import List, Tuple, Any
from exception import ExceptionInvalidName, ExceptionInvalidQuantity, ExceptionProductDuplicity


class Item:

    def __init__(self, id: int, name: str, description: str, quantity: int, items: List[Tuple[int, str, str, int]]) -> None:
        if len(name) == 0:
            raise ExceptionInvalidName()
        elif quantity < 1 or not isinstance(quantity, int):
            raise ExceptionInvalidQuantity()
        elif any(item[1] == name for item in items):
            raise ExceptionProductDuplicity()
        else:
            self.__id: int = id
            self.__name: str = name
            self.__description: str = description
            self.__quantity: int = quantity
            self.__items: List[Tuple[int, str, str, int]] = items

    @property
    def name(self) -> str:
        """
        Retorna o nome do item.

        :return: Nome do item.
        """
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        Define o nome do item.

        :param value: Novo nome do item.
        """
        if len(value) == 0:
            messagebox.showerror("Erro", "Nome inválido")
        elif any(item[1] == value for item in self.__items):
            messagebox.showerror("Erro", "Esse produto já existe")
        else:
            self.__name = value

    @property
    def quantity(self) -> int:
        """
        Retorna a quantidade do item.

        :return: Quantidade do item.
        """
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """
        Define a quantidade do item.

        :param value: Nova quantidade do item.
        """
        if value < 1 or not isinstance(value, int):
            messagebox.showerror("Erro", "Quantidade inválida")
        else:
            self.__quantity = value

    def toListable(self) -> List[Any]:
        """
        Converte o item em uma lista para exibição.

        :return: Lista contendo os detalhes do item.
        """
        return [self.__id, self.__name, self.__description, self.__quantity, ">"]