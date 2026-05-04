import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- НАСТРОЙКИ ---
FILENAME = "tasks.json"
DEFAULT_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Разобрать почту", "type": "работа"},
    {"name": "Посмотреть обучающее видео", "type": "учёба"},
    {"name": "Погулять на свежем воздухе", "type": "спорт"}
]

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x500")
        
        # Инициализация данных
        self.tasks = DEFAULT_TASKS.copy()
        self.history = []
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # --- Фрейм 1: Генерация задачи ---
        frame_gen = tk.LabelFrame(self.root, text="Сгенерировать задачу", padx=10, pady=10)
        frame_gen.pack(pady=5, fill="x", padx=10)

        self.task_label = tk.Label(frame_gen, text="", wraplength=300, font=("Arial", 12), justify="center")
        self.task_label.pack(pady=10)

        btn_gen = tk.Button(frame_gen, text="Сгенерировать задачу", command=self.generate_task)
        btn_gen.pack(pady=10)

        # --- Фрейм 2: Добавление новой задачи ---
        frame_add = tk.LabelFrame(self.root, text="Добавить свою задачу", padx=10, pady=10)
        frame_add.pack(pady=5, fill="x", padx=10)

        tk.Label(frame_add, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(frame_add, width=35)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(frame_add, text="Тип:").grid(row=1, column=0, sticky="w")
        self.entry_type = ttk.Combobox(frame_add, values=["учёба", "спорт", "работа"], width=32)
        self.entry_type.grid(row=1, column=1, pady=5)
        self.entry_type.set("учёба")

        btn_add = tk.Button(frame_add, text="Добавить в базу", command=self.add_task)
        btn_add.grid(row=2, columnspan=2, pady=10)

        # --- Фрейм 3: Фильтр и История ---
        frame_hist = tk.LabelFrame(self.root, text="История и фильтр", padx=10, pady=10)
        frame_hist.pack(pady=5, fill="both", expand=True, padx=10)

        # Панель фильтра
        filter_panel = tk.Frame(frame_hist)
        filter_panel.pack(fill="x")

        self.filter_var = tk.StringVar(value="all")
        
        rb_all = tk.Radiobutton(filter_panel, text="Все", variable=self.filter_var, value="all", command=self.update_history_list)
        rb_all.pack(side="left")
        
        rb_type = tk.Radiobutton(filter_panel, text="По типу", variable=self.filter_var, value="type", command=self.update_history_list)
        rb_type.pack(side="left")
        
        self.filter_entry = ttk.Combobox(filter_panel, values=["учёба", "спорт", "работа"], width=15, state="readonly")
        self.filter_entry.pack(side="left", padx=(5, 0))
        
        btn_apply_filter = tk.Button(filter_panel, text="Применить", command=self.update_history_list)
        btn_apply_filter.pack(side="left")

        # Список истории
        scrollbar = ttk.Scrollbar(frame_hist)
        scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(frame_hist, yscrollcommand=scrollbar.set, height=12)
        self.history_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)

    def load_data(self):
        """Загрузка данных из JSON файла при запуске"""
        if os.path.exists(FILENAME):
            try:
                with open(FILENAME, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'tasks' in data:
                        self.tasks = data['tasks']
                    if 'history' in data:
                        self.history = data['history']
                print("Данные успешно загружены из JSON.")
            except Exception as e:
                print(f"Ошибка при загрузке данных: {e}")
                messagebox.showerror("Ошибка", "Не удалось загрузить историю. Будет использована пустая база.")

    def save_data(self):
        """Сохранение данных в JSON файл"""
        data = {
            'tasks': self.tasks,
            'history': self.history
        }
        try:
            with open(FILENAME, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("GIT: Файл tasks.json изменен. Не забудьте закоммитить изменения (git add/commit/push).")
            print("Данные успешно сохранены.")
            self.update_history_list() # Обновляем список после сохранения на случай фильтрации
        except Exception as e:
                print(f"Ошибка при загрузке данных: {e}")
                messagebox.showerror("Ошибка", "Не удалось загрузить историю. Будет использована пустая база.")
    def generate_task(self):
        """Генерация случайной задачи из базы"""
        if not self.tasks:
            messagebox.showwarning("База пуста", "В базе нет задач. Добавьте свои через форму ниже.")
            return

        task = random.choice(self.tasks)
        
        # Отображение на экране
        self.task_label.config(text=f'• {task["name"]}')
        
        # Добавление в историю (без повторяющихся подряд задач)
        if not self.history or self.history[-1] != task:
            self.history.append(task)
            self.save_data() # Сохраняем сразу после добавления в историю

    def add_task(self):
        """Добавление новой задачи с проверкой на пустое название"""
        name = self.entry_name.get().strip()
        
        if not name:
            messagebox.showerror("Ошибка ввода", "Поле 'Название' обязательно для заполнения.")
            return

        new_task = {
            "name": name,
            "type": self.entry_type.get()
        }
        
        self.tasks.append(new_task)
        
        # Очистка поля и сохранение
        self.entry_name.delete(0, 'end')
        
    def update_history_list(self):
        """Обновление виджета списка истории с учетом активного фильтра"""
        filter_type = self.filter_var.get()
        
        # Очищаем список перед обновлением
        self.history_listbox.delete(0, 'end')
        
        for task in self.history:
            display_text = f'• {task["name"]} (Тип: {task["type"]})'
            
            if filter_type == "type":
                if task["type"] == self.filter_entry.get():
                    self.history_listbox.insert('end', display_text)
            else: # Показываем все (filter_type == "all")
                self.history_listbox.insert('end', display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
