from db_functions import *

def toggle_task_status(task_id):
    task_new_status = 0 if bool(get_task_status()) else 1
    set_task_status(task_id, task_new_status)
