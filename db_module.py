import sqlite3
from sqlite3 import OperationalError, ProgrammingError

class DB_Adapter:
    def __init__(self) -> None:
        self._db_objet = None

    def connect(self, db_name : str):
        self._db_objet = sqlite3.connect(db_name)

    def statement(self, statement : str ,parameters = None):
        cur = self._db_objet.cursor()
        if parameters is None:
            try:
                cur.execute(statement)
            except OperationalError as e:
                print(e)
        elif type(parameters) == tuple:
            try:
                cur.execute(statement, parameters)
            except OperationalError as e:
                print(e)
        elif type(parameters) == list :
            try:
                cur.executemany(statement, parameters)
            except ProgrammingError as e:
                print(e)

        
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

    db.statement("""
        CREATE TABLE laptops
               (price real, link text, screen text, CPU text, ram text, disc text, GPU text, OS text)
    """)


    db.commit()
