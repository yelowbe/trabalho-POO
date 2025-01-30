from tkinter import *
from tkinter import ttk
from data_base import DataBase
from view import View

FILE_PATH = "data_base.json"

if __name__ == "__main__":
    root = Tk()
    db = DataBase(FILE_PATH)
    dataSource = db.data

    if not ("users" in dataSource):
        dataSource["users"] = []

    if not ("storage" in dataSource):
        dataSource["storage"] = []
    
    if not ("num_itens_storage" in dataSource):
        dataSource["num_itens_storage"] = len(dataSource["storage"])

    if not ("rootPassword" in dataSource):
        dataSource["rootPassword"] = "1234"
    

    def onClose():
        db.save(FILE_PATH, dataSource)

    view = View(root, dataSource, onClose)

    view.renderLoginForm()
    root.mainloop()
