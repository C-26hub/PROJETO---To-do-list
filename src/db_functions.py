import sqlite3 as db

def execute(script, *args):
    connection = db.connect("to_do.db")
    cursor = connection.cursor()
    cursor.execute(script, args)
    connection.commit()
    cursor.close()
    connection.close()

## system config
def create_db():
    execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        task_description VARCHAR(100),
        deadline DATE NOT NULL,
        status INTEGER CHECK (status IN (0,1)) DEFAULT 0
    )
    """)
    
## create
def add_task(task_name, deadline, task_description=None, status=0):
    execute("""
        INSERT INTO tasks (task_name, task_description, deadline, status) VALUES (?,?,?,?,?)
    """, task_name, task_description, deadline, status)

## read

## select all tasks
## select done tasks
## select pending tasks

## update

## rename task
## rewrite description
## change deadline
## mark done/pending

## delete

## delete tasks by id
