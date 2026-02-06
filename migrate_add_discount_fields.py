import sqlite3

DB_NAME = "database.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Add original_price and discount columns to order_items if they don't exist
cursor.execute("PRAGMA table_info(order_items)")
columns = [column[1] for column in cursor.fetchall()]

if "original_price" not in columns:
    cursor.execute(
        "ALTER TABLE order_items ADD COLUMN original_price INTEGER DEFAULT 0"
    )
    print("✓ Added original_price column to order_items")

if "discount" not in columns:
    cursor.execute("ALTER TABLE order_items ADD COLUMN discount INTEGER DEFAULT 0")
    print("✓ Added discount column to order_items")

conn.commit()
conn.close()

print("Migration complete!")
