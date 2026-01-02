# работа с данными

from database.db import get_connection


# ---------- CATEGORIES ----------

def add_category(name: str) -> bool:
    """
    Добавить новую категорию
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name.strip(),)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def delete_category(category_id: int) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_categories():
    """
    Получить все категории
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()
    conn.close()
    return categories


# ---------- TRANSACTIONS ----------

def add_transaction(
    transaction_type: str,
    amount: float,
    category_id: int,
    date: str,
    comment: str
) -> bool:
    """
    Добавить доход или расход
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions
            (type, amount, category_id, date, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (transaction_type, amount, category_id, date, comment.strip()))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_all_transactions():
    """
    Получить все операции
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            t.id,
            t.type,
            t.amount,
            t.date,
            t.comment,
            c.name AS category
        FROM transactions t
        JOIN categories c ON c.id = t.category_id
        ORDER BY t.date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------- BALANCE & REPORTS ----------

def get_balance() -> float:
    """
    Текущий баланс
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END)
        FROM transactions
    """)

    balance = cursor.fetchone()[0]
    conn.close()
    return balance if balance else 0.0


def get_sum_by_category(transaction_type: str):
    """
    Сумма по категориям
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.name,
            SUM(t.amount) as total
        FROM transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE t.type = ?
        GROUP BY c.name
        ORDER BY total DESC
    """, (transaction_type,))

    data = cursor.fetchall()
    conn.close()
    return data

def get_transactions_filtered(
    transaction_type=None,
    date_from=None,
    date_to=None,
    category_id=None
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            t.type,
            t.amount,
            t.date,
            t.comment,
            c.name AS category,
            c.id AS category_id
        FROM transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE 1=1
    """
    params = []

    if transaction_type:
        query += " AND t.type = ?"
        params.append(transaction_type)

    if date_from:
        query += " AND t.date >= ?"
        params.append(date_from)

    if date_to:
        query += " AND t.date <= ?"
        params.append(date_to)

    if category_id:
        query += " AND c.id = ?"
        params.append(category_id)

    query += " ORDER BY t.date DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

