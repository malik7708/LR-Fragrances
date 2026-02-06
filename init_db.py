import sqlite3
import hashlib

DB_NAME = "database.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.executescript(
    """
PRAGMA foreign_keys = ON;

-- ================= PRODUCTS =================
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    discount INTEGER DEFAULT 0,
    size TEXT NOT NULL,
    description TEXT,
    image TEXT
);

-- ================= ORDERS =================
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    postal_code TEXT,
    country TEXT,
    status TEXT DEFAULT 'pending',
    total INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ================= ORDER ITEMS =================
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ================= RETURNS =================
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    email TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ================= SUPPORT =================
CREATE TABLE IF NOT EXISTS support_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ================= ADMINS =================
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
                     
-- ================= REVIEWS =================
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
"""
)

# ================= DEFAULT ADMIN =================
cursor.execute("SELECT id FROM admins WHERE username = ?", ("admin",))
if not cursor.fetchone():
    password = "admin123"
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
        ("admin", password_hash),
    )
    print("✅ Default admin created (admin / admin123)")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
