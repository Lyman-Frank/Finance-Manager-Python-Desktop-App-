# типы транзакций (UI → DB)
TRANSACTION_TYPES = {
    "Все": None,
    "Доходы": "income",
    "Расходы": "expense"
}

# обратное отображение (DB → UI)
TRANSACTION_TYPES_REVERSE = {
    "income": "Доход",
    "expense": "Расход"
}

# цвета
COLORS = {
    "income": "#2ecc71",
    "expense": "#e74c3c"
}

# тексты
TEXTS = {
    "income_title": "Добавить доход",
    "expense_title": "Добавить расход",
    "total": "Итого",
    "export": "Экспорт в Excel",
    "apply": "Применить",
    "reset": "Сбросить"
}

# Фиксированная ширина столбцов
FIXED_WIDTHS = {
    "COL_DATE": 12,
    "COL_CATEGORY": 18,
    "COL_AMOUNT": 12
}