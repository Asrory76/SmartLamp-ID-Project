from app import app
from app.controller import UserController, ProductController, WebController
from flask import request

#  JALUR API (UNTUK POSTMAN)

# 1. API Users
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET': return UserController.index()
    else: return UserController.store()

@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(id):
    if request.method == 'GET': return UserController.show(id)
    elif request.method == 'PUT': return UserController.update(id)
    elif request.method == 'DELETE': return UserController.delete(id)

# 2. API Products
@app.route('/api/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET': return ProductController.index()
    else: return ProductController.store()

@app.route('/api/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product_detail_api(id):
    if request.method == 'GET': return ProductController.show(id)
    elif request.method == 'PUT': return ProductController.update(id)
    elif request.method == 'DELETE': return ProductController.delete(id)

#  JALUR WEB (WEBSITE ASLI)

@app.route('/')
def home():
    return WebController.home()

@app.route('/detail/<int:product_id>')
def detail_product(product_id): 
    return WebController.detail_product(product_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return WebController.login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return WebController.register()

@app.route('/logout')
def logout():
    return WebController.logout()

@app.route('/dashboard')
def dashboard():
    return WebController.dashboard()

@app.route('/cart')
def cart():
    return WebController.cart()

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    return WebController.add_to_cart(product_id)

@app.route('/update_cart/<int:item_id>/<action>')
def update_cart(item_id, action):
    return WebController.update_cart(item_id, action)

@app.route('/delete_cart/<int:item_id>')
def delete_cart(item_id):
    return WebController.delete_cart(item_id)

@app.route('/beli/<int:product_id>')
def beli(product_id):
    return WebController.beli(product_id)

@app.route('/checkout_process', methods=['POST'])
def checkout_process():
    return WebController.checkout_process()

@app.route('/checkout_cart', methods=['GET', 'POST'])
def checkout_cart():
    return WebController.checkout_cart()

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return WebController.contact()

@app.route('/about')
def about():
    return WebController.about()

# -- Admin Web Routes --
@app.route('/admin')
def admin_dashboard():
    return WebController.admin_dashboard()

@app.route('/admin/add', methods=['GET', 'POST'])
def add_product():
    return WebController.add_product()

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    return WebController.edit_product(product_id)

@app.route('/admin/delete/<int:product_id>')
def delete_product(product_id):
    return WebController.delete_product(product_id)