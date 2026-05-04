import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- Настройки ---
FILENAME = "quotes.json"
DEFAULT_QUOTES = [
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "theme": "Мотивация"},
    {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "theme": "Жизнь"},
    {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "theme": "Образование"}
]

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")
        
        self.quotes = DEFAULT_QUOTES.copy()
        self.history = []
        
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # --- Фрейм для генерации ---
        frame_gen = tk.LabelFrame(self.root, text="Сгенерировать цитату")
        frame_gen.pack(pady=10, fill="x")

        self.quote_label = tk.Label(frame_gen, text="", wraplength=400, font=("Arial", 12))
        self.quote_label.pack(pady=5)

        self.author_label = tk.Label(frame_gen, text="", font=("Arial", 10, "italic"))
        self.author_label.pack(pady=5)

        btn_gen = tk.Button(frame_gen, text="Сгенерировать цитату", command=self.generate_quote)
        btn_gen.pack(pady=10)

        # --- Фрейм для добавления ---
        frame_add = tk.LabelFrame(self.root, text="Добавить свою цитату")
        frame_add.pack(pady=10, fill="x", padx=10)

        tk.Label(frame_add, text="Текст:").grid(row=0, column=0, sticky="w")
        self.entry_text = tk.Entry(frame_add, width=40)
        self.entry_text.grid(row=0, column=1, pady=5)

        tk.Label(frame_add, text="Автор:").grid(row=1, column=0, sticky="w")
        self.entry_author = tk.Entry(frame_add, width=40)
        self.entry_author.grid(row=1, column=1, pady=5)

        tk.Label(frame_add, text="Тема:").grid(row=2, column=0, sticky="w")
        self.entry_theme = ttk.Combobox(frame_add, values=["Мотивация", "Жизнь", "Образование", "Юмор"], width=37)
        self.entry_theme.grid(row=2, column=1, pady=5)
        self.entry_theme.set("Мотивация")

        btn_add = tk.Button(frame_add, text="Добавить", command=self.add_quote)
        btn_add.grid(row=3, columnspan=2, pady=10)

        # --- Фрейм для фильтрации ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтр истории")
        frame_filter.pack(pady=10, fill="x", padx=10)

        self.filter_var = tk.StringVar()
        
        rb_all = tk.Radiobutton(frame_filter, text="Все", variable=self.filter_var, value="all", command=self.update_history_list)
        rb_all.pack(side="left")
        
        rb_author = tk.Radiobutton(frame_filter, text="По автору", variable=self.filter_var, value="author", command=self.update_history_list)
        rb_author.pack(side="left")
        
        rb_theme = tk.Radiobutton(frame_filter, text="По теме", variable=self.filter_var, value="theme", command=self.update_history_list)
        rb_theme.pack(side="left")
        
        self.filter_entry = tk.Entry(frame_filter)
        self.filter_entry.pack(side="left", padx=5)
        
        btn_apply_filter = tk.Button(frame_filter, text="Применить", command=self.update_history_list)
        btn_apply_filter.pack(side="left")

        # --- Фрейм для истории ---
        frame_hist = tk.LabelFrame(self.root, text="История сгенерированных цитат")
        frame_hist.pack(pady=10, fill="both", expand=True)

        self.history_listbox = tk.Listbox(frame_hist, height=10)
        self.history_listbox.pack(fill="both", expand=True)
        
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(FILENAME):
            try:
                with open(FILENAME, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes = data.get('quotes', DEFAULT_QUOTES.copy())
                    self.history = data.get('history', [])
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить данные: {e}")

    def save_data(self):
        """Сохранение данных в JSON файл"""
        data = {
            'quotes': self.quotes,
            'history': self.history
        }
        try:
            with open(FILENAME, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Данные успешно сохранены.")
            # Сообщение в консоль Git (см. ниже)
            print("GIT: Файл quotes.json изменен.")
            print("GIT: Рекомендуется выполнить 'git add quotes.json'")
            print("GIT: Рекомендуется выполнить 'git commit -m 'Обновление истории/базы цитат''")
            print("GIT: Рекомендуется выполнить 'git push'")
def generate_quote(self):
        """Генерация случайной цитаты"""
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "База цитат пуста. Добавьте свои цитаты.")
            return

        quote = random.choice(self.quotes)
        
        # Отображение на экране
        self.quote_label.config(text=f'"{quote['text']}"')
        self.author_label.config(text=f"— {quote['author']} (Тема: {quote['theme']})")
        
        # Добавление в историю (без дублей подряд)
        if not self.history or self.history[-1] != quote:
            self.history.append(quote)
            self.update_history_list()
            self.save_data()

    def add_quote(self):
        """Добавление новой цитаты с проверкой ввода"""
        text = self.entry_text.get().strip()
        author = self.entry_author.get().strip()
        
        if not text or not author:
            messagebox.showerror("Ошибка ввода", "Поля 'Текст' и 'Автор' обязательны для заполнения.")
            return

        new_quote = {
            "text": text,
            "author": author,
            "theme": self.entry_theme.get()
        }
        
        self.quotes.append(new_quote)
        
        # Очистка полей
        self.entry_text.delete(0, 'end')
        self.entry_author.delete(0, 'end')
        
    def update_history_list(self):
        """Обновление списка истории с учетом фильтра"""
        self.history_listbox.delete(0, 'end')
        
        filter_type = self.filter_var.get()
        
        for quote in self.history:
            display_text = f'"{quote["text"]}" — {quote["author"]}'
            
            if filter_type == "author":
                if quote["author"].lower() == self.filter_entry.get().lower():
                    self.history_listbox.insert('end', display_text)
            elif filter_type == "theme":
                if quote["theme"].lower() == self.filter_entry.get().lower():
                    self.history_listbox.insert('end', display_text)
            else: # all
                self.history_listbox.insert('end', display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
