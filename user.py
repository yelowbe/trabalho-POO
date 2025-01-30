from tkinter import messagebox


class User:

    def __init__(self, name, password, permission, usersList):
        if len(name) == 0:
            return messagebox.showerror("Erro", "Nome inválido")
        elif len(password) == 0:
            return messagebox.showerror("Erro", "Senha inválida")
        elif any(user["name"] == name for user in usersList):
            return messagebox.showerror("Erro", "Esse usuário já existe")
        elif len(permission) == 0 or (
            permission != "leitura" and permission != "escrita"
        ):
            return messagebox.showerror("Erro", "Permissão inválida")
        else:
            self.__usersList = usersList
            self.__name = name
            self.__password = password
            self.__permission = permission

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) == 0:
            return messagebox.showerror("Erro", "Nome inválido")
        elif any(user["name"] == value for user in self.__usersList):
            return messagebox.showerror("Erro", "Esse usuário já existe")
        else:
            self.__name = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value) == 0:
            return messagebox.showerror("Erro", "Senha inválida")
        else:
            self.__password = value

    @property
    def permission(self):
        return self.__permission

    @permission.setter
    def permission(self, value):
        if value == "leitura" or value == "escrita":
            self.__permission = value

    def toDict(self):
        return {
            "name": self.name,
            "password": self.password,
            "permission": self.permission,
        }
