import os
import sqlite3
from email.parser import Parser

ARCHIVE_DIR = os.path.join(os.getcwd(), "CCL_Archive")
DB_NAME = "ccl_archive.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Drop existing table if you want a clean start
    cursor.execute('DROP TABLE IF EXISTS ccl_messages')
    cursor.execute('''
        CREATE TABLE ccl_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT,
            month TEXT,
            day_file TEXT,
            subject TEXT,
            sender TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    return conn

def load_files_to_db():
    conn = setup_database()
    cursor = conn.cursor()
    email_parser = Parser()
    
    print(f"Reparsing files with Headers from: {ARCHIVE_DIR}")
    count = 0

    for year in sorted(os.listdir(ARCHIVE_DIR)):
        year_path = os.path.join(ARCHIVE_DIR, year)
        if not os.path.isdir(year_path): continue
            
        for month in sorted(os.listdir(year_path)):
            month_path = os.path.join(year_path, month)
            if not os.path.isdir(month_path): continue
                
            for filename in sorted(os.listdir(month_path)):
                if filename.endswith(".txt"):
                    file_path = os.path.join(month_path, filename)
                    
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            raw_content = f.read()
                        
                        # Parse headers
                        msg_obj = email_parser.parsestr(raw_content)
                        subject = msg_obj.get('Subject', '(No Subject)')
                        sender = msg_obj.get('From', '(Unknown Sender)')
                        
                        cursor.execute('''
                            INSERT INTO ccl_messages (year, month, day_file, subject, sender, content)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (year, month, filename.replace(".txt", ""), subject, sender, raw_content))
                        
                        count += 1
                        if count % 100 == 0:
                            print(f"Indexed {count} messages...")
                            
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")

    conn.commit()
    conn.close()
    print(f"Finished! Total messages loaded: {count}")

if __name__ == "__main__":
    load_files_to_db()
