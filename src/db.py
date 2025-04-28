import sqlite3


class DB:
    def __init__(self):
        self.db: str = "tasks_dev.db"
        self._create_tables()

    def _create_tables(self) -> None:
        con = sqlite3.connect(self.db)
        with con:
            con.executescript("""
                BEGIN;
                CREATE TABLE IF NOT EXISTS tasks(
                    id integer primary key autoincrement, 
                    CaseNumber INT,
                    title TEXT,
                    description TEXT, 
                    status TEXT, 
                    CreatedDate TEXT);
                COMMIT;
                """)
        return

    def get_tasks(self) -> list[dict]:
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        with con:
            res = con.execute(
                """
                SELECT * FROM tasks;
                """
            )
            return [dict(row) for row in res.fetchall()]

    def delete_task(self, data):
        con = sqlite3.connect(self.db)
        with con:
            con.execute(
                """
                delete from tasks where id = :id;
                """,
                data
            )
        return

    def create_tasks(self, data):
        con = sqlite3.connect(self.db)
        with con:
            con.execute(
                """
                insert into tasks
                values(:id, :CaseNumber, :title, :description, :status, :CreatedDate);
                """,
                data
            )
        return

    def update_task_case_number(self, id, case_num):
        con = sqlite3.connect(self.db)
        with con:
            con.execute(
                """
                update tasks
                set CaseNumber = :case_num 
                where id = :id;
                """,
                {
                    'id': id,
                    'case_num': case_num
                }
            )
        return

    def update_task_description(self, id, description):
        con = sqlite3.connect(self.db)
        with con:
            con.execute(
                """
                update tasks
                set description = :description 
                where id = :id;
                """,
                {
                    'id': id,
                    'description': description
                }
            )
        return
