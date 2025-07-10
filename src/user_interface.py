import customtkinter as ctk
import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


tasks = []

app = ctk.CTk() 
app.title("Study Up - Minhas Tarefas") 
app.geometry("800x600") 


label_my_task = ctk.CTkLabel(app, text = "Minhas Tarefas", font=("Rubik", 36))
label_my_task.pack(pady=15) 

entry_my_task = ctk.CTkEntry(app, placeholder_text="Digite a sua tarefa aqui", width= 200)
entry_my_task.pack(pady=10)

entry_date = ctk.CTkEntry(app, placeholder_text="dd/mm/aaaa", width= 100)
entry_date.pack(pady=5)

entry_description = ctk.CTkEntry(app, placeholder_text="Descrição da tarefa", width=300)
entry_description.pack(pady=5)

Task_list = ctk.CTkFrame(app, width=600, height=200)
Task_list.pack(pady=10)
Task_list.pack_propagate(False)

filter_frame = ctk.CTkFrame(app, fg_color="transparent", width=100)
filter_frame.pack(pady= 10)
ctk.CTkLabel(filter_frame, text="Filtro", font=("Rubik", 14)).pack()

app.status_var = ctk.StringVar(value="Todos")
app.combo = ctk.CTkOptionMenu(
    filter_frame,
    values=["Todos", "Pendente", "Concluída"],
    variable=app.status_var,
    command=lambda _: update_list()
)
app.combo.pack()

def update_list():
    for widget in Task_list.winfo_children():
        widget.destroy()

    filtro = app.status_var.get()


    for i, t in enumerate(tasks):
        if filtro == "Todos" or \
           (filtro == "Pendente" and not t["feito"]) or \
           (filtro == "Concluída" and t["feito"]):

            task_frame = ctk.CTkFrame(Task_list, fg_color="transparent")
            task_frame.pack(fill="x", padx=10, pady=5)

            var = ctk.BooleanVar(value=t["feito"])

            def toggle_feito(index=i):
                tasks[index]["feito"] = not tasks[index]["feito"]
                update_list()

            checkbox = ctk.CTkCheckBox(
                task_frame,
                text=f"{t['task']} - {t['date']}",
                variable=var,
                command=toggle_feito
            )
            checkbox.pack(anchor="w", padx=5)

            if t["description"]:
                desc_label = ctk.CTkLabel(
                    task_frame,
                    text=f"Descrição: {t['description']}",
                    font=("Rubik", 12),
                    text_color="#666666"
                )
                desc_label.pack(anchor="w", padx=35)

            def excluir_tarefa(index=i):
                tasks.pop(index)
                update_list()

            delete_button = ctk.CTkButton(
                task_frame,
                text="❌",
                width=30,
                height=24,
                command=excluir_tarefa
            )
            delete_button.pack(side="right", padx=5)


def add_task():
    task = entry_my_task.get()
    date = entry_date.get()
    description = entry_description.get()

    if task.strip() == "" or date.strip() == "":
        return

    try:
        datetime.datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        entry_date.delete(0, "end")
        entry_date.configure(placeholder_text="Data Inválida")
        return

    tasks.append({"task": task, "date": date, "description": description, "feito": False})

    entry_my_task.delete(0, "end")
    entry_date.delete(0, "end")
    entry_description.delete(0, "end")
    update_list()

add_task_button = ctk.CTkButton(app, text="Adicionar Tarefa",  command= add_task)
add_task_button.pack(pady=10)

app.mainloop()