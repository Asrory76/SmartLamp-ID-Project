from flask import render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from config import Config
import os

def get_db_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST, user=Config.DB_USER, 
        password=Config.DB_PASS, database=Config.DB_NAME
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_all_product_images():
    conn = get_db_connection()
    images = {}
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, image FROM products")
        for name, img in cursor.fetchall():
            images[name] = img
        cursor.close()
        conn.close()
    return images

def home():
    conn = get_db_connection()
    products = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
    return render_template("index.html", products=products)

def detail_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product: return render_template('404.html'), 404
    
    price_fmt = "{:,.0f}".format(product['price']).replace(',', '.')
    specs_list = [s.strip() for s in product['specs'].split(',')] if product['specs'] else []
    details = {'desc': product['description'], 'specs': specs_list, 'category': product['category']}
    
    return render_template("detail_product.html", product=product, name=product['name'], 
                           price=price_fmt, details=details, image=product['image'])

def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            flash(f"Selamat datang, {user['name']}!", "success")
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash("Login Gagal", "error")
    return render_template("login.html")

def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        pw_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, 'member')", (name, email, pw_hash))
            conn.commit()
            flash("Daftar Berhasil", "success")
            return redirect(url_for('login'))
        except:
            flash("Email sudah ada", "error")
        finally:
            conn.close()
    return render_template("register.html")

def logout():
    session.clear()
    flash("Anda telah logout.", "success")
    return redirect(url_for('home'))

def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    orders = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", orders=orders)

def cart():
    if "user_id" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cart_items WHERE user_id = %s", (session["user_id"],))
    cart_items = cursor.fetchall()
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    for item in cart_items:
        item['subtotal'] = item['price'] * item['quantity']
        item['price_fmt'] = "{:,.0f}".format(item['price']).replace(',', '.')
        item['subtotal_fmt'] = "{:,.0f}".format(item['subtotal']).replace(',', '.')
    conn.close()
    total_fmt = "{:,.0f}".format(total_price).replace(',', '.')
    return render_template("cart.html", cart=cart_items, total=total_fmt, product_images=get_all_product_images())

def add_to_cart(product_id):
    if "user_id" not in session: return redirect(url_for("login"))
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    if product:
        cursor.execute("SELECT * FROM cart_items WHERE user_id = %s AND product_name = %s", (user_id, product['name']))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE id = %s", (existing['id'],))
        else:
            cursor.execute("INSERT INTO cart_items (user_id, product_name, price, quantity) VALUES (%s, %s, %s, 1)", (user_id, product['name'], product['price']))
        conn.commit()
        flash("Masuk keranjang!", "success")
    conn.close()
    return redirect(request.referrer)

def update_cart(item_id, action):
    if "user_id" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT quantity FROM cart_items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if item:
        new_qty = item['quantity'] + 1 if action == "plus" else item['quantity'] - 1
        if new_qty < 1: cursor.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
        else: cursor.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (new_qty, item_id))
        conn.commit()
    conn.close()
    return redirect(url_for("cart"))

def delete_cart(item_id):
    if "user_id" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("cart"))

def beli(product_id):
    if "user_id" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product: return render_template('404.html'), 404
    harga_fmt = "{:,.0f}".format(product['price']).replace(',', '.')
    return render_template("checkout.html", product=product['name'], price=product['price'], price_display=harga_fmt, product_images=get_all_product_images())

def checkout_process():
    if "user_id" not in session: return redirect(url_for("login"))
    user_id = session["user_id"]
    p_name = request.form.get("product_name")
    price = request.form.get("price")
    method = request.form.get("payment_method")
    addr = request.form.get("address")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, product_name, price, payment_method, shipping_address) VALUES (%s,%s,%s,%s,%s)", 
                   (user_id, p_name, price, method, addr))
    conn.commit()
    conn.close()
    flash("Pembayaran Berhasil!", "success")
    return redirect(url_for("dashboard"))

def checkout_cart():
    if "user_id" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        addr = request.form.get("address")
        method = request.form.get("payment_method")
        cursor.execute("SELECT * FROM cart_items WHERE user_id = %s", (session["user_id"],))
        items = cursor.fetchall()
        for item in items:
            total = item['price'] * item['quantity']
            full_name = f"{item['product_name']} ({item['quantity']} pcs)"
            cursor.execute("INSERT INTO orders (user_id, product_name, price, payment_method, shipping_address) VALUES (%s,%s,%s,%s,%s)",
                           (session["user_id"], full_name, total, method, addr))
        cursor.execute("DELETE FROM cart_items WHERE user_id = %s", (session["user_id"],))
        conn.commit()
        conn.close()
        flash("Checkout Berhasil!", "success")
        return redirect(url_for("dashboard"))
        
    cursor.execute("SELECT * FROM cart_items WHERE user_id = %s", (session["user_id"],))
    cart_items = cursor.fetchall()
    total_raw = sum(item['price'] * item['quantity'] for item in cart_items)
    total_display = "{:,.0f}".format(total_raw).replace(',', '.')
    conn.close()
    return render_template("checkout_cart.html", cart=cart_items, total_display=total_display, product_images=get_all_product_images())

def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, subject, message) VALUES (%s,%s,%s,%s)", (name, email, subject, message))
        conn.commit()
        conn.close()
        flash("Pesan Terkirim!", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

def about():
    return render_template("about.html")

# -- ADMIN FUNCTIONS --
def admin_dashboard():
    if session.get("user_role") != "admin": return redirect(url_for("dashboard"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    conn.close()
    return render_template("admin.html", products=products)

def add_product():
    if session.get("user_role") != "admin": return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        cat = request.form.get("category")
        desc = request.form.get("description")
        specs = request.form.get("specs")
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, category, description, specs, image) VALUES (%s,%s,%s,%s,%s,%s)", 
                           (name, price, cat, desc, specs, filename))
            conn.commit()
            conn.close()
            flash("Produk Ditambah!", "success")
            return redirect(url_for("admin_dashboard"))
    return render_template("add_product.html")

def edit_product(product_id):
    if session.get("user_role") != "admin": return redirect(url_for("home"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        cat = request.form.get("category")
        desc = request.form.get("description")
        specs = request.form.get("specs")
        img_name = product['image']
        
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                img_name = filename
        
        cursor.execute("UPDATE products SET name=%s, price=%s, category=%s, description=%s, specs=%s, image=%s WHERE id=%s",
                       (name, price, cat, desc, specs, img_name, product_id))
        conn.commit()
        conn.close()
        flash("Produk Diupdate!", "success")
        return redirect(url_for("admin_dashboard"))
        
    conn.close()
    return render_template("edit_product.html", product=product)

def delete_product(product_id):
    if session.get("user_role") != "admin": return redirect(url_for("home"))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
    flash("Produk Dihapus!", "success")
    return redirect(url_for("admin_dashboard"))