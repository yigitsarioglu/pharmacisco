import sqlite3

class DrugDatabase:
    def __init__(self, db_path="drugs.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Drop old tables if they exist to force migration (dev mode)
        # In prod, we would use ALTER TABLE or ignore. 
        # Since schema changed significantly, recreate.
        cursor.execute("DROP TABLE IF EXISTS drug_barcodes") 
        # We need to check if 'drugs' has the old schema. 
        # Pragma check is safest, but for this task, let's assume valid re-init.
        # Checking if 'barcode' column exists:
        try:
            cursor.execute("SELECT barcode FROM drugs LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, likely old schema. Drop and recreate.
            cursor.execute("DROP TABLE IF EXISTS drugs")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                pregnancy_category TEXT,
                short_instruction TEXT,
                full_instruction TEXT
            )
        ''')
        
        # Check if empty
        cursor.execute('SELECT count(*) FROM drugs')
        if cursor.fetchone()[0] == 0:
            self.seed_data(cursor)
            
        conn.commit()
        conn.close()

    def seed_data(self, cursor):
        # Unified Data
        drugs = [
            (
                "8699717010109", # Barcode
                "YASMIN 21 FILM TABLET",
                "DOĞUM KONTROL İLACI",
                "X", # Pregnancy
                "GÜNDE 1 DEFA 1 TABLET BİR BARDAK SU İLE İÇİLECEK",
                "Her gün aynı saatte kullanın. Adet döngüsünün ilk günü ilaca başlanmalıdır. 21 Gün düzenli kullanımdan sonra 7 gün ara verilmelidir."
            ),
             (
                "8699809018091", # Barcode (Mock)
                "AMOKLAVIN 1000 MG",
                "ANTIBIYOTIK",
                "B", # Pregnancy
                "SABAH AKŞAM TOK KARNINA 1 TABLET",
                "12 saat ara ile alınız. Tedavi bitene kadar düzenli kullanınız."
            )
        ]
        cursor.executemany('''
            INSERT INTO drugs (barcode, name, category, pregnancy_category, short_instruction, full_instruction) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', drugs)

    def search(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Search by Name OR Barcode
        cursor.execute('''
            SELECT * FROM drugs 
            WHERE name LIKE ? OR barcode LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_all_drugs(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs ORDER BY name ASC")
        results = cursor.fetchall()
        conn.close()
        return results

    def add_drug(self, barcode, name, category, preg_cat, short_inst, full_inst):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drugs (barcode, name, category, pregnancy_category, short_instruction, full_instruction) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (barcode, name, category, preg_cat, short_inst, full_inst))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_drug(self, id, barcode, name, category, preg_cat, short_inst, full_inst):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Note: Updating barcode might fail if it conflicts, but we assume user knows.
        try:
            cursor.execute("""
                UPDATE drugs 
                SET barcode=?, name=?, category=?, pregnancy_category=?, short_instruction=?, full_instruction=?
                WHERE id=?
            """, (barcode, name, category, preg_cat, short_inst, full_inst, id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_drug_en(self, id, name_en, category_en, preg_cat, short_inst_en, full_inst_en):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE drugs 
                SET name_en=?, category_en=?, pregnancy_category=?, short_instruction_en=?, full_instruction_en=?
                WHERE id=?
            """, (name_en, category_en, preg_cat, short_inst_en, full_inst_en, id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_drug(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drugs WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return True

    def get_drug_by_barcode(self, barcode):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs WHERE barcode=?", (str(barcode),))
        result = cursor.fetchone()
        conn.close()
        return result

db = DrugDatabase()
