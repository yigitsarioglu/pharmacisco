import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drugs.db')

def update_schema():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    columns_to_add = [
        "name_en TEXT", "name_ru TEXT", "name_ar TEXT",
        "category_en TEXT", "category_ru TEXT", "category_ar TEXT",
        "short_instruction_en TEXT", "short_instruction_ru TEXT", "short_instruction_ar TEXT",
        "full_instruction_en TEXT", "full_instruction_ru TEXT", "full_instruction_ar TEXT"
    ]

    # Get existing columns
    cursor.execute("PRAGMA table_info(drugs)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    for col_def in columns_to_add:
        col_name = col_def.split()[0]
        if col_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE drugs ADD COLUMN {col_def}")
                print(f"Added column: {col_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding {col_name}: {e}")
        else:
            print(f"Column {col_name} already exists.")

    conn.commit()
    conn.close()
    print("Database schema update complete.")

if __name__ == "__main__":
    update_schema()
