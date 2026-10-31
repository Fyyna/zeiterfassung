import sqlite3
import logging

logger = logging.getLogger(__name__)


class DB_HANDLER:
    def __init__(self, path="time_clock.db"):
        self.conn = sqlite3.connect(path)
        self._create_project_table()
        self._create_worker_table()



    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS project (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_number TEXT NOT NULL UNIQUE,
                project_name TEXT NOT NULL
            )
        """)
        self.conn.commit()


    def _create_worker_table(self):
         self.conn.execute("""
             CREATE TABLE IF NOT EXISTS worker (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name VARCHAR(50),
                 last_name VARCHAR(50),
                 street VARCHAR(50),
                 zip_code CHAR(4),
                 ort VARCHAR(50)
                 position_admin BOOLEAN
                 )
         """)
         self.conn.commit()

    def _create_time_stamp_table(self):
     self.conn.execute("""
         CREATE TABLE IF NOT EXISTS time_stamp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER FOREIGN KEY NOT NULL,
            project_id INTEGER FOREIGN KEY NOT NULL,
            begin DATETIME NOT NULL,
            end DATETIME,


             )
     """)
     self.conn.commit()

    def add_worker(self,first_name: str, last_name: str, street: str, zip_code: int, ort: str, position_admin: bool):
        self.conn.execute(
            "INSERT INTO worker (first_name, last_name, street, zip_code, ort, position_admin)VALUES(?, ?, ?, ?, ?, ?)", (first_name, last_name, street,zip_code, ort, position_admin)
        )
        self.conn.commit()
        logger.info("Added Worker: %s", first_name last_name, street zip_code ort, position_admin)



    def add_project(self,project_name: str ):
        self.conn.execute(
                    "INSERT INTO project (project_name)VALUES(?)", (project_name)
                )

    def add_timestamp():
        



    def get_all_products(self):
        return self.conn.execute("SELECT id, product_name, product_price FROM products").fetchall()

    def get_time(self, id: int):
        return self.conn.execute("SELECT id, product_name, product_price FROM products WHERE id = ?", (id,)).fetchone()

    def show_all_workers(self):
        for id, product_name, product_price in self.get_all_products():
            print(f"{id}, {product_name}: {product_price} CHF")

    def close_db_conn(self):
        self.conn.close()
        