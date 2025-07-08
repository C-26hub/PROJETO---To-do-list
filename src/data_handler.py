from db_functions import *

def toggle_task_status(task_id):
    task_new_status = 0 if bool(get_task_status()) else 1
    set_task_status(task_id, task_new_status)

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
