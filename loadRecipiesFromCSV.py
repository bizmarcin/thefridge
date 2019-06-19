import  sqlite3
import csv

from database import  database

def get_connection(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_connection('fridge.db')
cursor = conn.cursor()

database.execute_sql_script('db_init_recipies.sql', conn.cursor())

with open('static\\csv\\recipes.csv','r') as f:
    for line in f:
        reader = csv.reader(f)
        data = next(reader)
        query = 'insert into recipies values ({0})'
        query = query.format(','.join('?' * (len(data)+1)))
        cursor = conn.cursor()
        final_data = []
        final_data.append(None)
        for item in data:
            final_data.append(item)
        cursor.execute(query, final_data )
        for data in reader:
            final_data = []
            final_data.append(None)
            for item in data:
                final_data.append(item)
            cursor.execute(query, final_data)

        conn.commit()


conn.rollback()
conn.close()