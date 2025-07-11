from db_functions import *
from datetime import datetime 

def init_database():
    create_db()

## create
def create_task(task_name, deadline, task_description):
    add_task(task_name, deadline, task_description)

## read
def get_filtered_tasks(filtro="Todos"):

    if filtro == "Pendente":
        tasks_from_db = select_pending_tasks()
    elif filtro == "Concluída":
        tasks_from_db = select_done_tasks()
    else: 
        tasks_from_db = select_all_tasks()
        
    formatted_tasks = []
    for task_tuple in tasks_from_db:
        task_id, task_name, deadline, description, status_code = task_tuple
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

def update_task_name(task_id, new_name):
    set_task_name(task_id, new_name)
## delete
def delete_task(task_id):
    delete_task_by_id(task_id)
