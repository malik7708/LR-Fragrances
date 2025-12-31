import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO products (name, price, discount, size, description, image)
VALUES
('Black Wood', 3000, 35, '100ml', 'Luxury woody fragrance', 'perfume1.jpg'),
('Pearl Essance', 2500, 30, '100ml', 'Deep amber luxury fragrance', 'perfume2.jpg')
""")

conn.commit()
conn.close()

print("✅ Products added successfully")
import sqlite3

conn = sqlite3.connect("database.db")   # use your real DB name
cursor = conn.cursor()

cursor.execute("""
INSERT INTO products (name, price, discount, size, description, image)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    'Sky line',
    2500,
    30,
    '100ml',
    'Deep amber luxury fragrance',
    'perfume3.jpg'
))

conn.commit()
conn.close()

print("✅ Paragon Night added successfully")

import sqlite3

conn = sqlite3.connect("database.db")   # use your real DB name
cursor = conn.cursor()

cursor.execute("""
INSERT INTO products (name, price, discount, size, description, image)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    'Strom Cheaser',
    2500,
    30,
    '100ml',
    'Deep amber luxury fragrance',
    'perfume4.jpg'
))

conn.commit()
conn.close()

print("✅ Paragon Night added successfully")
import sqlite3

conn = sqlite3.connect("database.db")   # use your real DB name
cursor = conn.cursor()

cursor.execute("""
INSERT INTO products (name, price, discount, size, description, image)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    'Paragon',
    2500,
    30,
    '100ml',
    'Deep amber luxury fragrance',
    'perfume5.jpg'
))

conn.commit()
conn.close()

print("✅ Paragon Night added successfully")

