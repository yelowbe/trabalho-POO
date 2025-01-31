from tkinter import messagebox
from typing import List, Dict, Optional

class User:
    def __init__(self, name: str, password: str, permission: str, usersList: List[Dict[str, str]]) -> None:
        if len(name) == 0:
            messagebox.showerror("Erro", "Nome inválido")
            return
        elif len(password) == 0:
            messagebox.showerror("Erro", "Senha inválida")
            return
        elif any(user["name"] == name for user in usersList):
            messagebox.showerror("Erro", "Esse usuário já existe")
            return
        elif len(permission) == 0 or (permission != "leitura" and permission != "escrita"):
            messagebox.showerror("Erro", "Permissão inválida")
            return
        else:
            self.__usersList: List[Dict[str, str]] = usersList
            self.__name: str = name
            self.__password: str = password
            self.__permission: str = permission

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if len(value) == 0:
            messagebox.showerror("Erro", "Nome inválido")
            return
        elif any(user["name"] == value for user in self.__usersList):
            messagebox.showerror("Erro", "Esse usuário já existe")
            return
        else:
            self.__name = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        if len(value) == 0:
            messagebox.showerror("Erro", "Senha inválida")
            return
        else:
            self.__password = value

    @property
    def permission(self) -> str:
        return self.__permission

    @permission.setter
    def permission(self, value: str) -> None:
        if value == "leitura" or value == "escrita":
            self.__permission = value

    def toDict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "password": self.password,
            "permission": self.permission,
        }