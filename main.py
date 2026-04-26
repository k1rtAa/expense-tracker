import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker v1.0")
        self.root.geometry("600x650")
        
        self.data_file = "expenses.json"
        self.expenses = self.load_data()

        # --- Форма ввода ---
        frame_input = tk.LabelFrame(root, text="Добавить новый расход", padx=10, pady=10)
        frame_input.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0, sticky="w")
        self.entry_amount = tk.Entry(frame_input)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Категория:").grid(row=1, column=0, sticky="w")
        self.combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Жилье", "Другое"])
        self.combo_category.grid(row=1, column=1, padx=5, pady=2)
        self.combo_category.current(0)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky="w")
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=2, column=1, padx=5, pady=2)

        tk.Button(frame_input, text="Добавить расход", command=self.add_expense, bg="#4CAF50", fg="white").grid(row=3, columnspan=2, pady=10)

        # --- Фильтрация ---
        frame_filter = tk.LabelFrame(root, text="Фильтрация и Итоги", padx=10, pady=10)
        frame_filter.pack(pady=5, padx=10, fill="x")

        tk.Label(frame_filter, text="Категория:").grid(row=0, column=0)
        self.filter_cat = ttk.Combobox(frame_filter, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Жилье", "Другое"])
        self.filter_cat.current(0)
        self.filter_cat.grid(row=0, column=1, padx=5)

        tk.Button(frame_filter, text="Применить фильтр", command=self.update_table).grid(row=0, column=2, padx=5)

        self.label_total = tk.Label(frame_filter, text="Итого за период: 0.00", font=("Arial", 10, "bold"))
        self.label_total.grid(row=1, columnspan=3, pady=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Date", "Category", "Amount"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Amount", text="Сумма")
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.update_table()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=4, ensure_ascii=False)

    def add_expense(self):
        amount_str = self.entry_amount.get().strip()
        category = self.combo_category.get()
        date_str = self.entry_date.get().strip()

        # Валидация
        try:
            amount = float(amount_str)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return

        self.expenses.append({"date": date_str, "category": category, "amount": amount})
        self.save_data()
        self.update_table()
        self.entry_amount.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        selected_cat = self.filter_cat.get()
        total = 0.0

        for exp in self.expenses:
            if selected_cat == "Все" or exp["category"] == selected_cat:
                self.tree.insert("", tk.END, values=(exp["date"], exp["category"], f"{exp['amount']:.2f}"))
                total += exp["amount"]
        
        self.label_total.config(text=f"Итого за период: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
