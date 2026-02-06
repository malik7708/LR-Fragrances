import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Check orders table
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="orders"')
result = cursor.fetchone()
if result:
    print('Orders table exists')
    cursor.execute('SELECT COUNT(*) FROM orders')
    count = cursor.fetchone()[0]
    print(f'Orders count: {count}')

    # Check recent orders
    cursor.execute('SELECT * FROM orders ORDER BY id DESC LIMIT 5')
    orders = cursor.fetchall()
    print(f'Recent orders: {orders}')
else:
    print('Orders table does not exist')

# Check products table
cursor.execute('SELECT COUNT(*) FROM products')
product_count = cursor.fetchone()[0]
print(f'Products count: {product_count}')

# Check order_items table
cursor.execute('SELECT COUNT(*) FROM order_items')
item_count = cursor.fetchone()[0]
print(f'Order items count: {item_count}')

conn.close()