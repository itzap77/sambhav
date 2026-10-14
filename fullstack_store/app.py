from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_college_project_key'
DB_FILE = os.path.join(os.path.dirname(__file__), 'database', 'store.db')

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'cart' not in session:
        session['cart'] = {}
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    with get_db() as conn:
        products = conn.execute('SELECT * FROM Products').fetchall()
    return jsonify([dict(p) for p in products])

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = str(data['product_id'])
    
    with get_db() as conn:
        product = conn.execute('SELECT stock_qty FROM Products WHERE product_id = ?', (product_id,)).fetchone()
    
    if product and product['stock_qty'] > 0:
        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        session['cart'] = cart
        session.modified = True
        return jsonify({"status": "success", "message": "Added to cart"})
    return jsonify({"status": "error", "message": "Out of stock"}), 400

@app.route('/api/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    if not cart:
        return jsonify({"items": [], "total": 0, "count": 0})
    
    with get_db() as conn:
        placeholders = ','.join('?' for _ in cart.keys())
        query = f'SELECT product_id, name, price, image_url FROM Products WHERE product_id IN ({placeholders})'
        products = conn.execute(query, list(cart.keys())).fetchall()
    
    cart_data = []
    total = count = 0
    for p in products:
        qty = cart[str(p['product_id'])]
        subtotal = p['price'] * qty
        total += subtotal
        count += qty
        cart_data.append({"name": p['name'], "price": p['price'], "qty": qty, "subtotal": subtotal, "image_url": p['image_url']})
        
    return jsonify({"items": cart_data, "total": total, "count": count})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return jsonify({"status": "error", "message": "Cart is empty"}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN TRANSACTION")
        total_amt = 0
        items_to_process = []
        
        for pid, qty in cart.items():
            prod = cursor.execute('SELECT price, stock_qty FROM Products WHERE product_id = ?', (pid,)).fetchone()
            if prod['stock_qty'] < qty:
                raise Exception(f"Insufficient stock for product ID {pid}")
            total_amt += (prod['price'] * qty)
            items_to_process.append((pid, qty, prod['price']))
            
        cursor.execute('INSERT INTO Orders (total_amt) VALUES (?)', (total_amt,))
        order_id = cursor.lastrowid
        
        for pid, qty, price in items_to_process:
            cursor.execute('INSERT INTO Order_Items (order_id, product_id, qty, price_locked) VALUES (?, ?, ?, ?)', (order_id, pid, qty, price))
            cursor.execute('UPDATE Products SET stock_qty = stock_qty - ? WHERE product_id = ?', (qty, pid))
            
        conn.commit()
        session['cart'] = {}
        session.modified = True
        return jsonify({"status": "success", "order_id": order_id})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        print("Database not found. Please run 'python3 database/init_db.py' first.")
    else:
        app.run(debug=True)
