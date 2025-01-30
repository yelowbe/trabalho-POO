from tkinter import messagebox
from user import User


class UserManager:
    def __init__(self, users=[]):
        self.__users = users
        self.authenticatedUser = None

    # decoradores
    def authenticateUser(func):
        def wrapper(self, name, password, action):
            # retorna o primeiro user da lista que atende à condição user["name"] == name.
            # caso nenhum usuário seja encontrado, retorna None (definido como valor padrão).
            user = next((user for user in self.__users if user["name"] == name), None)

            if user:
                if user["password"] == password:
                    return func(self, name, password, action)
                else:
                    return messagebox.showerror("Erro", "Nome ou Senha inválidos")
            else:
                return messagebox.showerror("Erro", "Nome ou Senha inválidos")

        return wrapper

    def canEditUser(func):
        def wrapper(self, name, password, action):

            if len(name) == 0:
                return messagebox.showerror("Erro", "Nome inválido")
            elif len(password) == 0:
                return messagebox.showerror("Erro", "Senha inválida")
            elif any(user["name"] == name for user in self.__users):
                if name != self.authenticatedUser["name"]:
                    return messagebox.showerror("Erro", "Esse usuário já existe")

            func(self, name, password, action)

        return wrapper

    # métodos
    @property
    def users(self):
        return self.__users

    def addUser(self, name, password, permission, action):
        newUser = User(name, password, permission, self.__users)
        self.__users.append(newUser.toDict())
        messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
        action()

    @authenticateUser
    def loginUser(self, name, password, action):
        self.authenticatedUser = next(
            (user for user in self.__users if user["name"] == name)
        )
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        action()

    @canEditUser
    def editUser(self, name, password, action):
        newAuthenticatedUser = self.authenticatedUser
        newAuthenticatedUser["name"] = name
        newAuthenticatedUser["password"] = password

        authenticatedIndex = next(
            (
                i
                for i, user in enumerate(self.__users)
                if user["name"] == self.authenticatedUser["name"]
            )
        )
        self.__users[authenticatedIndex] = newAuthenticatedUser
        self.authenticatedUser = newAuthenticatedUser

        messagebox.showinfo("Sucesso", "Usuário editado com sucesso!")
        action()

    def deleteUser(self, action):
        authenticatedIndex = next(
            (
                i
                for i, user in enumerate(self.__users)
                if user["name"] == self.authenticatedUser["name"]
            )
        )
        self.__users.pop(authenticatedIndex)
        self.authenticatedUser = None

        messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")
        action()
