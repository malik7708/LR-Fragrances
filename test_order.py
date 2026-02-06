import sqlite3

conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get first order
cursor.execute("SELECT * FROM orders LIMIT 1")
order = cursor.fetchone()

if order:
    print(f"\n{'='*50}")
    print(f"Order ID: {order['order_id']}")
    print(f"Email: {order['email']}")
    print(f"First Name: {order['first_name']}")
    print(f"Last Name: {order['last_name']}")
    print(f"Address: {order['address']}")
    print(f"City: {order['city']}")
    print(f"Phone: {order['phone']}")
    print(f"Total: {order['total']}")
    print(f"Status: {order['status']}")
    print(f"{'='*50}")

    # Get items for this order
    cursor.execute(
        """
        SELECT oi.*, p.name 
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """,
        (order["id"],),
    )

    items = cursor.fetchall()
    print(f"\nItems in order ({len(items)}):")
    total_calc = 0
    for item in items:
        subtotal = item["price"] * item["quantity"]
        total_calc += subtotal
        print(
            f"  - {item['name']}: {item['quantity']} × Rs.{item['price']} = Rs.{subtotal}"
        )
    print(f"\nCalculated Total: Rs.{total_calc}")
else:
    print("No orders found")

conn.close()
