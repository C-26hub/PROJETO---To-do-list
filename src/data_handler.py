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
    ## processamento ou conversão
    return tasks

## update

## delete
