from tkinter import *
from tkinter import ttk
from data_base import DataBase
from view import View
import numpy as np

FILE_PATH = "data_base.json"

if __name__ == "__main__":
    root = Tk()
    db = DataBase(FILE_PATH)
    dataSource = db.data

    if not ("users" in dataSource):
        dataSource["users"] = np.empty()

    if not ("storage" in dataSource):
        dataSource["storage"] = np.empty()
    
    if not ("num_itens_storage" in dataSource):
        # Usando numpy para contar os itens do storage
        dataSource["num_itens_storage"] = dataSource["storage"]

    if not ("rootPassword" in dataSource):
        dataSource["rootPassword"] = "1234"
    
    def onClose():
        db.save(FILE_PATH, dataSource)

    view = View(root, dataSource, onClose)

    view.renderLoginForm()
    root.mainloop()
