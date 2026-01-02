# фильтр категорий

import customtkinter as ctk
from database.crud import get_categories


class CategoryFilterWindow(ctk.CTkToplevel):

    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.on_select = on_select

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.attributes("-topmost", True)

        self.title("Фильтр по категории")
        self.geometry("300x370")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Категория",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        self.selected_id = None
        self.buttons = []

        self.list_frame = ctk.CTkScrollableFrame(frame, height=200)
        self.list_frame.pack(fill="x")

        # ⬇️ ВАЖНО: добавляем "Все"
        categories = [{"id": None, "name": "Все"}] + get_categories()

        for c in categories:
            btn = ctk.CTkButton(
                self.list_frame,
                text=c["name"],
                fg_color="transparent",
                anchor="w",
                command=lambda cid=c["id"]: self.select(cid)
            )
            btn.category_id = c["id"]
            btn.pack(fill="x", pady=2)
            self.buttons.append(btn)

        ctk.CTkButton(
            frame,
            text="Применить",
            command=self.apply
        ).pack(fill="x", pady=15)
        
    def select(self, category_id):
        self.selected_id = category_id

        for btn in self.buttons:
            if btn.category_id == category_id:
                btn.configure(fg_color="#1f6aa5")
            else:
                btn.configure(fg_color="transparent")

    def apply(self):
        self.on_select(self.selected_id)
        self.destroy()
