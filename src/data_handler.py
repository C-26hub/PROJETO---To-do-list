from db_functions import *
from datetime import datetime 

def toggle_task_status(task_id):
   current_status = get_task_status(task_id)
   new_status = 1 if current_status == 0 else 0
   set_task_status(task_id, new_status)

## create
def create_task(task_description, deadline):
    add_task(task_description, deadline)

## read
def get_tasks():
    tasks = select_all_tasks()
    formatted_tasks = []
    for task in tasks:
        task_id, description, deadline, status_code = task
        status_text = "Pendente" if status_code == 0 else "Concluída"
        formatted_line = f"ID:  {task_id} Status: {status_text} Prazo: {deadline} Tarefa: {description}"
        formatted_tasks.append(formatted_line)
    ## processamento ou conversão
    return formatted_tasks

## update

## delete
