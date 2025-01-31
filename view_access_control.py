from abc import ABC, abstractmethod
from tkinter import simpledialog, messagebox
from typing import Callable, Any, Tuple

# Interface para controle de acesso
class IAccessControl(ABC):

    @abstractmethod
    def _verifyWritePermission(func: Callable[..., Any]) -> Callable[..., Any]:
        pass

    @abstractmethod
    def _validateRootPassword(func: Callable[..., Any]) -> Callable[..., Any]:
        pass


# Classe abstrata que implementa a interface
class ViewAccessControl(IAccessControl, ABC):

    def __init__(self, rootPassword):
        self.rootPassword = rootPassword

    # Implementação do decorador _verifyWritePermission
    def _verifyWritePermission(func):
        def wrapper(*args, permission):
            if permission == "leitura":
                messagebox.showerror("Erro", "Permissão negada!")
            else:
                func(*args, permission)

        return wrapper

    # Implementação do decorador _validateRootPassword
    def _validateRootPassword(func):
        def wrapper(self, name, password, permission):
            if permission == "escrita":
                passwordEntry = simpledialog.askstring(
                    "Senha", "Digite a senha do usuário root:", show="*"
                )

                if not (passwordEntry == self.rootPassword):
                    return messagebox.showerror("Erro", "Senha incorreta!")

            func(self, name, password, permission)

        return wrapper

    @abstractmethod
    def _cleanWindow(self):
        pass

    @abstractmethod
    def _closeWindow(self):
        pass
