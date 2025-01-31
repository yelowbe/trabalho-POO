import json
import os
from typing import Dict, Any
from exception import ExceptionDataBase


class DataBase:

    def __init__(self, file_path: str) -> None:
        """
        Inicializa a classe DataBase.

        :param file_path: Caminho do arquivo JSON que será usado como banco de dados.
        """
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({}, file)

        with open(file_path, "r") as file:
            try:
                self.data: Dict[str, Any] = json.load(file)
            except TypeError as e:
                raise TypeError(f"Erro ao ler o banco de dados: {e}")

    @staticmethod
    def save(file_path: str, data: Dict[str, Any]) -> None:
        """
        Salva os dados no arquivo JSON.

        :param file_path: Caminho do arquivo JSON.
        :param data: Dados a serem salvos no arquivo.
        :raises ExceptionDataBase: Se o arquivo não existir.
        """
        if not os.path.exists(file_path):
            raise ExceptionDataBase(file_path, data)

        with open(file_path, "w") as file:
            json.dump(data, file)