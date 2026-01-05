import sqlite3
import os

def create_database_from_sql_files(db_name, schema_file, data_file):
    try:
        if os.path.exists(db_name):
            os.remove(db_name)
            print("...Η παλιά βάση δεδομένων διαγράφηκε.")
            
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)
            print("...Πίνακες δημιουργήθηκαν επιτυχώς.")

        with open(data_file, 'r', encoding='utf-8') as f:
            data_sql = f.read()
            cursor.executescript(data_sql)
            print("...Δεδομένα εισήχθησαν επιτυχώς.")

        conn.commit()
        conn.close()
        print("\nSUCCESS: Δημιουργήθηκε νέα βάση δεδομένων με πίνακες και δεδομένα.")

    except sqlite3.Error as e:
        print(f"\nERROR: An error occurred with SQLite: {e}")
    except FileNotFoundError as e:
        print(f"\nERROR: File not found: {e}")
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")

if __name__ == "__main__":

    DB_NAME = "NEWflightmanagement.db"
    SCHEMA_FILE = "dhmiourgiapinakwn.sql"  
    DATA_FILE = "NEWData.sql"              

    create_database_from_sql_files(DB_NAME, SCHEMA_FILE, DATA_FILE)