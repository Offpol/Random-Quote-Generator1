import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# --- Константы ---
HISTORY_FILE = "quote_history.json"

# --- Структура данных ---
quotes = [
    {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Работа"},
    {"text": "Успех — это способность идти от одной неудачи к другой, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"},
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Счастье не в том, чтобы делать, что хочешь, а в том, чтобы хотеть того, что делаешь.", "author": "Лев Толстой", "topic": "Счастье"},
]

# --- Функции ---

def load_history():
    """Загружает историю цитат из JSON файла."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history(history):
    """Сохраняет историю цитат в JSON файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_quote():
    """Генерирует и отображает случайную цитату."""
    if not quotes:
        messagebox.showwarning("Нет цитат", "Добавьте цитаты в список.")
        return

    selected_quote = random.choice(quotes)
    quote_text.set(f"'{selected_quote['text']}'")
    quote_author.set(f"- {selected_quote['author']}")
    quote_topic.set(f"Тема: {selected_quote['topic']}")

    # Добавляем в историю
    current_history = load_history()
    current_history.append(selected_quote)
    save_history(current_history)
    update_history_list()

def update_history_list():
    """Обновляет отображение списка истории цитат."""
    history_frame.destroy() # Удаляем старый виджет Frame
    build_history_display() # Создаем новый

def build_history_display():
    """Создает виджеты для отображения истории."""
    global history_frame
    history_frame = tk.Frame(history_window)
    history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    current_history = load_history()
    for i, q in enumerate(reversed(current_history)): # Отображаем в обратном порядке
        label_text = f"{i+1}. '{q['text']}' ({q['author']}, {q['topic']})"
        tk.Label(history_frame, text=label_text, wraplength=300, justify="left").pack(anchor="w", fill=tk.X)

def filter_quotes(filter_type):
    """Фильтрует цитаты по автору или теме."""
    filter_value = simpledialog.askstring("Фильтрация", f"Введите {filter_type.lower()} для фильтрации:")
    if not filter_value:
        return

    filtered = []
    if filter_type == "Автор":
        filtered = [q for q in quotes if filter_value.lower() in q["author"].lower()]
    elif filter_type == "Тема":
        filtered = [q for q in quotes if filter_value.lower() in q["topic"].lower()]

    if not filtered:
        messagebox.showinfo("Результат фильтрации", f"Цитат по '{filter_value}' не найдено.")
        return

    selected_quote = random.choice(filtered)
    quote_text.set(f"'{selected_quote['text']}'")
    quote_author.set(f"- {selected_quote['author']}")
    quote_topic.set(f"Тема: {selected_quote['topic']}")

def add_new_quote():
    """Добавляет новую цитату в список."""
    text = simpledialog.askstring("Добавить цитату", "Введите текст цитаты:")
    if not text:
        messagebox.showwarning("Внимание", "Текст цитаты не может быть пустым.")
        return

    author = simpledialog.askstring("Добавить цитату", "Введите автора цитаты:")
    if not author:
        messagebox.showwarning("Внимание", "Автор цитаты не может быть пустым.")
        return

    topic = simpledialog.askstring("Добавить цитату", "Введите тему цитаты:")
    if not topic:
        messagebox.showwarning("Внимание", "Тема цитаты не может быть пустой.")
        return

    quotes.append({"text": text, "author": author, "topic": topic})
    messagebox.showinfo("Успех", "Цитата успешно добавлена!")
    # Обновить доступные авторы и темы для фильтрации, если потребуется
    # Для простоты, пока перезагрузка может быть сделана вручную или при перезапуске
    update_history_list() # Обновляем список, чтобы показать добавленную в историю, хотя эта функция только для просмотра

# --- GUI элементы ---

root = tk.Tk()
root.title("Генератор случайных цитат")
root.geometry("500x600")

# Контейнер для отображения цитаты
quote_display_frame = tk.Frame(root, padx=20, pady=20)
quote_display_frame.pack(fill=tk.X)

quote_text = tk.StringVar()
quote_author = tk.StringVar()
quote_topic = tk.StringVar()

tk.Label(quote_display_frame, textvariable=quote_text, font=("Arial", 14), wraplength=400, justify="center").pack(pady=10)
tk.Label(quote_display_frame, textvariable=quote_author, font=("Arial", 12, "italic")).pack(pady=5)
tk.Label(quote_display_frame, textvariable=quote_topic, font=("Arial", 10)).pack(pady=5)

# Кнопки управления
button_frame = tk.Frame(root, padx=20, pady=10)
button_frame.pack(fill=tk.X)

tk.Button(button_frame, text="Сгенерировать цитату", command=generate_quote, width=20).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Фильтр по автору", command=lambda: filter_quotes("Автор"), width=15).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Фильтр по теме", command=lambda: filter_quotes("Тема"), width=15).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Добавить цитату", command=add_new_quote, width=15).pack(side=tk.LEFT, padx=5)

# Контейнер для истории
history_window = tk.LabelFrame(root, text="История цитат", padx=10, pady=10)
history_window.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Начальная загрузка истории
build_history_display()

# --- Запуск приложения ---
root.mainloop()

# --- Сохранение истории при выходе (опционально, json сохраняет сразу) ---
# save_history(load_history())
