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
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT 0
                 )
         """)
         self.conn.commit()

    def _create_time_stamp_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS time_stamp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id INTEGER NOT NULL REFERENCES worker(id),
                project_id INTEGER NOT NULL REFERENCES project(id),
                start_time TEXT NOT NULL,
                end_time TEXT
             )
     """)
     self.conn.commit()

    # ---------- worker ----------
    def add_worker(self, first_name, last_name, is_admin=False):
        self.conn.execute(
            "INSERT INTO worker (first_name, last_name, is_admin) VALUES (?, ?, ?)",
            (first_name, last_name, is_admin),
        )
        self.conn.commit()
        logger.info("Added Worker: %s", first_name last_name, street zip_code ort, position_admin)

    def get_all_workers(self):
        return self.conn.execute("SELECT id, first_name, last_name, is_admin FROM worker").fetchall()

    # ---------- project ----------
    def add_project(self, project_number, project_name):
        self.conn.execute(
            "INSERT INTO project (project_number, project_name) VALUES (?, ?)",
            (project_number, project_name),
        )
        self.conn.commit()

    def get_all_projects(self):
        return self.conn.execute("SELECT id, product_name, product_price FROM products").fetchall()

    def add_timestamp(self, worker_id, project_id, start_time, end_time=None):
        self.conn.execute(
            "INSERT INTO time_stamp (worker_id, project_id, start_time, end_time) VALUES (?, ?, ?, ?)",
            (worker_id, project_id, start_time, end_time),
        )
        self.conn.commit()





    def stamp(self, worker_id, project_id):
        """One button: stops the running stamp or starts a new one.
        Returns "started" or "stopped"."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running = self.conn.execute(
            "SELECT id, project_id FROM time_stamp WHERE worker_id = ? AND end_time IS NULL",
            (worker_id,),
        ).fetchone()

        if running is not None:
            # end the running stamp
            self.conn.execute(
                "UPDATE time_stamp SET end_time = ? WHERE id = ?", (now, running[0])
            )
            if running[1] == project_id:
                # same project -> just clock out
                self.conn.commit()
                return "stopped"

        # no running stamp, or a different project -> start a new one
        self.conn.execute(
            "INSERT INTO time_stamp (worker_id, project_id, start_time) VALUES (?, ?, ?)",
            (worker_id, project_id, now),
        )
        self.conn.commit()
        return "started"

    def get_all_timestamps(self):
        return self.conn.execute(
            "SELECT id, worker_id, project_id, start_time, end_time FROM time_stamp"
        ).fetchall()

    def close_db_conn(self):
        self.conn.close()
        