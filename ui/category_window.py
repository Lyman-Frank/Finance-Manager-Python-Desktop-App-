# категории

import customtkinter as ctk
from database.crud import get_categories, add_category, delete_category


class CategoryWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        # modal
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.attributes("-topmost", True)

        self.title("Категории")
        self.geometry("360x450")
        self.resizable(False, False)

        self.selected_category_id = None
        self.category_buttons = []

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------- TITLE ----------
        ctk.CTkLabel(
            self.frame,
            text="Категории",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 10))

        # ---------- CATEGORY LIST ----------
        self.list_frame = ctk.CTkScrollableFrame(
            self.frame,
            height=200
        )
        self.list_frame.pack(fill="x", pady=(0, 10))

        # ---------- ADD CATEGORY ----------
        self.entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Новая категория"
        )
        self.entry.pack(fill="x", pady=1)

        self.status = ctk.CTkLabel(
            self.frame,
            text="",
            text_color="#e74c3c"
        )
        self.status.pack(pady=(0, 5))

        ctk.CTkButton(
            self.frame,
            text="➕ Добавить",
            fg_color="#2ecc71",
            command=self.add_category
        ).pack(fill="x", pady=5)

        ctk.CTkButton(
            self.frame,
            text="🗑 Удалить выбранную",
            fg_color="#c0392b",
            command=self.delete_category
        ).pack(fill="x", pady=(0, 5))

        self.refresh()

    # ---------- RENDER ----------

    def refresh(self):
        # очистка
        for btn in self.category_buttons:
            btn.destroy()

        self.category_buttons.clear()
        self.selected_category_id = None

        self.categories = get_categories()

        if not self.categories:
            ctk.CTkLabel(
                self.list_frame,
                text="Категорий нет",
                text_color="gray"
            ).pack(pady=10)
            return

        for c in self.categories:
            btn = ctk.CTkButton(
                self.list_frame,
                text=c["name"],
                fg_color="transparent",
                anchor="w",
                command=lambda cid=c["id"], b=None: self.select_category(cid)
            )

            btn.pack(fill="x", pady=2)
            self.category_buttons.append(btn)

    # ---------- SELECTION ----------

    def select_category(self, category_id):
        self.selected_category_id = category_id
        self.status.configure(text="")

        for btn, cat in zip(self.category_buttons, self.categories):
            if cat["id"] == category_id:
                btn.configure(fg_color="#1f6aa5")
            else:
                btn.configure(fg_color="transparent")

    # ---------- ACTIONS ----------

    def add_category(self):
        name = self.entry.get().strip()
        if not name:
            return

        if add_category(name):
            self.entry.delete(0, "end")
            self.status.configure(text="")
            self.refresh()
        else:
            self.status.configure(text="Категория уже существует")

    def delete_category(self):
        if not self.selected_category_id:
            self.status.configure(text="Выберите категорию")
            return

        if delete_category(self.selected_category_id):
            self.status.configure(text="")
            self.refresh()
        else:
            self.status.configure(text="Категория используется")
