import sqlite3
import uuid

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create a test order with all details
order_id = str(uuid.uuid4())[:8].upper()
email = "customer@example.com"
first_name = "Ahmed"
last_name = "Khan"
phone = "03001234567"
address = "123 Gulberg Lane"
city = "Lahore"
postal_code = "54000"
country = "Pakistan"
total = 4400  # 2 items

# Insert order
cursor.execute(
    """
    INSERT INTO orders (order_id, email, first_name, last_name, phone, address, city, postal_code, country, status, total)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        order_id,
        email,
        first_name,
        last_name,
        phone,
        address,
        city,
        postal_code,
        country,
        "processing",
        total,
    ),
)

order_db_id = cursor.lastrowid

# Get first two products to add as items
cursor.execute("SELECT id FROM products LIMIT 2")
products = cursor.fetchall()

# Add order items
for i, (product_id,) in enumerate(products):
    cursor.execute(
        """
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (?, ?, ?, ?)
    """,
        (order_db_id, product_id, 1, 2200),
    )

conn.commit()

print(f"✅ Test order created!")
print(f"Order ID: {order_id}")
print(f"Email: {email}")
print(f"Customer: {first_name} {last_name}")
print(f"Address: {address}, {city}, {postal_code}, {country}")
print(f"Phone: {phone}")
print(f"Total: Rs. {total}")
print(f"\nUse this Order ID to test the track order page")

conn.close()
