from tkinter import messagebox
import json


class ExceptionDataBase(Exception):
    def __init__(self,file_path,dataSource):
        
        messagebox.showerror("Erro", "Banco de dados apagado,recuperando dados...")        
        with open(file_path, "w") as file:
                json.dump({}, file)

        with open(file_path, "w") as file:
                json.dump(dataSource, file)
                
            
        
        
                
                
        
                
        
        

