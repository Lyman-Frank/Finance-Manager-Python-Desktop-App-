import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox

from database.crud import get_transactions_filtered
from services.export_excel import export_transactions_to_excel
from ui.date_picker import DatePicker
from ui.category_filter_window import CategoryFilterWindow
from config.constants import TRANSACTION_TYPES, COLORS, FIXED_WIDTHS

COL_DATE = FIXED_WIDTHS["COL_DATE"]
COL_CATEGORY = FIXED_WIDTHS["COL_CATEGORY"]
COL_AMOUNT = FIXED_WIDTHS["COL_AMOUNT"]

class TransactionsWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        # modal
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.attributes("-topmost", True)

        self.title("Операции")
        self.geometry("900x650")
        self.resizable(False, False)

        # состояние
        self.selected_category_id = None
        self.sort_by = None          # "date" | "amount"
        self.sort_direction = 1      # 1 = ↑, -1 = ↓

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= FILTERS =================
        filter_frame = ctk.CTkFrame(self.frame)
        filter_frame.pack(fill="x", pady=(0, 10))

        self.type_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=list(TRANSACTION_TYPES.keys()),
            width=110
        )
        self.type_filter.set("Все")
        self.type_filter.pack(side="left", padx=5)

        ctk.CTkButton(
            filter_frame,
            text="Категория",
            width=110,
            command=self.open_category_filter
        ).pack(side="left", padx=5)

        self.date_from = ctk.CTkEntry(filter_frame, placeholder_text="Дата от", width=120)
        self.date_from.pack(side="left", padx=5)
        self.date_from.bind("<Button-1>", lambda e: DatePicker(self, self.date_from))

        self.date_to = ctk.CTkEntry(filter_frame, placeholder_text="Дата до", width=120)
        self.date_to.pack(side="left", padx=5)
        self.date_to.bind("<Button-1>", lambda e: DatePicker(self, self.date_to))
        self.date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ctk.CTkButton(
            filter_frame,
            text="Применить",
            width=120,
            command=self.apply_filter
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            filter_frame,
            text="Сбросить",
            width=120,
            command=self.reset_filters
        ).pack(side="left", padx=5)
        
        # ================= HEADER =================
        header = ctk.CTkFrame(self.frame, fg_color="#2b2b2b")
        header.pack(fill="x")

        self.date_label = ctk.CTkLabel(header, text="Дата ▲▼", width=120)
        self.date_label.pack(side="left")
        self.date_label.bind("<Button-1>", lambda e: self.sort("date"))

        ctk.CTkLabel(header, text="Категория", width=90).pack(side="left")

        self.amount_label = ctk.CTkLabel(header, text="Сумма ▲▼", width=120)
        self.amount_label.pack(side="left")
        self.amount_label.bind("<Button-1>", lambda e: self.sort("amount")) 

        ctk.CTkLabel(header, text="Комментарий").pack(side="left")


        # ================= TABLE =================
        self.table = ctk.CTkTextbox(
            self.frame,
            font=("Consolas", 13)
        )
        self.table.pack(fill="both", expand=True, pady=5)
        self.table.configure(state="disabled")

        # ================= TOTALS =================
        totals = ctk.CTkFrame(self.frame)
        totals.pack(fill="x", pady=(5, 5))

        self.income_var = ctk.StringVar(value="Доходы: +0.00 ₸")
        self.expense_var = ctk.StringVar(value="Расходы: -0.00 ₸")

        ctk.CTkLabel(totals, text="Итого:", font=ctk.CTkFont(size=14, weight="bold"))\
            .pack(side="left", padx=10)

        ctk.CTkLabel(totals, textvariable=self.income_var,
                     text_color=COLORS["income"]).pack(side="left", padx=20)

        ctk.CTkLabel(totals, textvariable=self.expense_var,
                     text_color=COLORS["expense"]).pack(side="left")

        # ================= EXPORT =================
        export_frame = ctk.CTkFrame(self.frame)
        export_frame.pack(fill="x", pady=(0, 5))

        ctk.CTkButton(
            export_frame,
            text="📤 Экспорт в Excel",
            height=40,
            command=self.export_excel
        ).pack(fill="x", padx=10)

        self.load_data()

    # ================= DATA =================

    def load_data(self):
        self.table.configure(state="normal")
        self.table.delete("1.0", "end")

        rows = get_transactions_filtered(
            transaction_type=TRANSACTION_TYPES[self.type_filter.get()],
            date_from=self.date_from.get() or None,
            date_to=self.date_to.get() or None,
            category_id=self.selected_category_id
        )

        # сортировка
        if self.sort_by:
            if self.sort_by == "amount":
                rows = sorted(
                    rows,
                    key=lambda r: (
                        0 if r["type"] == "expense" else 1,  # сначала расходы
                        float(r["amount"])
                    ),
                    reverse=self.sort_direction == -1
                )
            elif self.sort_by == "date":
                rows = sorted(
                    rows,
                    key=lambda r: datetime.strptime(r["date"], "%Y-%m-%d"),
                    reverse=self.sort_direction == -1
                )

        total_income = 0.0
        total_expense = 0.0

        for r in rows:
            amount = float(r["amount"])

            if r["type"] == "income":
                total_income += amount
                signed_amount = f"+{amount:.2f}"
                tag = "income"
            else:
                total_expense += amount
                signed_amount = f"-{amount:.2f}"
                tag = "expense"

            line = (
                f"{r['date']:<{COL_DATE}}"
                f"{r['category']:<{COL_CATEGORY}}"
                f"{signed_amount:>{COL_AMOUNT}}  "
                f"{r['comment']}\n"
            )

            self.table.insert("end", line, tag)


        self.table.tag_config("income", foreground=COLORS["income"])
        self.table.tag_config("expense", foreground=COLORS["expense"])
        self.table.configure(state="disabled")

        self.income_var.set(f"Доходы: +{total_income:.2f} ₸")
        self.expense_var.set(f"Расходы: -{total_expense:.2f} ₸")

    # ================= FILTERS =================

    def apply_filter(self):
        df = self.date_from.get()
        dt = self.date_to.get()

        if df and dt and dt < df:
            messagebox.showerror("Ошибка", "Дата «до» не может быть раньше даты «от»")
            return

        self.load_data()

    def reset_filters(self):
        self.type_filter.set("Все")
        self.selected_category_id = None

        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")
        self.date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.sort_by = None
        self.sort_direction = 1

        self.date_label.configure(text="Дата ▲▼")
        self.amount_label.configure(text="Сумма ▲▼")

        self.load_data()

    def open_category_filter(self):
        CategoryFilterWindow(self, self.set_category)

    def set_category(self, category_id):
        self.selected_category_id = category_id
        self.load_data()

    # ================= SORT =================

    def sort(self, field):
        if self.sort_by == field:
            self.sort_direction *= -1
        else:
            self.sort_by = field
            self.sort_direction = 1

        arrow = "▲" if self.sort_direction == 1 else "▼"
        self.date_label.configure(text=f"Дата {arrow if field=='date' else '▲▼'}")
        self.amount_label.configure(text=f"Сумма {arrow if field=='amount' else '▲▼'}")

        self.load_data()

    # ================= EXPORT =================

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not file_path:
            return

        export_transactions_to_excel(
            file_path=file_path,
            transaction_type=TRANSACTION_TYPES[self.type_filter.get()],
            date_from=self.date_from.get() or None,
            date_to=self.date_to.get() or None
        )
