class database():
    def execute_sql_script(querry, conn):
        with open(querry, encoding='utf-8') as f:
            querry = f.read()
        conn.executescript(querry)