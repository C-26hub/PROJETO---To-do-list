from db_functions import *
from datetime import datetime 

## create
def create_task(task_description, deadline):
    add_task(task_description, deadline)

## read
def get_tasks():
    tasks = select_all_tasks()
    formatted_tasks = []
    for task in tasks:
        task_id, description, deadline, status_code = task
        status_text = "Concluída" if bool(status_code) == 0 else "Pendente"
        formatted_line = f"ID:  {task_id} Status: {status_text} Prazo: {deadline} Tarefa: {description}"
        formatted_tasks.append(formatted_line)
    ## processamento ou conversão
    return formatted_tasks

## update
def toggle_task_status(task_id):
    new_status = 0 if bool(get_task_status(task_id)) else 1
    set_task_status(task_id, new_status)
def update_task_description(task_id, new_description):
    set_task_description(task_id, new_description)

def update_task_deadline(task_id, new_deadline):
    set_deadline(task_id, new_deadline)

## delete
def delete_task(task_id):
    delete_task_by_id(task_id)
