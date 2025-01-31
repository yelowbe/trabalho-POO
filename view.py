from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from storage import Storage
from user_manager import UserManager
from view_access_control import ViewAccessControl

from permissions_list import permissions

# Hexadecimal das cores utilizadas
black = "#00000f"
white = "#feffff"
green = "#4fa882"
darkBlue = "#38576b"
blue = "#038cfc"
red = "#ef5350"
darkGreen = "#263238"
lightBlue = "#e9edf5"
darkOrange = "#ff8c00"


class View(ViewAccessControl):

    def __init__(self, root, dataSource, onClose):
        self.usersManager = UserManager(dataSource["users"])
        self.storage = Storage(dataSource)
        self.rootPassword = dataSource["rootPassword"]

        self.onClose = onClose

        self.root = root
        self.root.title("Gerenciador de estoque")
        self.root.geometry("1043x453")
        self.root.configure(background=white)
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self._closeWindow)

    # métodos privados
    def _cleanWindow(self):
        for child in self.root.winfo_children():
            child.destroy()

    def _closeWindow(self):
        self.onClose()
        self.root.destroy()

    @ViewAccessControl._validateRootPassword
    def __addUser(self, name, password, permission):
        self.usersManager.addUser(name, password, permission, self.renderLoginForm)

    @ViewAccessControl._verifyWritePermission
    def __addProduct(self, name, description, quantity, permission):
        self.storage.addProduct(name, description, quantity, action=self.renderHome)

    @ViewAccessControl._verifyWritePermission
    def __editProduct(self, id, name, description, quantity, permission):
        self.storage.editProduct(id, name, description, quantity, self.renderHome)

    @ViewAccessControl._verifyWritePermission
    def __deleteProduct(self, name, permission):
        self.storage.deleteProduct(name, self.renderHome)

    # métodos públicos
    def renderHome(self):
        # limpar a janela principal
        self._cleanWindow()

        # construção do header
        homeHeader = Frame(
            self.root, width=770, height=50, bg=darkOrange, relief="flat"
        )
        homeHeader.grid(row=0, column=0)
        headerLabel = Label(
            homeHeader,
            text="Gerenciador de estoque",
            font="Roboto 13 bold",
            bg=darkOrange,
            fg=white,
            relief="flat",
        )
        headerLabel.place(x=10, y=10)

        homeNav = Frame(self.root, width=273, height=50, bg=darkOrange, relief="flat")
        homeNav.grid(row=0, column=1)

        editClientButton = Button(
            homeNav,
            text="Editar usuário",
            width=15,
            font="Roboto 8 bold",
            bg=white,
            fg=black,
            relief="raised",
            overrelief="ridge",
            command=self.renderEditUserForm,
        )
        editClientButton.place(x=0, y=15)

        createProductButton = Button(
            homeNav,
            text="Novo produto",
            width=15,
            font="Roboto 8 bold",
            bg=white,
            fg=black,
            relief="raised",
            overrelief="ridge",
            command=self.renderProductForm,
        )
        createProductButton.place(x=135, y=15)

        # corpo principal da tabela
        homeMain = Frame(self.root, width=1043, height=403, bg=white, relief="flat")
        homeMain.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # configura a tabela para preencher todo o espaço disponível
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        homeMain.grid_rowconfigure(0, weight=1)
        homeMain.grid_columnconfigure(0, weight=1)

        # inicia a tabela e o scroll vertical
        tableHead = ["ID", "Nome", "Descrição", "Quantidade", ""]
        table = ttk.Treeview(
            homeMain, selectmode="extended", columns=tableHead, show="headings"
        )
        vsb = ttk.Scrollbar(homeMain, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=vsb.set)
        table.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")

        # estilização da tabela
        wd = [
            "nw",
            "nw",
            "nw",
            "center",
            "ne",
        ]
        w = [40, 280, 480, 100, 5]
        n = 0

        # insere os itens na tabela
        for col in tableHead:
            table.heading(col, text=col.title(), anchor=CENTER)
            table.column(col, width=w[n], anchor=wd[n])
            n += 1

        def generate_items(items):
            for index, item in enumerate(items):
                if index % 2 == 0:
                    yield item, "even", index
                else:
                    yield item, "odd", index

        for item, tag, index in generate_items(self.storage.items):
            table.insert("", "end", values=item, tags=(tag,), iid=index)

        # evento de clique em cada linha
        table.bind(
            "<<TreeviewSelect>>",
            lambda *args: self.renderEditProductForm(int(table.focus())),
        )

        # Configurando as cores para as tags
        table.tag_configure("even", background=lightBlue)
        table.tag_configure("odd", background=white)

    def renderProductForm(self):

        # limpar a janela principal
        self._cleanWindow()

        # cabeçalho do formulário
        formHeader = Frame(self.root, width=1043, height=50, bg="green", relief="flat")
        formHeader.grid(row=0, column=0)
        formHeader.pack_propagate(False)

        headerLabel = Label(
            formHeader,
            text="Criação de Produto",
            font="Roboto 13 bold",
            bg="green",
            fg="white",
            relief="flat",
        )
        headerLabel.pack(expand=True)

        # Corpo principal do formulário
        formMain = Frame(self.root, width=1043, height=403, bg="white", relief="flat")
        formMain.grid(row=1, column=0, sticky="nsew", pady=(0, 20), padx=40)
        formMain.grid_propagate(False)

        Label(formMain, text="Nome:", font="Roboto 8 bold", bg="white").grid(
            row=0, column=0, sticky="w", pady=15
        )
        nameEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        nameEntry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        Label(formMain, text="Descrição:", font="Roboto 8 bold", bg="white").grid(
            row=1, column=0, sticky="nw", pady=15
        )
        descricao_text = Text(
            formMain, font="Roboto 8 bold", width=50, height=10, relief="solid"
        )
        descricao_text.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        Label(formMain, text="Quantidade:", font="Roboto 8 bold", bg="white").grid(
            row=2, column=0, sticky="w", pady=15
        )

        def generate_quantities(start, end):
            for quantity in range(start, end + 1):
                yield quantity

        quantities = list(generate_quantities(0, 100))
        quantidade_spin = Spinbox(
            formMain, values=quantities, font="Roboto 8 bold", width=10, relief="solid"
        )
        quantidade_spin.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        buttonsFrame = Frame(formMain, bg="white", relief="flat")
        buttonsFrame.grid(row=3, column=0, pady=20, padx=40, columnspan=2)

        return_button = Button(
            buttonsFrame,
            text="Voltar",
            font="Roboto 8 bold",
            bg="black",
            fg="white",
            width=15,
            command=self.renderHome,
            relief="raised",
            overrelief="ridge",
        )
        return_button.grid(row=0, column=0, pady=20, padx=4)

        submit_button = Button(
            buttonsFrame,
            text="Continuar",
            font="Roboto 8 bold",
            bg="green",
            fg="white",
            width=15,
            command=lambda: self.__addProduct(
                nameEntry.get(),
                descricao_text.get("1.0", "end").strip(),
                int(quantidade_spin.get()),
                permission=self.usersManager.authenticatedUser["permission"],
            ),
            relief="raised",
            overrelief="ridge",
        )
        submit_button.grid(row=0, column=1, pady=20, padx=4)

    def renderEditProductForm(self, id):
        # Deleta o produto atual
        def deleteProduct():
            name = nameEntry.get()
            confirmation = messagebox.askyesno(
                "Confirmação", "Tem certeza que deseja continuar?"
            )

            if confirmation:
                self.__deleteProduct(
                    name, permission=self.usersManager.authenticatedUser["permission"]
                )
            else:
                messagebox.showinfo("Cancelado", "Ação cancelada!")

        # Limpar a janela principal
        self._cleanWindow()

        # Cabeçalho do formulário
        formHeader = Frame(self.root, width=1043, height=50, bg="green", relief="flat")
        formHeader.grid(row=0, column=0)
        formHeader.pack_propagate(False)

        headerLabel = Label(
            formHeader,
            text="Criação de Produto",
            font="Roboto 13 bold",
            bg="green",
            fg="white",
            relief="flat",
        )
        headerLabel.pack(expand=True)

        # Corpo principal do formulário
        formMain = Frame(self.root, width=1043, height=403, bg="white", relief="flat")
        formMain.grid(row=1, column=0, sticky="nsew", pady=(0, 20), padx=40)
        formMain.grid_propagate(False)

        Label(formMain, text="Nome:", font="Roboto 8 bold", bg="white").grid(
            row=0, column=0, sticky="w", pady=15
        )
        nameEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        nameEntry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        # Campo para Descrição (caixa de texto maior)
        Label(formMain, text="Descrição:", font="Roboto 8 bold", bg="white").grid(
            row=1, column=0, sticky="nw", pady=15
        )
        descricao_text = Text(
            formMain, font="Roboto 8 bold", width=50, height=10, relief="solid"
        )
        descricao_text.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Campo para Contador (Spinbox)
        Label(formMain, text="Quantidade:", font="Roboto 8 bold", bg="white").grid(
            row=2, column=0, sticky="w", pady=15
        )

        def generate_quantities(start, end):
            for quantity in range(start, end + 1):
                yield quantity

        quantities = list(generate_quantities(0, 100))
        quantidade_spin = Spinbox(
            formMain, values=quantities, font="Roboto 8 bold", width=10, relief="solid"
        )
        quantidade_spin.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        buttonsFrame = Frame(formMain, bg="white", relief="flat")
        buttonsFrame.grid(row=3, column=0, pady=20, padx=40, columnspan=2)

        return_button = Button(
            buttonsFrame,
            text="Voltar",
            font="Roboto 8 bold",
            bg="black",
            fg="white",
            width=15,
            relief="raised",
            overrelief="ridge",
            command=self.renderHome,
        )
        return_button.grid(row=0, column=0, pady=20, padx=4)

        submit_button = Button(
            buttonsFrame,
            text="Continuar",
            font="Roboto 8 bold",
            bg="green",
            fg="white",
            width=15,
            command=lambda: self.__editProduct(
                id,
                nameEntry.get(),
                descricao_text.get("1.0", "end").strip(),
                int(quantidade_spin.get()),
                permission=self.usersManager.authenticatedUser["permission"],
            ),
            relief="raised",
            overrelief="ridge",
        )
        submit_button.grid(row=0, column=2, pady=20, padx=4)

        delete_button = Button(
            buttonsFrame,
            text="Deletar",
            font="Roboto 8 bold",
            bg="red",
            fg="white",
            width=15,
            command=deleteProduct,
            relief="raised",
            overrelief="ridge",
        )
        delete_button.grid(row=0, column=3, pady=20, padx=4)

        # Preenche o formulário
        nameEntry.insert(0, self.storage.items[id][1])
        descricao_text.insert("1.0", self.storage.items[id][2])
        quantidade_spin.delete(0, "end")
        quantidade_spin.insert(0, self.storage.items[id][3])

    def renderEditUserForm(self):
        # Deleta o usuário logado
        def deleteUser():
            confirmation = messagebox.askyesno(
                "Confirmação", "Tem certeza que deseja continuar?"
            )

            if confirmation:
                self.usersManager.deleteUser(self.renderLoginForm)
            else:
                messagebox.showinfo("Cancelado", "Ação cancelada!")

        # Limpar a janela principal
        self._cleanWindow()

        # Costrução do header
        formHeader = Frame(self.root, width=1043, height=50, bg=darkBlue, relief="flat")
        formHeader.grid(row=0, column=0)
        formHeader.pack_propagate(False)

        headerLabel = Label(
            formHeader,
            text="Editar usuário",
            font="Roboto 13 bold",
            bg=darkBlue,
            fg="white",
            relief="flat",
        )
        headerLabel.pack(expand=True)

        # Corpo principal do formulário
        formMain = Frame(self.root, width=1043, height=403, bg="white", relief="flat")
        formMain.grid(row=1, column=0, sticky="nsew", pady=(20, 40))
        formMain.grid_propagate(False)

        Label(formMain, text="Nome:", font="Roboto 8 bold", bg="white").grid(
            row=0, column=0, sticky="w", pady=15, padx=(40, 0)
        )
        nameEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        nameEntry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        Label(formMain, text="Senha:", font="Roboto 8 bold", bg="white").grid(
            row=1, column=0, sticky="w", pady=15, padx=(40, 0)
        )
        passwordEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        passwordEntry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        buttonsFrame = Frame(formMain, bg="white", relief="flat")
        buttonsFrame.grid(row=3, column=0, pady=20, padx=40, columnspan=2)

        submit_button = Button(
            buttonsFrame,
            text="Voltar",
            font="Roboto 8 bold",
            bg="black",
            fg="white",
            width=15,
            command=self.renderHome,
            relief="raised",
            overrelief="ridge",
        )
        submit_button.grid(row=0, column=0, pady=20, padx=4)

        return_button = Button(
            buttonsFrame,
            text="Continuar",
            font="Roboto 8 bold",
            bg="green",
            fg="white",
            width=15,
            command=lambda: self.usersManager.editUser(
                nameEntry.get(), passwordEntry.get(), self.renderHome
            ),
            relief="raised",
            overrelief="ridge",
        )
        return_button.grid(row=0, column=2, pady=20, padx=4)

        delete_button = Button(
            buttonsFrame,
            text="Deletar",
            font="Roboto 8 bold",
            bg="red",
            fg="white",
            width=15,
            command=deleteUser,
            relief="raised",
            overrelief="ridge",
        )
        delete_button.grid(row=0, column=3, pady=20, padx=4)

        # insere os valores do usuário autenticado
        nameEntry.insert(0, self.usersManager.authenticatedUser["name"])
        passwordEntry.insert(0, self.usersManager.authenticatedUser["password"])

    def renderLoginForm(self):
        # Limpar a janela principal
        self._cleanWindow()

        # Construção do header
        formHeader = Frame(self.root, width=1043, height=50, bg=darkBlue, relief="flat")
        formHeader.grid(row=0, column=0)
        formHeader.pack_propagate(False)

        headerLabel = Label(
            formHeader,
            text="Entrar",
            font="Roboto 13 bold",
            bg=darkBlue,
            fg="white",
            relief="flat",
        )
        headerLabel.pack(expand=True)

        # Corpo principal do formulário
        formMain = Frame(self.root, width=1043, height=403, bg="white", relief="flat")
        formMain.grid(row=1, column=0, sticky="nsew", pady=(20, 40))
        formMain.grid_propagate(False)

        Label(formMain, text="Nome:", font="Roboto 8 bold", bg="white").grid(
            row=0, column=0, sticky="w", pady=15, padx=(40, 0)
        )
        nameEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        nameEntry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        Label(formMain, text="Senha:", font="Roboto 8 bold", bg="white").grid(
            row=1, column=0, sticky="w", pady=15, padx=(40, 0)
        )
        passwordEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        passwordEntry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        buttonsFrame = Frame(formMain, bg="white", relief="flat")
        buttonsFrame.grid(row=3, column=0, pady=20, padx=40, columnspan=2)

        submit_button = Button(
            buttonsFrame,
            text="Criar Usuário",
            font="Roboto 8 bold",
            bg=darkBlue,
            fg="white",
            width=15,
            command=self.renderCreateUserForm,
            relief="raised",
            overrelief="ridge",
        )
        submit_button.grid(row=0, column=0, pady=20, padx=4)

        return_button = Button(
            buttonsFrame,
            text="Continuar",
            font="Roboto 8 bold",
            bg="green",
            fg="white",
            width=15,
            command=lambda: self.usersManager.loginUser(
                nameEntry.get(), passwordEntry.get(), self.renderHome
            ),
            relief="raised",
            overrelief="ridge",
        )
        return_button.grid(row=0, column=2, pady=20, padx=4)

    def renderCreateUserForm(self):
        # limpar a janela principal
        self._cleanWindow()

        # construção do header
        formHeader = Frame(self.root, width=1043, height=50, bg=darkBlue, relief="flat")
        formHeader.grid(row=0, column=0)
        formHeader.pack_propagate(False)
        headerLabel = Label(
            formHeader,
            text="Criar usuário",
            font="Roboto 13 bold",
            bg=darkBlue,
            fg="white",
            relief="flat",
        )
        headerLabel.pack(expand=True)

        # Corpo principal do formulário
        formMain = Frame(self.root, width=1043, height=403, bg="white", relief="flat")
        formMain.grid(row=1, column=0, sticky="nsew", pady=(20, 40))
        formMain.grid_propagate(False)

        Label(formMain, text="Nome:", font="Roboto 8 bold", bg="white").grid(
            row=0, column=0, sticky="w", pady=15, padx=(40, 0)
        )
        nameEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        nameEntry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        Label(formMain, text="Senha:", font="Roboto 8 bold", bg="white").grid(
            row=1, column=0, sticky="w", pady=15, padx=(40, 0)
        )
        passwordEntry = Entry(
            formMain,
            textvariable=StringVar(),
            font="Roboto 8 bold",
            width=50,
            relief="solid",
        )
        passwordEntry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        Label(formMain, text="Permissão: ", font="Roboto 8 bold", bg="white").grid(
            row=2, column=0, sticky="w", pady=15, padx=(40, 0)
        )

        options = permissions()
        comboPermission = ttk.Combobox(formMain, values=options)
        comboPermission.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        comboPermission.set("Selecione uma opção")

        buttonsFrame = Frame(formMain, bg="white", relief="flat")
        buttonsFrame.grid(row=3, column=0, pady=20, padx=40, columnspan=2)
        return_button = Button(
            buttonsFrame,
            text="Voltar",
            font="Roboto 8 bold",
            bg="black",
            fg="white",
            width=15,
            command=self.renderLoginForm,
            relief="raised",
            overrelief="ridge",
        )
        return_button.grid(row=0, column=0, pady=20, padx=4)
        submit_button = Button(
            buttonsFrame,
            text="Continuar",
            font="Roboto 8 bold",
            bg="green",
            fg="white",
            width=15,
            command=lambda: self.__addUser(
                nameEntry.get(), passwordEntry.get(), comboPermission.get()
            ),
            relief="raised",
            overrelief="ridge",
        )
        submit_button.grid(row=0, column=2, pady=20, padx=4)