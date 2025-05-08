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
        print(f"Error connecting to database: {str(e)}")
        return None

def add_item(name, description):
    """Add an item to the database"""
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        cursor = conn.cursor()
        # Create items table if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='items' AND xtype='U')
            CREATE TABLE items (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
        """)
        
        # Insert the new item
        cursor.execute("""
            INSERT INTO items (name, description)
            VALUES (?, ?)
        """, (name, description))
        
        conn.commit()
        
        # Get the ID of the inserted item
        cursor.execute("SELECT @@IDENTITY")
        item_id = cursor.fetchone()[0]
        
        return {
            "id": item_id,
            "name": name,
            "description": description
        }
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_item(item_id):
    """Retrieve an item from the database by ID"""
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description
            FROM items
            WHERE id = ?
        """, (item_id,))
        
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
        return {"error": "Item not found"}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()