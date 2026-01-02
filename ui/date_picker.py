import customtkinter as ctk
from tkcalendar import Calendar


class DatePicker(ctk.CTkToplevel):

    def __init__(self, parent, target_entry, min_date=None):
        super().__init__(parent)

        self.target_entry = target_entry

        self.title("Выбор даты")
        self.geometry("300x320")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.attributes("-topmost", True)

        self.calendar = Calendar(
            self,
            selectmode="day",
            date_pattern="yyyy-mm-dd",

            background="#1f1f1f",
            foreground="white",
            selectbackground="#1f6aa5",
            selectforeground="white",
            headersbackground="#1f1f1f",
            headersforeground="white",
            normalbackground="#2b2b2b",
            normalforeground="white",
            weekendbackground="#2b2b2b",
            weekendforeground="#e74c3c",
            othermonthbackground="#2b2b2b",
            othermonthforeground="#7f8c8d",
            bordercolor="#1f1f1f"
        )
        self.calendar.pack(padx=10, pady=10)

        if min_date:
            self.calendar.config(mindate=min_date)

        ctk.CTkButton(
            self,
            text="Выбрать",
            command=self.select_date
        ).pack(pady=10)

    def select_date(self):
        date = self.calendar.get_date()
        self.target_entry.delete(0, "end")
        self.target_entry.insert(0, date)
        self.destroy()
