import sqlite3 as db

def execute(script, *args):
    connection = db.connect("to_do.db")
    cursor = connection.cursor()
    cursor.execute(script, args)
    connection.commit()
    cursor.close()
    connection.close()

def query(script, *args):
    connection = db.connect("to_do.db")
    cursor = connection.cursor()
    cursor.execute(script, args)
    results = cursor.fetchall() #pegar resultados
    cursor.close()
    connection.close()
    return results # retorna resultados 

## system config
def create_db():
    execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        task_name TEXT NOT NULL,
        task_description TEXT,
        deadline TEXT NOT NULL,
        status INTEGER CHECK (status IN (0,1)) DEFAULT 0
    )
    """)
    """sqlite não tem varchar, bool e date, ele converte para text e numeral, para melhorar desempenho e clareza do código foi decidido usar os tipos do sqlite"""
    
## create

def add_task(task_name, task_description=None, deadline, status=0):
    execute("""
        INSERT INTO tasks (task_name, task_description, deadline, status) VALUES (?,?,?,?)
    """, task_name, task_description, deadline, status)

## read

## select all tasks

def select_all_tasks():
    """Retorna todas as tarefas, sem filtro, ordenadas pela data de prazo."""
    return query("SELECT * FROM tasks ORDER BY deadline ASC")

## select done tasks
def select_done_tasks():
    """Retorna apenas as tarefas com status 1 (concluída)."""
    return query("SELECT * FROM tasks WHERE status = ? ORDER BY deadline ASC", 1)

## select pending tasks
def select_pending_tasks():
    """Retorna apenas as tarefas com status 0 (pendente)."""
    return query("SELECT * FROM tasks WHERE status = ?", 0)

def get_task_status(task_id):
    result = query("SELECT status FROM tasks WHERE task_id = ?", task_id)
    if result:
        return result[0][0]
    return None

## update
## rename task
def set_task_description(task_id, new_description):
    execute("""
    UPDATE tasks
    SET task_description = ?
    WHERE task_id = ?
    """, new_description, task_id)

## change deadline
def set_deadline(task_id, new_deadline):
    execute("""
    UPDATE tasks
    SET deadline = ?
    WHERE task_id = ?
    """, new_deadline, task_id)

## mark done/pending
def set_task_status(task_id, task_new_status):
    execute("""
    UPDATE tasks
    SET status = ?
    WHERE task_id = ?
    """, task_new_status, task_id)

## delete
## delete tasks by id
def delete_task_by_id(task_id):
    """Apaga uma tarefa específica do banco, identificada pelo ID."""
    execute("DELETE FROM tasks WHERE task_id = ?", task_id)
