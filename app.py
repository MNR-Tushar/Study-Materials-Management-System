import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__)

# MySQL Connection Setup
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    return connection


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
@app.route('/delete_material/<int:material_id>')
def delete_material(material_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM materials WHERE material_id = %s", (material_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))

#Add Order
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        material_id = request.form['material_id']
        quantity = int(request.form['quantity'])

        # Material
        cursor.execute("SELECT price, discount FROM materials WHERE material_id = %s", (material_id,))
        material = cursor.fetchone()

        if material:
            price = material['price']
            discount = material['discount']
            price_after_discount = price - (price * discount / 100)
            total_price = quantity * price_after_discount

            # Order insert
            cursor.execute("""
                INSERT INTO orders (customer_id, customer_name, material_id, quantity, total_price, order_date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (customer_id, customer_name, material_id, quantity, total_price))

            conn.commit()

        cursor.close()
        conn.close()
        return redirect('/')
    
    else:
        cursor.execute("SELECT * FROM materials")
        materials = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('add_order.html', materials=materials)

#View all Order
@app.route('/all_orders')
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
