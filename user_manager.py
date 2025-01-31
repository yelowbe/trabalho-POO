from tkinter import messagebox
from typing import List, Dict, Optional, Callable
from user import User


class UserManager:
    def __init__(self, users: List[Dict[str, str]] = []) -> None:
        self.__users: List[Dict[str, str]] = users
        self.authenticatedUser: Optional[Dict[str, str]] = None

    # decoradores
    def authenticateUser(func: Callable) -> Callable:
        def wrapper(self: 'UserManager', name: str, password: str, action: Callable) -> Optional[bool]:
            user: Optional[Dict[str, str]] = next((user for user in self.__users if user["name"] == name), None)

            if user:
                if user["password"] == password:
                    return func(self, name, password, action)
                else:
                    messagebox.showerror("Erro", "Nome ou Senha inválidos")
                    return None
            else:
                messagebox.showerror("Erro", "Nome ou Senha inválidos")
                return None

        return wrapper

    def canEditUser(func: Callable) -> Callable:
        def wrapper(self: 'UserManager', name: str, password: str, action: Callable) -> Optional[bool]:
            if len(name) == 0:
                messagebox.showerror("Erro", "Nome inválido")
                return None
            elif len(password) == 0:
                messagebox.showerror("Erro", "Senha inválida")
                return None
            elif any(user["name"] == name for user in self.__users):
                if name != self.authenticatedUser["name"]:
                    messagebox.showerror("Erro", "Esse usuário já existe")
                    return None

            return func(self, name, password, action)

        return wrapper

    # métodos
    @property
    def users(self) -> List[Dict[str, str]]:
        return self.__users

    def addUser(self, name: str, password: str, permission: str, action: Callable) -> None:
        newUser: User = User(name, password, permission, self.__users)
        self.__users.append(newUser.toDict())
        messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
        action()

    @authenticateUser
    def loginUser(self, name: str, password: str, action: Callable) -> None:
        self.authenticatedUser = next((user for user in self.__users if user["name"] == name))
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        action()

    @canEditUser
    def editUser(self, name: str, password: str, action: Callable) -> None:
        newAuthenticatedUser: Dict[str, str] = self.authenticatedUser
        newAuthenticatedUser["name"] = name
        newAuthenticatedUser["password"] = password

        authenticatedIndex: int = next(
            (i for i, user in enumerate(self.__users) if user["name"] == self.authenticatedUser["name"])
        )
        self.__users[authenticatedIndex] = newAuthenticatedUser
        self.authenticatedUser = newAuthenticatedUser

        messagebox.showinfo("Sucesso", "Usuário editado com sucesso!")
        action()

    def deleteUser(self, action: Callable) -> None:
        authenticatedIndex: int = next(
            (i for i, user in enumerate(self.__users) if user["name"] == self.authenticatedUser["name"])
        )
        self.__users.pop(authenticatedIndex)
        self.authenticatedUser = None

        messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")
        action()