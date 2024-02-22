from database import cur, conn


class CreateTables:
    """Первичне создание отсутствующих таблиц в базе"""

    @classmethod
    def create_tables(cls):

        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255),
                job_title TEXT ,
                email VARCHAR(100)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                status VARCHAR(25),
                deadline TIMESTAMP,
                parent_task INT,
                employee_id INT,
                FOREIGN KEY (parent_task) REFERENCES tasks(id),
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)

        conn.commit()
