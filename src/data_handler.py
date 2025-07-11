from db_functions import *
from datetime import datetime 

def init_database():
    db.create_db()

## create
def create_task(task_description, deadline):
    add_task(task_description, deadline)

## read
def get_tasks():
    """Busca as tarefas do banco e retorna uma lista de dicionários."""

    tasks_from_db = select_all_tasks()
    formatted_tasks = []
    for task_tuple in tasks_from_db:
        task_id, task_name, description, deadline, status_code = task_tuple
        task_info = {
            "id": task_id,
            "task": task_name,
            "date": deadline,
            "description": description,  
            "feito": bool(status_code) 
        }
        formatted_tasks.append(task_info)

    ## processamento ou conversão
    return formatted_tasks

## update
def toggle_task_status(task_id):
    new_status = int(not bool(get_task_status(task_id)))
    set_task_status(task_id, new_status)

def update_task_description(task_id, new_description):
    set_task_description(task_id, new_description)

def update_task_deadline(task_id, new_deadline):
    set_deadline(task_id, new_deadline)

## delete
def delete_task(task_id):
    delete_task_by_id(task_id)
