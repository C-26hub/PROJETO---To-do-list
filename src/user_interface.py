import customtkinter as ctk
import datetime
from PIL import Image

# Aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Janela principal
app = ctk.CTk()
app.title("🧠 Study Up - Minhas Tarefas")
app.geometry("800x600")
app.configure(fg_color="#FDFCFB")  # tom off-white suave

# --- Logo + Título ---
logo_image = ctk.CTkImage(
    light_image=Image.open("src\\image\\transparent_logo.png"),
    dark_image=Image.open("src\\image\\transparent_logo.png"),
    size=(100, 100)
)

# Logo maior com nome incluso
logo_image = ctk.CTkImage(
    light_image=Image.open("src\\image\\transparent_logo.png"),
    dark_image=Image.open("src\\image\\transparent_logo.png"),
    size=(160, 160)  # novo tamanho recomendado
)
logo_label = ctk.CTkLabel(app, image=logo_image, text="")
logo_label.pack(pady=(30, 5))  # mais espaço em cima

# Subtítulo
subtitle = ctk.CTkLabel(app, text="Minhas Tarefas", font=ctk.CTkFont(size=24, weight="bold"))
subtitle.pack(pady=(10, 20))

# --- Área de entrada da tarefa ---
entry_frame = ctk.CTkFrame(app, fg_color="transparent")
entry_frame.pack(pady=5)

# Campo: Tarefa
entry_my_task = ctk.CTkEntry(entry_frame, placeholder_text="Digite a sua tarefa aqui", width=250)
entry_my_task.grid(row=0, column=0, padx=8)

# Campo: Data
entry_date = ctk.CTkEntry(entry_frame, placeholder_text="dd/mm/aaaa", width=120)
entry_date.grid(row=0, column=1, padx=8)

# Campo: Descrição
entry_description = ctk.CTkEntry(entry_frame, placeholder_text="Digite uma descrição...", width=200)
entry_description.grid(row=0, column=2, padx=8)

# Botão adicionar
add_task_button = ctk.CTkButton(app, text="Adicionar Tarefa", corner_radius=10, fg_color="#A264D5", hover_color="#8A4AB1", command=lambda: add_task())
add_task_button.pack(pady=10)

# --- Lista de tarefas ---
tasks = []

task_list_frame = ctk.CTkFrame(app, width=700, height=300, fg_color="transparent")
task_list_frame.pack(pady=10)
task_list_frame.pack_propagate(False)

# --- Filtro ---
filter_frame = ctk.CTkFrame(app, fg_color="transparent")
filter_frame.pack(pady=(10, 5), anchor="e")

ctk.CTkLabel(filter_frame, text="Filtro:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)

app.status_var = ctk.StringVar(value="Todos")
app.combo = ctk.CTkOptionMenu(
    filter_frame,
    values=["Todos", "Pendente", "Concluída"],
    variable=app.status_var,
    command=lambda _: update_list()
)
app.combo.pack(side="left")

# --- Funções principais ---
def update_list():
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    filtro = app.status_var.get()
    
    for i, t in enumerate(tasks):
        if filtro == "Todos" or \
           (filtro == "Pendente" and not t["feito"]) or \
           (filtro == "Concluída" and t["feito"]):

            row = ctk.CTkFrame(task_list_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=4)
            
            var = ctk.BooleanVar(value=t["feito"])
            def toggle(index=i):
                tasks[index]["feito"] = not tasks[index]["feito"]
                update_list()

            checkbox = ctk.CTkCheckBox(
                row,
                text=f'{t["task"]} — {t["description"]}',
                variable=var,
                command=toggle,
                font=ctk.CTkFont(size=16),
                checkbox_width=18,
                checkbox_height=18
            )
            checkbox.pack(side="left", padx=10)

            date_label = ctk.CTkLabel(row, text=t["date"], font=ctk.CTkFont(size=16))
            date_label.pack(side="right", padx=10)

            delete_button = ctk.CTkButton(
                row,
                text="❌",
                width=30,
                height=24,
                command=lambda index=i: delete_task(index),
                fg_color="transparent",
                hover=False
            )
            delete_button.pack(side="right")


def add_task():
    task = entry_my_task.get()
    date = entry_date.get()
    description = entry_description.get()

    if not task.strip() or not date.strip():
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


def delete_task(index):
    tasks.pop(index)
    update_list()

# --- Iniciar App ---
app.mainloop()
