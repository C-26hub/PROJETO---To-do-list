import sqlite3 as db

def open_connection():
    connection = db.connect("todo.db")
    return connection.cursor()

def close_connection(curso):
    
    curso.close()

def create_db():
    connection = db.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name VARCHAR(40),
        task_description VARCHAR(100)
    )
    """)
    cursor.commit()
    cursor.close()
    connection.close()

def add_task(task_name, task_description):
    connection = db.connect("todo.db")
    cursor = connection.cursor()
    open_connection().execute("""
        INSERT INTO tasks (task_name, task_description) VALUES (?,?)
    """, (task_name, task_description))
    cursor.commit()
    cursor.close()
    connection.close()  