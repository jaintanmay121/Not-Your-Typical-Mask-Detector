import psycopg2
from CONFIG import *

class Database:

    def __init__(self, database=database, user=user, password=password, table=table):
        """
        Initialize the class with the parameters required to connect to databse.\n
        Inputs:

            database: Name of the databse to which we need to connect.
            user: name of the user of the databse.
            password: password for the databse.
            table: name of the table to use.
        """
        self.database=database
        self.user=user
        self.password=password
        self.table=table

        connect_str = f"dbname={self.database} user={self.user} password={self.password}"
        
        try:
            self.conn = psycopg2.connect(connect_str)
            self.cursor = self.conn.cursor()
            print(f"\nConnected to {self.database}-->{self.table}\n")
        except Exception as e:
            print(e)


    def alter_size(self, col, new_size):
        """
        Alters the size of a column.\n
        Inputs:

            col: Name of column to be altered.
            new_size: New size of the column.
        """
        self.cursor.execute(f"ALTER TABLE {self.table} ALTER COLUMN {col} TYPE {new_size};")


    def alter_type(self, col, new_type):
        """
        Alters the data type of a column.\n
        Inputs:

            col: Name of column to be altered.
            old_type: Current data type of the column.
            new_type: New data type of the column.
        """
        self.cursor.execute(f"ALTER TABLE {self.table} ALTER COLUMN {col} TYPE {new_type};")#USING {col}::{new_type}""")


    def insert(self, values):
        """
        Insert a new row in the table.\n
        Inputs:

            values: Insert values according to the table in form of a list
                    in the format (id, name, mail) or (id, name, mail).
        """
        self.cursor.execute(f"INSERT INTO {self.table}(id, name, mail) VALUES({values[0]}, '{values[1]}', '{values[2]}', '{values[3]}');")

    def delete(self, query):
        """
        Deletes a row from a column.\n\n
        Inputs:

            query:  Provide the query for the row to be deleted.\n
                    Example: "id=0"
        """
        self.cursor.execute(f"DELETE FROM {self.table} WHERE {query};")


    def show_all(self):
        """
        Displays the entire table.
        """
        self.cursor.execute(f"SELECT * from {self.table};")
        print(self.cursor.fetchall())


    def show(self, query='', columns="*", get=False):
        """
        Displays the entire table.
        Inputs:
        
            query: Input the WHERE condition.
            columns: The columns to be displayed.
            get: return if True else print()
        """
        if query:
            self.cursor.execute(f"SELECT {columns} from {self.table} WHERE {query};")
        else:
            self.cursor.execute(f"SELECT {columns} from {self.table};")
        if get:
            return self.cursor.fetchall()[0]
        else:
            print(self.cursor.fetchall()[0])
    

    def close(self):
        """Call this function to finally close the connection at the end of all queries.
        """
        self.conn.commit()
        
        self.cursor.close()
        self.conn.close()