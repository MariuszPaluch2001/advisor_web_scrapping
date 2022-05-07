import sqlite3
from sqlite3 import OperationalError, ProgrammingError

class DB_Adapter:
    def __init__(self) -> None:
        self._db_objet = None

    def connect(self, db_name : str):
        self._db_objet = sqlite3.connect(db_name)

    def statement_without_param(self, statement : str):
        cur = self._db_objet.cursor()
        cur.execute(statement)
        res = cur.fetchall()
        cur.close()
        return res
    
    def statement_with_param(self, statement : str ,parameter):
        cur = self._db_objet.cursor()
        cur.execute(statement, parameter)
        res = cur.fetchall()
        cur.close()
        return res

    def statement_with_parameters(self, statement : str ,parameters):
        cur = self._db_objet.cursor()
        cur.executemany(statement, parameters)
        res = cur.fetchall()
        cur.close()
        return res
    
    def commit(self):
        self._db_objet.commit()
    
    def __close_connection(self):
        self._db_objet.close()

    def __del__(self):
        self.__close_connection()

if __name__ == "__main__":
    db = DB_Adapter()
    db.connect("database.db")

    db.statement_without_param("""
        CREATE TABLE laptops
               (price real, link text, screen text, CPU text, ram text, disc text, GPU text, OS text, time text)
    """)


    db.commit()
