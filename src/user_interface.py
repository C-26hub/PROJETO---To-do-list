import customtkinter as ctk
import datetime
from PIL import Image
import data_handler as dh

# Variáveis globais
app = None
entry_my_task = None
entry_date = None
entry_description = None
task_list_frame = None

# Aparência
def configure_appearance():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

# Janela principal
def create_window():
    global app
    app = ctk.CTk()
    app.title("🧠 Study Up - Minhas Tarefas")
    app.geometry("800x600")
    app.configure(fg_color="#FDFCFB")

# Logo
def display_logo():
    logo_image = ctk.CTkImage(
        light_image=Image.open("src\\image\\transparent_logo.png"),
        dark_image=Image.open("src\\image\\transparent_logo.png"),
        size=(160, 160)
    )
    logo_label = ctk.CTkLabel(app, image=logo_image, text="")
    logo_label.pack(pady=(30, 5))

# Subtítulo
def display_subtitle():
    subtitle = ctk.CTkLabel(app, text="Minhas Tarefas", font=ctk.CTkFont(size=24, weight="bold"))
    subtitle.pack(pady=(10, 20))

# Área de entrada
def create_input_area():
    global entry_my_task, entry_date, entry_description
    entry_frame = ctk.CTkFrame(app, fg_color="transparent")
    entry_frame.pack(pady=5)

    entry_my_task = ctk.CTkEntry(entry_frame, placeholder_text="Digite a sua tarefa aqui", width=250)
    entry_my_task.grid(row=0, column=0, padx=8)

    entry_date = ctk.CTkEntry(entry_frame, placeholder_text="dd/mm/aaaa", width=120)
    entry_date.grid(row=0, column=1, padx=8)

    entry_description = ctk.CTkEntry(entry_frame, placeholder_text="Digite uma descrição...", width=200)
    entry_description.grid(row=0, column=2, padx=8)

    add_task_button = ctk.CTkButton(app, text="Adicionar Tarefa", corner_radius=10,
                                    fg_color="#A264D5", hover_color="#8A4AB1",
                                    command=lambda: add_task())
    add_task_button.pack(pady=10)

# Lista de tarefas com scroll
def create_task_list():
    global task_list_frame

    container = ctk.CTkFrame(app)
    container.pack(pady=10, fill="both", expand=True)

    canvas = ctk.CTkCanvas(container, bg="#FDFCFB", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = ctk.CTkFrame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    task_list_frame = scrollable_frame

# Filtro de status
def create_filter():
    app.status_var = ctk.StringVar(value="Todos")

    filter_frame = ctk.CTkFrame(app, fg_color="transparent")
    filter_frame.pack(side="bottom", pady=10, fill="x", padx=20)

    ctk.CTkLabel(filter_frame, text="Filtro:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)

    app.combo = ctk.CTkOptionMenu(
        filter_frame,
        values=["Todos", "Pendente", "Concluída"],
        variable=app.status_var,
        command=lambda _: update_list()
    )
    app.combo.pack(side="right")

# Atualizar lista de tarefas
def update_list():
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    filtro = app.status_var.get()
    tarefas_filtradas = dh.get_filtered_tasks(filtro)

    for t in tarefas_filtradas:
        task_id = t["id"]

        row = ctk.CTkFrame(task_list_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=4)

        var = ctk.BooleanVar(value=t["feito"])

        def toggle(id_to_toggle=task_id):
            dh.toggle_task_status(id_to_toggle)
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
        date_label.pack(side="right", padx=5)

        delete_button = ctk.CTkButton(
            row, text="❌", width=30, height=24,
            command=lambda id_to_delete=task_id: delete_task(id_to_delete),
            fg_color="red", hover=False
        )
        delete_button.pack(side="right", padx=2)

        edit_button = ctk.CTkButton(
            row, text="✏️", width=30, height=24,
            command=lambda t_id=task_id, t_name=t["task"], t_date=t["date"], t_desc=t["description"]: open_edit_popup(t_id, t_name, t_date, t_desc),
            fg_color="transparent", hover=False
        )
        edit_button.pack(side="right", padx=2)

# Função de editar tarefa
def open_edit_popup(task_id, current_task, current_date, current_description):
    popup = ctk.CTkToplevel(app)
    popup.title("Editar Tarefa")
    popup.geometry("400x250")

    ctk.CTkLabel(popup, text="Tarefa:").pack(pady=5)
    task_entry = ctk.CTkEntry(popup)
    task_entry.insert(0, current_task)
    task_entry.pack()

    ctk.CTkLabel(popup, text="Data (dd/mm/aaaa):").pack(pady=5)
    date_entry = ctk.CTkEntry(popup)
    date_entry.insert(0, datetime.datetime.strptime(current_date, "%Y-%m-%d").strftime('%d/%m/%Y'))
    date_entry.pack()

    ctk.CTkLabel(popup, text="Descrição:").pack(pady=5)
    desc_entry = ctk.CTkEntry(popup)
    desc_entry.insert(0, current_description)
    desc_entry.pack()

    def salvar_edicao():
        nova_tarefa = task_entry.get()
        nova_data = date_entry.get()
        nova_desc = desc_entry.get()

        if nova_tarefa.strip():
            dh.update_task_name(task_id, nova_tarefa)

        if nova_desc.strip():
            dh.update_task_description(task_id, nova_desc)

        try:
            data_formatada = datetime.datetime.strptime(nova_data, "%d/%m/%Y").strftime('%Y-%m-%d')
            dh.update_task_deadline(task_id, data_formatada)
        except ValueError:
            date_entry.delete(0, "end")
            date_entry.configure(placeholder_text="Data Inválida")
            return

        popup.destroy()
        update_list()

    ctk.CTkButton(popup, text="Salvar", command=salvar_edicao).pack(pady=10)

# Adicionar nova tarefa
def add_task():
    task = entry_my_task.get()
    date = entry_date.get()
    description = entry_description.get()

    if not task.strip() or not date.strip():
        return

    try:
        deadline_for_db = datetime.datetime.strptime(date, "%d/%m/%Y").strftime('%Y-%m-%d')
    except ValueError:
        entry_date.delete(0, "end")
        entry_date.configure(placeholder_text="Data Inválida")
        return

    dh.create_task(task, deadline_for_db, description)

    entry_my_task.delete(0, "end")
    entry_date.delete(0, "end")
    entry_description.delete(0, "end")
    update_list()

# Deletar tarefa
def delete_task(task_id):
    dh.delete_task(task_id)
    update_list()

# Iniciar aplicação
def start_app():
    configure_appearance()
    create_window()
    display_logo()
    display_subtitle()
    create_input_area()
    create_filter()
    create_task_list()
    update_list()
    app.mainloop()
