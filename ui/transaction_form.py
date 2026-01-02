import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from database.crud import add_transaction, get_categories
from ui.date_picker import DatePicker


class TransactionForm(ctk.CTkToplevel):

    def __init__(self, parent, transaction_type, on_success):
        super().__init__(parent)

        self.transaction_type = transaction_type  # income / expense
        self.on_success = on_success

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.attributes("-topmost", True)

        title = "Добавить доход" if transaction_type == "income" else "Добавить расход"
        self.title(title)
        self.geometry("400x450")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self.frame,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        # сумма
        self.amount = ctk.CTkEntry(
            self.frame,
            placeholder_text="Сумма (₸)"
        )
        self.amount.pack(fill="x", pady=5)

        # категории
        self.categories = get_categories()
        self.category_box = ctk.CTkOptionMenu(
            self.frame,
            values=[c["name"] for c in self.categories]
        )
        self.category_box.pack(fill="x", pady=5)

        # дата
        date_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=5)

        self.date = ctk.CTkEntry(date_frame)
        self.date.pack(side="right", fill="x", expand=True)

        ctk.CTkButton(
            date_frame,
            text="📅",
            width=40,
            command=lambda: DatePicker(self, self.date)
        ).pack(side="left", padx=(0, 5))

        self.date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # комментарий
        self.comment = ctk.CTkEntry(
            self.frame,
            placeholder_text="Комментарий (обязательно)"
        )
        self.comment.pack(fill="x", pady=5)

        self.status = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.status.pack(pady=5)

        ctk.CTkButton(
            self.frame,
            text="Сохранить",
            height=40,
            command=self.save
        ).pack(pady=10)

    def save(self):
        try:
            amount = float(self.amount.get())
            comment = self.comment.get().strip()

            if not comment:
                raise ValueError("Комментарий обязателен")

            category_name = self.category_box.get()
            category_id = next(
                c["id"] for c in self.categories if c["name"] == category_name
            )

            add_transaction(
                self.transaction_type,
                amount,
                category_id,
                self.date.get(),
                comment
            )

            self.on_success()
            self.destroy()

        except Exception as e:
            self.status.configure(text=str(e))
