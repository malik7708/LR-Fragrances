import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    discount INTEGER DEFAULT 0,
    size TEXT NOT NULL,
    description TEXT,
    image TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone TEXT,
    address TEXT,
    payment_method TEXT,
    total_amount INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price INTEGER
);
                     -- Orders table (for tracking)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE,
    email TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Return requests
CREATE TABLE returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    email TEXT,
    reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- Customer support tickets 
CREATE TABLE support_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    subject TEXT,
    message TEXT,
    status TEXT DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);                                        
""")

conn.commit()
conn.close()

print("✅ Database created successfully")
