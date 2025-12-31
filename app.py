from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "lr_fragrances_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/images/products'


# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
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


# ================= PRODUCT DETAIL (FIXED + RELATED) =================
@app.route("/product/<int:id>")
def product(id):
    db = get_db()

    product = db.execute(
        "SELECT * FROM products WHERE id = ?", (id,)
    ).fetchone()

    related = db.execute(
        "SELECT * FROM products WHERE id != ? ORDER BY RANDOM() LIMIT 4",
        (id,)
    ).fetchall()

    cart_count = sum(session.get("cart", {}).values())

    return render_template(
        "product.html",
        product=product,
        related=related,
        cart_count=cart_count
    )


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
    cart = session.get("cart", {})
    items = []
    total = 0

    if cart:
        db = get_db()
        for product_id, qty in cart.items():
            product = db.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()

            if product:
                price = product["price"] - (product["price"] * product["discount"] // 100)
                subtotal = price * qty
                total += subtotal

                items.append({
                    "product": product,
                    "qty": qty,
                    "subtotal": subtotal
                })

    cart_count = sum(cart.values())
    return render_template("cart.html", items=items, total=total, cart_count=cart_count)


# ================= UPDATE / REMOVE CART =================
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
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    cart_count = sum(session.get("cart", {}).values())
    return render_template("admin.html", products=products, cart_count=cart_count)


@app.route("/admin/delete/<int:id>")
def delete_product(id):
    db = get_db()
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


# ================= CONTACT =================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    cart_count = sum(session.get("cart", {}).values())

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        try:
            msg = EmailMessage()
            msg['Subject'] = f'New Contact Message from {name}'
            msg['From'] = email
            msg['To'] = "malikrehman7708@gmail.com"
            msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('your_gmail_account@gmail.com', 'your_app_password')
            server.send_message(msg)
            server.quit()

            flash("Message sent successfully!", "success")
        except Exception as e:
            print("Email error:", e)
            flash("Failed to send message.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html", cart_count=cart_count)
# ================= ORDER TRACKING =================
@app.route("/track-order", methods=["POST"])
def track_order():
    order_id = request.form["order_id"]

    db = get_db()
    order = db.execute(
        "SELECT * FROM orders WHERE order_id = ?", (order_id,)
    ).fetchone()

    if order:
        return render_template(
            "track_result.html",
            order=order
        )

    return render_template(
        "track_result.html",
        error="Order not found"
    )
# ================= RETURN REQUESTS =================
@app.route("/submit-return", methods=["POST"])
def submit_return():
    order_id = request.form["order_id"]
    email = request.form["email"]
    reason = request.form["reason"]

    db = get_db()
    db.execute(
        "INSERT INTO returns (order_id, email, reason) VALUES (?, ?, ?)",
        (order_id, email, reason)
    )
    db.commit()

    return redirect(url_for("customer_support"))
# ================= CUSTOMER SUPPORT TICKETS =================
@app.route("/submit-ticket", methods=["POST"])

def submit_ticket():
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    db = get_db()
    db.execute(
        "INSERT INTO support_tickets (email, subject, message) VALUES (?, ?, ?)",
        (email, subject, message)
    )
    db.commit()

    return redirect(url_for("customer_support"))
# ================= POLICIES =================
@app.route("/privacy-policy")
def privacy_policy():
    return render_template("policies/privacy.html")
# ================= POLICIES =================
@app.route("/shipping-policy")
def shipping_policy():
    return render_template("policies/shipping.html")
# ================= POLICIES =================
@app.route("/terms")
def terms():
    return render_template("policies/terms.html")
# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



