from tkinter import messagebox
import json
from typing import Dict, Any

class ExceptionDataBase(Exception):
    def __init__(self, file_path: str, dataSource: Dict[str, Any]) -> None:
        """Armazenamento apagado durante a execução do programa"""
        messagebox.showerror("Erro", "Banco de dados apagado, recuperando dados...")        
        with open(file_path, "w") as file:
            json.dump({}, file)

        with open(file_path, "w") as file:
            json.dump(dataSource, file)
                               
        with open(file_path, "r") as file:
            try:
                self.data: Dict[str, Any] = json.load(file)
                
                if self.data["num_itens_storage"] == dataSource["num_itens_storage"]:
                    messagebox.showinfo("Sucesso", "Dados recuperados com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível recuperar todos os dados. :(")        
                
            except TypeError as e:
                raise TypeError(f"Erro ao ler o banco de dados: {e}") 
            
class ExceptionInvalidName(Exception):
    def __init__(self) -> None:
        """Nome inserido é invalido"""
        messagebox.showerror("Erro", "Nome inválido")

class ExceptionInvalidQuantity(Exception):
    def __init__(self) -> None:
        """Quantidade inválida (< 0)"""
        messagebox.showerror("Erro", "Quantidade é inválida")

class ExceptionProductDuplicity(Exception):
    def __init__(self) -> None:
        """Produto Existente"""
        messagebox.showerror("Erro", "Esse produto já existe")