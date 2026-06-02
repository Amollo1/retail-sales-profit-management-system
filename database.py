import sqlite3
import os
from datetime import datetime

DB_PATH = "data/shop.db"

def init_db():
    """Initialize the SQLite database with required tables"""
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            buying_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            cost_price REAL NOT NULL,
            profit REAL NOT NULL,
            payment_method TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    # Daily summary table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            total_sales REAL NOT NULL,
            total_profit REAL NOT NULL,
            total_items_sold INTEGER NOT NULL,
            transaction_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get a database connection"""
    return sqlite3.connect(DB_PATH)

def add_product(name, category, buying_price, selling_price, quantity):
    """Add a new product to the inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO products (name, category, buying_price, selling_price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, buying_price, selling_price, quantity))
        conn.commit()
        return True, "Product added successfully"
    except sqlite3.IntegrityError:
        return False, "Product already exists"
    finally:
        conn.close()

def update_product(product_id, name, category, buying_price, selling_price, quantity):
    """Update product details"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE products 
            SET name=?, category=?, buying_price=?, selling_price=?, quantity=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (name, category, buying_price, selling_price, quantity, product_id))
        conn.commit()
        return True, "Product updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_all_products():
    """Get all products from inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, buying_price, selling_price, quantity FROM products ORDER BY name')
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    """Get a specific product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, buying_price, selling_price, quantity FROM products WHERE id=?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def reduce_stock(product_id, quantity):
    """Reduce stock after a sale"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET quantity = quantity - ? WHERE id=?', (quantity, product_id))
    conn.commit()
    conn.close()

def add_sale(product_id, product_name, quantity, unit_price, cost_price, payment_method):
    """Record a sale transaction"""
    conn = get_connection()
    cursor = conn.cursor()
    
    total_amount = quantity * unit_price
    profit = (unit_price - cost_price) * quantity
    
    cursor.execute('''
        INSERT INTO sales (product_id, product_name, quantity, unit_price, total_amount, cost_price, profit, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (product_id, product_name, quantity, unit_price, total_amount, cost_price, profit, payment_method))
    
    conn.commit()
    conn.close()
    
    return total_amount, profit

def get_today_sales():
    """Get all sales for today"""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT id, product_name, quantity, unit_price, total_amount, profit, payment_method, created_at
        FROM sales
        WHERE DATE(created_at) = ?
        ORDER BY created_at DESC
    ''', (today,))
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_sales_by_date_range(start_date, end_date):
    """Get sales within a date range"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, product_name, quantity, unit_price, total_amount, profit, payment_method, created_at
        FROM sales
        WHERE DATE(created_at) BETWEEN ? AND ?
        ORDER BY created_at DESC
    ''', (start_date, end_date))
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_today_summary():
    """Get today's sales and profit summary"""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT 
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_sales,
            SUM(profit) as total_profit,
            SUM(quantity) as total_items_sold
        FROM sales
        WHERE DATE(created_at) = ?
    ''', (today,))
    
    result = cursor.fetchone()
    conn.close()
    
    return {
        'transaction_count': result[0] or 0,
        'total_sales': result[1] or 0.0,
        'total_profit': result[2] or 0.0,
        'total_items_sold': result[3] or 0
    }

def delete_product(product_id):
    """Delete a product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()
    return True

def clear_all_sales():
    """Delete all sales records"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sales')
    conn.commit()
    conn.close()
    return True

def clear_all_products():
    """Delete all products from inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products')
    conn.commit()
    conn.close()
    return True

def reset_database():
    """Delete all data and reinitialize database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Drop all tables
    cursor.execute('DROP TABLE IF EXISTS sales')
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS daily_summary')
    
    conn.commit()
    conn.close()
    
    # Reinitialize the database
    init_db()
    return True

# Initialize database on import
init_db()
