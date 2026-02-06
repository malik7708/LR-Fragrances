import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Check if columns exist
cursor.execute("PRAGMA table_info(orders)")
columns = [column[1] for column in cursor.fetchall()]

# Add missing columns if they don't exist
if "first_name" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN first_name TEXT")
    print("Added first_name column")

if "last_name" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN last_name TEXT")
    print("Added last_name column")

if "phone" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN phone TEXT")
    print("Added phone column")

if "address" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN address TEXT")
    print("Added address column")

if "city" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN city TEXT")
    print("Added city column")

if "postal_code" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN postal_code TEXT")
    print("Added postal_code column")

if "country" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN country TEXT")
    print("Added country column")

if "total" not in columns:
    cursor.execute("ALTER TABLE orders ADD COLUMN total INTEGER DEFAULT 0")
    print("Added total column")

conn.commit()
conn.close()
print("✅ Database migration completed!")
