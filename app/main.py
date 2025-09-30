from flask import Flask, render_template, request, redirect, session, flash
import psycopg2
import os
from pathlib import Path

# АБСОЛЮТНЫЙ путь к templates
base_dir = Path(__file__).parent.parent
templates_path = base_dir / 'templates'

app = Flask(__name__, template_folder=str(templates_path))
app.secret_key = os.urandom(24)

# Добавьте этот маршрут после delete_task

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        # Обновляем задачу
        new_task = request.form.get('task', '').strip()
        if not new_task:
            flash('Task cannot be empty!')
            return redirect('/')
        
        try:
            cur.execute('UPDATE todos SET task = %s WHERE id = %s AND user_id = %s', 
                       (new_task, id, session['user_id']))
            conn.commit()
            flash('Task updated successfully!')
        except Exception as e:
            flash(f'Server error: {str(e)}')
        finally:
            cur.close()
            conn.close()
        return redirect('/')
    
    else:
        # Показываем форму редактирования
        try:
            cur.execute('SELECT * FROM todos WHERE id = %s AND user_id = %s', 
                       (id, session['user_id']))
            task = cur.fetchone()
            
            if not task:
                flash('Task not found!')
                return redirect('/')
                
        except Exception as e:
            flash(f'Server error: {str(e)}')
            return redirect('/')
        finally:
            cur.close()
            conn.close()
        
        return render_template('edit.html', task=task)

# Также обновите index.html чтобы кнопка Edit вела на правильный URL
# В templates/index.html должна быть строка типа:
# <a href="/edit/{{ task[0] }}">Edit</a>





def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database=os.environ.get('DB_NAME', 'todo_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            flash('Registered successfully! Please log in.')
        except psycopg2.IntegrityError:
            flash('Username already exists')
        except Exception as e:
            flash(f'Server error: {str(e)}')
        finally:
            cur.close()
            conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, password))
            user = cur.fetchone()
            if user:
                session['username'] = username
                session['user_id'] = user[0]
                flash('Logged in!')
                return redirect('/')
            else:
                flash('Invalid credentials')
        except Exception as e:
            flash(f'Server error: {str(e)}')
        finally:
            cur.close()
            conn.close()
        return redirect('/login')
    
    # Диагностика
    print(f"Template folder: {app.template_folder}")
    print(f"Login.html exists: {os.path.exists(os.path.join(app.template_folder, 'login.html'))}")
    
    return render_template('login.html')

@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM todos WHERE user_id = %s', (session['user_id'],))
        tasks = cur.fetchall()
    except Exception as e:
        flash(f'Server error: {str(e)}')
        tasks = []
    finally:
        cur.close()
        conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect('/login')
    task = request.form.get('task', '').strip()
    if not task:
        flash('Task cannot be empty!')
        return redirect('/')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO todos (task, user_id) VALUES (%s, %s)', (task, session['user_id']))
        conn.commit()
        flash('Task added successfully!')
    except Exception as e:
        flash(f'Server error: {str(e)}')
    finally:
        cur.close()
        conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM todos WHERE id = %s AND user_id = %s', (id, session['user_id']))
        conn.commit()
        flash('Task deleted!')
    except Exception as e:
        flash(f'Server error: {str(e)}')
    finally:
        cur.close()
        conn.close()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out!')
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
