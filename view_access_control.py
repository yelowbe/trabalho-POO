from tkinter import simpledialog, messagebox


class ViewAccessControl:

    # decoradores
    def _verifyWritePermission(func):
        def wrapper(*args, permission):
            if permission == "leitura":
                messagebox.showerror("Erro", "Permissão negada!")
            else:
                func(*args, permission)

        return wrapper

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
