import json
import os
from exception import ExceptionDataBase


class DataBase:

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({}, file)

        with open(file_path, "r") as file:
            try:
                self.data = json.load(file)
                
            except TypeError as e:
                    raise TypeError(f"Erro ao ler o banco de dados: {e}")
            

    @staticmethod
    def save(file_path, data):
        
        if not os.path.exists(file_path):            
            raise ExceptionDataBase(file_path,data)
        
        else:
            with open(file_path, "w") as file:
                json.dump(data, file)        