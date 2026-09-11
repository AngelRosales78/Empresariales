import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
print("=== DATABASE TABLES ===")
for t in cursor.fetchall():
    print(f"  - {t[0]}")

print("\n=== LIBRARY TABLE STRUCTURES ===")
for table in ['library_author', 'library_authorprofile', 'library_category', 'library_publisher', 'library_book', 'library_publication', 'library_book_categories']:
    try:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        print(f"\n  Table: {table}")
        for col in columns:
            print(f"    {col[1]:25s} {col[2]}")
    except:
        print(f"\n  Table: {table} - not found")

conn.close()
