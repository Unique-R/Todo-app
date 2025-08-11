from flask import Flask, render_template, request, redirect, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database=os.environ.get('POSTGRES_DB', 'todo_db'), # Изменение
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, task VARCHAR(255), completed BOOLEAN DEFAULT FALSE);')
    cur.execute('SELECT id, task, completed FROM todos;')
    tasks = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return render_template('index.html', tasks=tasks, editing_task_id=None)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task'].strip()
    if not task:
        flash('Task cannot be empty!')
        return redirect('/')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (task) VALUES (%s);', (task,))
    cur.close()
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = %s;', (id,))
    cur.close()
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        task = request.form['task'].strip()
        if not task:
            flash('Task cannot be empty!')
            cur.execute('SELECT id, task, completed FROM todos;')
            tasks = cur.fetchall()
            cur.close()
            conn.commit()
            conn.close()
            return render_template('index.html', tasks=tasks, editing_task_id=id)
        cur.execute('UPDATE todos SET task = %s WHERE id = %s;', (task, id))
        cur.close()
        conn.commit()
        conn.close()
        return redirect('/')
    cur.execute('SELECT id, task, completed FROM todos WHERE id = %s;', (id,))
    task = cur.fetchone()
    cur.execute('SELECT id, task, completed FROM todos;')
    tasks = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return render_template('index.html', tasks=tasks, editing_task_id=id)

@app.route('/health')
def health_check():
    return 'OK', 200


@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT completed FROM todos WHERE id = %s;', (id,))
    current_status = cur.fetchone()[0]
    cur.execute('UPDATE todos SET completed = NOT %s WHERE id = %s;', (current_status, id))
    cur.close()
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
