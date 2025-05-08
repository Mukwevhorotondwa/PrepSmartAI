import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
DB_SERVER = os.getenv('DB_SERVER')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_db_connection():
    """Create and return a database connection"""
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USER};PWD={DB_PASSWORD}'
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        raise Exception(f"Error connecting to database: {str(e)}")

def initialize_db():
    """Initialize the database by creating the items table if it doesn't exist"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='items' AND xtype='U')
            CREATE TABLE items (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
        """)
        conn.commit()
    except pyodbc.Error as e:
        raise Exception(f"Error initializing database: {str(e)}")
    finally:
        conn.close()

def add_item(name, description):
    """Add an item to the database"""
    if not name or not isinstance(name, str) or len(name.strip()) == 0:
        raise ValueError("Name must be a non-empty string")
    if not isinstance(description, str):
        raise ValueError("Description must be a string")
    
    name = name.strip()
    description = description.strip() if description else None
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO items (name, description)
            VALUES (?, ?)
        """, (name, description))
        conn.commit()
        
        cursor.execute("SELECT @@IDENTITY")
        item_id = cursor.fetchone()[0]
        
        return {
            "id": item_id,
            "name": name,
            "description": description
        }
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def get_db_size():
    """Return the number of items in the database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        return cursor.fetchone()[0]
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def get_item_from_db(name):
    """Retrieve an item from the database by name"""
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description
            FROM items
            WHERE name = ?
        """, (name.strip(),))
        
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
        return None
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def get_item_from_db_by_id(id):
    """Retrieve an item from the database by ID"""
    if not isinstance(id, int) or id <= 0:
        raise ValueError("ID must be a positive integer")
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description
            FROM items
            WHERE id = ?
        """, (id,))
        
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
        return None
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def get_all_items_from_db():
    """Retrieve all items from the database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM items")
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            } for row in rows
        ]
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def update_item(id, name, description):
    """Update an item in the database"""
    if not isinstance(id, int) or id <= 0:
        raise ValueError("ID must be a positive integer")
    if not name or not isinstance(name, str) or len(name.strip()) == 0:
        raise ValueError("Name must be a non-empty string")
    if not isinstance(description, str):
        raise ValueError("Description must be a string")
    
    name = name.strip()
    description = description.strip() if description else None
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE items
            SET name = ?, description = ?
            WHERE id = ?
        """, (name, description, id))
        conn.commit()
        
        if cursor.rowcount == 0:
            return None
        return {
            "id": id,
            "name": name,
            "description": description
        }
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def delete_item_from_db(id):
    """Delete an item from the database"""
    if not isinstance(id, int) or id <= 0:
        raise ValueError("ID must be a positive integer")
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (id,))
        conn.commit()
        
        return cursor.rowcount > 0
    except pyodbc.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_db()