# главное окно

import customtkinter as ctk
from database.crud import get_balance

from ui.transaction_form import TransactionForm
from ui.category_window import CategoryWindow
from ui.transactions_window import TransactionsWindow

class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ---------- APP SETTINGS ----------
        ctk.set_appearance_mode("System")   # Dark / Light / System
        ctk.set_default_color_theme("blue")

        self.title("Finance Manager")
        self.geometry("600x400")
        self.resizable(False, False)

        # ---------- MAIN CONTAINER ----------
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------- TITLE ----------
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Личный финансовый менеджер",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))

        # ---------- BALANCE ----------
        self.balance_var = ctk.StringVar()
        self.balance_label = ctk.CTkLabel(
            self.container,
            textvariable=self.balance_var,
            font=ctk.CTkFont(size=18)
        )
        self.balance_label.pack(pady=(0, 30))

        self.update_balance()

        # ---------- BUTTONS ----------
        self.buttons_frame = ctk.CTkFrame(self.container)
        self.buttons_frame.pack(pady=10)

        self.income_btn = ctk.CTkButton(
            self.buttons_frame,
            text="💰 Добавить доход",
            width=200,
            command=self.open_income_window
        )
        self.income_btn.grid(row=0, column=0, padx=10, pady=10)

        self.expense_btn = ctk.CTkButton(
            self.buttons_frame,
            text="💸 Добавить расход",
            width=200,
            command=self.open_expense_window
        )
        self.expense_btn.grid(row=1, column=0, padx=10, pady=10)

        self.category_btn = ctk.CTkButton(
            self.buttons_frame,
            text="📂 Категории",
            width=200,
            command=self.open_category_window
        )
        self.category_btn.grid(row=2, column=0, padx=10, pady=10)

        self.transactions_btn = ctk.CTkButton(
            self.buttons_frame,
            text="📋 Операции",
            width=200,
            command=self.open_transactions
        )
        self.transactions_btn.grid(row=3, column=0, padx=10, pady=10)

    # ---------- METHODS ----------

    def update_balance(self):
        balance = get_balance()

        color = "#2ecc71" if balance >= 0 else "#e74c3c"

        self.balance_var.set(f"Текущий баланс: {balance:.2f} ₸")
        self.balance_label.configure(text_color=color)


    def open_income_window(self):
        TransactionForm(self, "income", self.update_balance)

    def open_expense_window(self):
        TransactionForm(self, "expense", self.update_balance)

    def open_category_window(self):
        CategoryWindow(self)

    def open_transactions(self):
        TransactionsWindow(self)
