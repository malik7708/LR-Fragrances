from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
import smtplib
from email.message import EmailMessage
import os
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "lr_fragrances_secret_key"
app.config["UPLOAD_FOLDER"] = "static/images/products"


# ================= PASSWORD HASHING FUNCTION =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ================= DATABASE =================
def get_db():
    """Return a sqlite3 connection with row_factory set to sqlite3.Row.
    Use this everywhere so templates can access columns by name."""
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ================= HOME =================
@app.route("/")
def home():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("index.html", cart_count=cart_count)


# ================= SHOP =================
@app.route("/shop")
def shop():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    cart_count = sum(session.get("cart", {}).values())
    return render_template("shop.html", products=products, cart_count=cart_count)


# ================= PRODUCT DETAIL =================
@app.route("/product/<int:id>")
def product(id):
    db = get_db()

    product = db.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()

    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("shop"))

    related = db.execute(
        "SELECT * FROM products WHERE id != ? ORDER BY RANDOM() LIMIT 4", (id,)
    ).fetchall()

    reviews = db.execute(
        """
        SELECT username, rating, comment, created_at
        FROM reviews
        WHERE product_id = ?
        ORDER BY created_at DESC
        """,
        (id,),
    ).fetchall()

    avg_rating = db.execute(
        "SELECT ROUND(AVG(rating), 1) FROM reviews WHERE product_id = ?", (id,)
    ).fetchone()[0]

    cart_count = sum(session.get("cart", {}).values())

    return render_template(
        "product.html",
        product=product,
        related=related,
        reviews=reviews,
        avg_rating=avg_rating,
        cart_count=cart_count,
    )


# ================= ADD REVIEW =================
@app.route("/product/<int:product_id>/review", methods=["POST"])
def add_review(product_id):
    db = get_db()

    rating = int(request.form["rating"])
    comment = request.form.get("review", "").strip()
    username = request.form.get("name", "Verified Buyer")

    if rating < 1 or rating > 5:
        flash("Invalid rating value.", "error")
        return redirect(url_for("product", id=product_id))

    db.execute(
        """
        INSERT INTO reviews (product_id, username, rating, comment)
        VALUES (?, ?, ?, ?)
        """,
        (product_id, username, rating, comment),
    )

    db.commit()
    flash("Thank you! Your review has been submitted.", "success")

    return redirect(url_for("product", id=product_id))


# ================= ADD TO CART =================
@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))


# ================= CART =================
@app.route("/cart")
def cart():
    try:
        cart = session.get("cart", {})
        items = []
        total = 0

        if cart:
            db = get_db()
            for product_id, qty in cart.items():
                product = db.execute(
                    "SELECT * FROM products WHERE id = ?", (product_id,)
                ).fetchone()

                if product:
                    price = product["price"] - (
                        product["price"] * product["discount"] // 100
                    )
                    subtotal = price * qty
                    total += subtotal

                    items.append({"product": product, "qty": qty, "subtotal": subtotal})

        cart_count = sum(cart.values())
        return render_template(
            "cart.html", items=items, total=total, cart_count=cart_count
        )
    except Exception as e:
        print(f"Error in cart route: {e}")
        flash("An error occurred loading your cart.", "error")
        return redirect(url_for("shop"))


# ================= CHECKOUT =================
def checkout():
    try:
        cart = session.get("cart", {})

        # Check if cart is empty
        if not cart:
            flash(
                "Your cart is empty. Please add items to your cart before checkout.",
                "error",
            )
            return redirect(url_for("shop"))

        items = []
        total = 0

        if cart:
            db = get_db()
            for product_id, qty in cart.items():
                product = db.execute(
                    "SELECT * FROM products WHERE id = ?", (product_id,)
                ).fetchone()

                if product:
                    price = product["price"] - (
                        product["price"] * product["discount"] // 100
                    )
                    subtotal = price * qty
                    total += subtotal

                    items.append({"product": product, "qty": qty, "subtotal": subtotal})

        cart_count = sum(session.get("cart", {}).values())
        return render_template(
            "checkout.html", items=items, total=total, cart_count=cart_count
        )
    except Exception as e:
        print(f"Error in checkout route: {e}")
        import traceback

        traceback.print_exc()
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for("cart"))


app.add_url_rule("/checkout", "checkout", checkout)


# ================= PROCESS PAYMENT =================
@app.route("/process-payment", methods=["POST"])
def process_payment():

    # -------- GET FORM DATA --------
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    city = request.form.get("city")
    postal_code = request.form.get("postal_code")
    country = request.form.get("country")
    payment_method = request.form.get("payment_method")
    jazzcash_number = request.form.get("jazzcash_number")
    jazzcash_cnic = request.form.get("jazzcash_cnic")

    # -------- CHECK CART --------
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty. Please add items before checkout.", "error")
        return redirect(url_for("shop"))

    # -------- CALCULATE TOTAL --------
    items = []
    total = 0
    db = get_db()

    for product_id, qty in cart.items():
        product = db.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()

        if product:
            price = product["price"] - (product["price"] * product["discount"] // 100)
            subtotal = price * qty
            total += subtotal

            items.append(
                {
                    "product_id": product_id,
                    "quantity": qty,
                    "price": price,
                    "original_price": product["price"],
                    "discount": product["discount"],
                }
            )

    # -------- ORDER ID --------
    import uuid

    order_id = str(uuid.uuid4())[:8].upper()

    # -------- PAYMENT LOGIC --------
    payment_success = payment_method in ["jazzcash", "cod"]

    if not payment_success:
        flash("Payment failed. Please try again.", "error")
        return redirect(url_for("checkout"))

    try:
        # -------- SAVE ORDER --------
        order_status = (
            "processing" if payment_method == "jazzcash" else "Pay on Delivery"
        )

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO orders (order_id, email, first_name, last_name, phone, address, city, postal_code, country, status, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                order_status,
                total,
            ),
        )
        order_db_id = cursor.lastrowid

        for item in items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price, original_price, discount) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    order_db_id,
                    item["product_id"],
                    item["quantity"],
                    item["price"],
                    item["original_price"],
                    item["discount"],
                ),
            )

        db.commit()

        # -------- CUSTOMER EMAIL --------
        try:
            msg = EmailMessage()
            msg["Subject"] = f"Order Confirmation - {order_id}"
            msg["From"] = "lrfragrancess@gmail.com"
            msg["To"] = email

            msg.set_content(
                f"""
Thank you for your order!

Order ID: {order_id}
Total: PKR {total}
Payment Method: {"JazzCash" if payment_method == "jazzcash" else "Cash on Delivery"}

Your order is being processed.

LR Fragrances
"""
            )

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("lrfragrancess@gmail.com", "eieluxywznvztihm")
            server.send_message(msg)
            server.quit()

        except Exception as e:
            print("Customer email error:", e)

        # -------- ADMIN ORDER NOTIFICATION --------
        try:
            admin_msg = EmailMessage()
            admin_msg["Subject"] = f"🛒 New Order Received - {order_id}"
            admin_msg["From"] = "lrfragrancess@gmail.com"
            admin_msg["To"] = "lrfragrancess@gmail.com"

            admin_msg.set_content(
                f"""
NEW ORDER RECEIVED

Order ID: {order_id}
Customer: {first_name} {last_name}
Email: {email}
Phone: {phone}

Address:
{address}, {city}, {postal_code}, {country}

Payment Method: {"JazzCash" if payment_method == "jazzcash" else "Cash on Delivery"}
Total Amount: PKR {total}

ITEMS:
"""
                + "\n".join(
                    [
                        f"- Product ID: {i['product_id']} | Qty: {i['quantity']} | Price: PKR {i['price']}"
                        for i in items
                    ]
                )
            )

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("lrfragrancess@gmail.com", "eieluxywznvztihm")
            server.send_message(admin_msg)
            server.quit()

        except Exception as e:
            print("Admin email error:", e)

        # -------- CLEAR CART --------
        session.pop("cart", None)

        flash("Order placed successfully! Confirmation email sent.", "success")
        return redirect(url_for("order_confirmation", order_id=order_id))

    except Exception as e:
        db.rollback()
        print("ORDER ERROR:", e)
        flash("Failed to place order. Please try again.", "error")
        return redirect(url_for("checkout"))


# ================= ORDER CONFIRMATION =================
@app.route("/order-confirmation/<order_id>")
def order_confirmation(order_id):
    db = get_db()

    order = db.execute(
        "SELECT * FROM orders WHERE order_id = ?", (order_id,)
    ).fetchone()

    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("shop"))

    # Fetch order items with product details including discount
    raw_items = db.execute(
        """
        SELECT 
            oi.quantity,
            oi.price,
            p.name,
            p.image,
            p.price as original_price,
            p.discount
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """,
        (order["id"],),
    ).fetchall()

    # Build template-friendly data
    order_items = []
    total = 0

    for item in raw_items:
        subtotal = item["price"] * item["quantity"]
        total += subtotal

        order_items.append(
            {
                "product": {
                    "name": item["name"],
                    "image": item["image"],
                    "original_price": item["original_price"],
                    "discount": item["discount"],
                },
                "quantity": item["quantity"],
                "price": item["price"],
            }
        )

    cart_count = sum(session.get("cart", {}).values())
    return render_template(
        "order_confirmation.html",
        order={
            "order_id": order["order_id"],
            "created_at": order["created_at"],
            "status": order["status"],
            "email": order["email"],
            "total": total,
        },
        order_items=order_items,
        cart_count=cart_count,
    )


# ================= TRACK ORDER PAGE =================
@app.route("/track-order-page")
def track_order_page():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("track_order.html", cart_count=cart_count, total_discount=0)


@app.route("/update-cart/<int:product_id>/<action>")
def update_cart(product_id, action):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        if action == "increase":
            cart[pid] += 1
        elif action == "decrease":
            cart[pid] -= 1

        if cart[pid] <= 0:
            del cart[pid]

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("cart"))


# ================= ADMIN =================
@app.route("/admin")
def admin():
    # require admin session; if not logged in, show the login page inline
    if not session.get("is_admin"):
        # render the admin login form directly so clicks to /admin always prompt for password
        return render_template("admin_login.html")

    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()

    # Stats
    total_products = db.execute("SELECT COUNT(*) as count FROM products").fetchone()[
        "count"
    ]
    total_orders = db.execute("SELECT COUNT(*) as count FROM orders").fetchone()[
        "count"
    ]
    total_revenue = (
        db.execute(
            "SELECT SUM(price * quantity) as revenue FROM order_items"
        ).fetchone()["revenue"]
        or 0
    )
    pending_returns = db.execute("SELECT COUNT(*) as count FROM returns").fetchone()[
        "count"
    ]
    open_tickets = db.execute(
        "SELECT COUNT(*) as count FROM support_tickets WHERE status = 'open'"
    ).fetchone()["count"]

    # Recent orders
    recent_orders = db.execute(
        """
        SELECT o.*, COUNT(oi.id) as item_count, SUM(oi.price * oi.quantity) as total
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        GROUP BY o.id
        ORDER BY o.created_at DESC
        LIMIT 10
    """
    ).fetchall()

    cart_count = sum(session.get("cart", {}).values())
    return render_template(
        "admin.html",
        products=products,
        cart_count=cart_count,
        stats={
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "pending_returns": pending_returns,
            "open_tickets": open_tickets,
        },
        recent_orders=recent_orders,
    )


@app.route("/admin/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product_page(id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()

    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("admin"))

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price", type=int)
        discount = request.form.get("discount", type=int, default=0)
        size = request.form.get("size")
        description = request.form.get("description", "")

        db.execute(
            """
            UPDATE products 
            SET name = ?, price = ?, discount = ?, size = ?, description = ?
            WHERE id = ?
            """,
            (name, price, discount, size, description, id),
        )
        db.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("admin"))

    cart_count = sum(session.get("cart", {}).values())
    return render_template(
        "edit_product.html",
        product=product,
        cart_count=cart_count,
    )


@app.route("/admin/edit/<int:id>", methods=["POST"])
def edit_product(id):
    if not session.get("is_admin"):
        return {"success": False, "error": "Unauthorized"}, 401

    try:
        name = request.form.get("name")
        price = request.form.get("price", type=int)
        discount = request.form.get("discount", type=int, default=0)
        size = request.form.get("size")
        description = request.form.get("description", "")

        db = get_db()

        # Update product
        db.execute(
            """
            UPDATE products 
            SET name = ?, price = ?, discount = ?, size = ?, description = ?
            WHERE id = ?
            """,
            (name, price, discount, size, description, id),
        )
        db.commit()

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500


@app.route("/admin/delete/<int:id>")
def delete_product(id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    db = get_db()
    # remove image file if present
    product = db.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()
    if product and product["image"]:
        try:
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], product["image"]))
        except Exception:
            pass

    db.execute("DELETE FROM products WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("admin"))


# ================= ABOUT =================
@app.route("/about")
def about():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("about.html", cart_count=cart_count)


# ================= SUPPORT =================
@app.route("/support")
def support():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("support.html", cart_count=cart_count)


# Temporary debug routes
@app.route("/__ping__")
def _ping():
    return "pong"


@app.route("/__routes__")
def _routes():
    # Return a plain-text list of registered routes for debugging
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.rule} -> {rule.endpoint}")
    return "\n".join(sorted(routes)), 200, {"Content-Type": "text/plain; charset=utf-8"}


# Customer support alias used by some redirects in the app
@app.route("/customer-support")
def customer_support():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("support.html", cart_count=cart_count)


# ================= CONTACT =================
from email.message import EmailMessage
import smtplib


@app.route("/contact", methods=["GET", "POST"])
def contact():
    cart_count = sum(session.get("cart", {}).values())

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        try:
            msg = EmailMessage()
            msg["Subject"] = f"New Customer Message – LR Fragrances"
            msg["From"] = "lrfragrancess@gmail.com"  # ✅ YOUR email
            msg["To"] = "lrfragrancess@gmail.com"  # ✅ WHERE YOU RECEIVE
            msg["Reply-To"] = email  # ✅ Customer reply

            msg.set_content(
                f"""
New Customer Message

Name: {name}
Email: {email}

Message:
{message}
                """
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("lrfragrancess@gmail.com", "eieluxywznvztihm")
                server.send_message(msg)

            flash("Message sent successfully!", "success")

        except Exception as e:
            print("Email error:", e)
            flash("Failed to send message. Try again.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html", cart_count=cart_count)


# ================= ORDER TRACKING =================
@app.route("/track-order", methods=["GET", "POST"])
def track_order():
    if request.method == "GET":
        cart_count = sum(session.get("cart", {}).values())
        return render_template(
            "track_order.html", cart_count=cart_count, total_discount=0
        )

    order_id = request.form["order_id"]

    db = get_db()
    order = db.execute(
        "SELECT * FROM orders WHERE order_id = ?", (order_id,)
    ).fetchone()

    cart_count = sum(session.get("cart", {}).values())

    if order:
        # Fetch order items with product details including discount
        raw_items = db.execute(
            """
            SELECT 
                oi.quantity,
                oi.price,
                oi.original_price,
                oi.discount,
                p.name,
                p.image
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """,
            (order["id"],),
        ).fetchall()

        # Build template-friendly data
        order_items = []
        total = 0
        total_discount = 0

        for item in raw_items:
            subtotal = item["price"] * item["quantity"]
            total += subtotal

            # Calculate discount using stored original_price
            if item["discount"] > 0 and item["original_price"] > 0:
                discount_per_item = item["original_price"] - item["price"]
                item_discount = discount_per_item * item["quantity"]
                total_discount += item_discount

            order_items.append(
                {
                    "product": {
                        "name": item["name"],
                        "image": item["image"],
                        "original_price": item["original_price"],
                        "discount": item["discount"],
                    },
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "subtotal": subtotal,
                }
            )

        # If order total is 0 in database, use calculated total
        final_total = total if total > 0 else order.get("total", 0)

        return render_template(
            "track_order.html",
            order=order,
            order_items=order_items,
            order_total=final_total,
            total_discount=total_discount,
            cart_count=cart_count,
        )

    return render_template(
        "track_order.html",
        error="Order not found",
        cart_count=cart_count,
        total_discount=0,
    )


# ================= RETURN REQUESTS =================
@app.route("/submit-return", methods=["POST"])
def submit_return():
    order_id = request.form.get("order_id")
    email = request.form.get("email")
    reason = request.form.get("reason")

    try:
        # Save to database
        db = get_db()
        db.execute(
            "INSERT INTO returns (order_id, email, reason) VALUES (?, ?, ?)",
            (order_id, email, reason),
        )
        db.commit()

        # Send email to support
        msg = EmailMessage()
        msg["Subject"] = f"New Return Request | Order #{order_id}"
        msg["From"] = "lrfragrancess@gmail.com"
        msg["To"] = "lrfragrancess@gmail.com"
        msg.set_content(
            f"""
New Return Request Received

Order ID: {order_id}
Customer Email: {email}

Reason:
{reason}
"""
        )

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("lrfragrancess@gmail.com", "eieluxywznvztihm")
        server.send_message(msg)
        server.quit()

        flash("Your return request has been submitted successfully.", "success")

    except Exception as e:
        print("RETURN REQUEST ERROR:", e)
        flash("Failed to submit return request. Please try again.", "error")

    return redirect(url_for("support"))


# ================= INITIALIZE DATABASE =================
import init_db

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# ================= CUSTOMER SUPPORT TICKETS =================
@app.route("/submit-ticket", methods=["POST"])
def submit_ticket():
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    db = get_db()
    db.execute(
        "INSERT INTO support_tickets (email, subject, message) VALUES (?, ?, ?)",
        (email, subject, message),
    )
    db.commit()

    return redirect(url_for("customer_support"))


# ================= ADMIN: ADD PRODUCT =================
@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))
    # Get form fields
    name = request.form.get("name")
    price = request.form.get("price") or 0
    discount = request.form.get("discount") or 0
    size = request.form.get("size")
    description = request.form.get("description")

    # Handle image upload
    image_file = request.files.get("image")
    filename = None
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(save_path)

    # Insert into DB
    db = get_db()
    db.execute(
        "INSERT INTO products (name, price, discount, size, description, image) VALUES (?, ?, ?, ?, ?, ?)",
        (name, int(price), int(discount), size, description, filename),
    )
    db.commit()

    return redirect(url_for("admin"))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password required", "error")
            return redirect(url_for("admin_login"))

        db = get_db()
        admin = db.execute(
            "SELECT * FROM admins WHERE username = ?", (username,)
        ).fetchone()

        if admin and admin["password_hash"] == hash_password(password):
            session["is_admin"] = True
            session["admin_username"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


@app.route("/admin-logout")
def admin_logout():
    session.pop("is_admin", None)
    session.pop("admin_username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))


# ================= ADMIN: CHANGE PASSWORD =================
@app.route("/admin/change-password", methods=["GET", "POST"])
def change_password():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        username = session.get("admin_username")
        old_password = request.form.get("old_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not old_password or not new_password or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for("change_password"))

        if new_password != confirm_password:
            flash("New passwords do not match", "error")
            return redirect(url_for("change_password"))

        if len(new_password) < 6:
            flash("Password must be at least 6 characters", "error")
            return redirect(url_for("change_password"))

        db = get_db()
        admin = db.execute(
            "SELECT * FROM admins WHERE username = ?", (username,)
        ).fetchone()

        if admin and admin["password_hash"] == hash_password(old_password):
            db.execute(
                "UPDATE admins SET password_hash = ? WHERE username = ?",
                (hash_password(new_password), username),
            )
            db.commit()
            flash("Password changed successfully!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Old password is incorrect", "error")
            return redirect(url_for("change_password"))

    return render_template("change_password.html")


# ================= ADMIN: EDIT PRODUCT =================
@app.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def admin_edit(id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("admin"))

    if request.method == "POST":
        name = request.form.get("name")
        price = int(request.form.get("price") or 0)
        discount = int(request.form.get("discount") or 0)
        size = request.form.get("size")
        description = request.form.get("description")

        image_file = request.files.get("image")
        filename = product["image"]
        if image_file and image_file.filename:
            # remove old image
            if product["image"]:
                try:
                    os.remove(
                        os.path.join(app.config["UPLOAD_FOLDER"], product["image"])
                    )
                except Exception:
                    pass
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db.execute(
            "UPDATE products SET name=?, price=?, discount=?, size=?, description=?, image=? WHERE id=?",
            (name, price, discount, size, description, filename, id),
        )
        db.commit()
        return redirect(url_for("admin"))

    return render_template("admin_edit.html", product=product)


# ================= POLICIES =================
@app.route("/privacy-policy")
def privacy_policy():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("policies/privacy.html", cart_count=cart_count)


# ================= POLICIES =================
@app.route("/shipping-policy")
def shipping_policy():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("policies/shipping.html", cart_count=cart_count)


# ================= POLICIES =================
@app.route("/terms")
def terms():
    cart_count = sum(session.get("cart", {}).values())
    return render_template("policies/terms.html", cart_count=cart_count)


# ================= RUN =================
if __name__ == "__main__":
    # Debug instrumentation: print startup marker and catch exceptions
    print("[LR FRAGRANCES] Starting app.py -- entering __main__")
    try:
        # Disable the auto-reloader to avoid importlib.metadata scanning issues
        # that can hang in some Windows/virtualenv setups. Keep debug logging on.
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except Exception:
        import traceback

        traceback.print_exc()
        print("[LR FRAGRANCES] app.run raised an exception; see traceback above")
