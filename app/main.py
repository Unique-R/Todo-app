from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="todo_db",
        user="igor",
        password="password"
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, task VARCHAR(255));')
    cur.execute('SELECT task FROM todos;')
    tasks = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return f'Hello, this is a ToDo App! IGOR<br>Tasks: {tasks}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

