import os
from flask import Flask, render_template, request, redirect, url_for,session,flash
import mysql.connector
from functools import wraps
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()


app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'a3f5c1e2b7d643cfb2d8790caae210d7'


# MySQL Connection Setup
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        port=os.environ.get("MYSQLPORT"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE")
    )
    return connection

# Auth decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Login required", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required!', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']  # store admin status
            flash('Logged in successfully!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose another.", "danger")
            return redirect("/register")

        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", 
                       (username, hashed_password, False))
        db.commit()
        flash("Registration successful. Please login.", "success")
        return redirect("/login")

    return render_template("register.html")




@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Retrieve all materials
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', materials=materials)


#Add Material
@app.route('/add_material', methods=['GET', 'POST'])
@admin_required
def add_material():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        discount = request.form['discount']
        availability_status = request.form['availability_status']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO materials (name, category, quantity, price, discount, availability_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, category, quantity, price, discount, availability_status))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    return render_template('add_material.html')


#Update Material
@app.route('/update_material/<int:material_id>', methods=['GET', 'POST'])
@admin_required
def update_material(material_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM materials WHERE material_id = %s", (material_id,))
    material = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        discount = request.form['discount']
        availability_status = request.form['availability_status']

        cursor.execute("""
            UPDATE materials
            SET name = %s, category = %s, quantity = %s, price = %s, discount = %s, availability_status = %s
            WHERE material_id = %s
        """, (name, category, quantity, price, discount, availability_status, material_id))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    cursor.close()
    connection.close()
    return render_template('update_material.html', material=material)


#Delete Material
@app.route('/update_material/<int:material_id>', methods=['GET', 'POST'])
@admin_required
def delete_material(material_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM materials WHERE material_id = %s", (material_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))


# Add Order
@app.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        material_id = request.form['material_id']
        quantity = int(request.form['quantity'])

        # লগইন ইউজারের ID session থেকে নিও
        user_id = session.get('id')

        # Material
        cursor.execute("SELECT price, discount FROM materials WHERE material_id = %s", (material_id,))
        material = cursor.fetchone()

        if material:
            price = material['price']
            discount = material['discount']
            price_after_discount = price - (price * discount / 100)
            total_price = quantity * price_after_discount

            # Order insert with user_id
            cursor.execute("""
                INSERT INTO orders 
                (customer_id, customer_name, material_id, quantity, total_price, order_date, user_id)
                VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            """, (customer_id, customer_name, material_id, quantity, total_price, user_id))

            conn.commit()

        cursor.close()
        conn.close()
        return redirect('/my_orders')  # redirect to user's order page
    
    else:
        cursor.execute("SELECT * FROM materials")
        materials = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('add_order.html', materials=materials)



@app.route('/my_orders')
@login_required
def my_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user_id = session.get('id')  # লগইন ইউজারের আইডি

    cursor.execute("""
        SELECT orders.*, materials.name AS material_name
        FROM orders
        JOIN materials ON orders.material_id = materials.material_id
        WHERE orders.user_id = %s
        ORDER BY orders.order_date DESC
    """, (user_id,))

    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('my_orders.html', orders=orders)


#View all Order
@app.route('/all_orders')
@admin_required
def all_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT orders.order_id, orders.customer_name, materials.name as material_name,
               orders.quantity, orders.total_price, orders.order_date
        FROM orders
        JOIN materials ON orders.material_id = materials.material_id
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('all_orders.html', orders=orders)

#Update order
@app.route('/update_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        material_id = request.form['material_id']
        quantity = int(request.form['quantity'])

        # Get price of selected material
        cursor.execute("SELECT price FROM materials WHERE material_id = %s", (material_id,))
        material = cursor.fetchone()
        price = material['price']
        total_price = price * quantity

        cursor.execute("""
            UPDATE orders
            SET customer_name = %s, material_id = %s, quantity = %s, total_price = %s
            WHERE order_id = %s
        """, (customer_name, material_id, quantity, total_price, order_id))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect('/all_orders')

    # GET request: show form with existing order
    cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()

    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('update_order.html', order=order, materials=materials)


#Delete order
@app.route('/delete_order/<int:order_id>', methods=['GET'])
@login_required
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect('/all_orders')


#Delete all Material
@app.route('/delete_all_materials', methods=['POST'])
@login_required
def delete_all_materials():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materials")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
